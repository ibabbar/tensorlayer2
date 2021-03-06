#! /usr/bin/python
# -*- coding: utf-8 -*-

import tensorflow as tf

from tensorlayer.layers.core import Layer

from tensorlayer import logging

__all__ = [
    'Concat',
    'Elementwise',
]


class Concat(Layer):
    """A layer that concats multiple tensors according to given axis.

    Parameters
    ----------
    concat_dim : int
        The dimension to concatenate.
    name : None or str
        A unique layer name.

    Examples
    ----------
    >>> import tensorflow as tf
    >>> import tensorlayer as tl
    >>> sess = tf.InteractiveSession()
    >>> x = tf.placeholder(tf.float32, shape=[None, 784])
    >>> inputs = tl.layers.Input(x, name='input')
    [TL]   Input input (?, 784)
    >>> net1 = tl.layers.Dense(inputs, 800, act=tf.nn.relu, name='relu1_1')
    [TL]   Dense relu1_1: 800, relu
    >>> net2 = tl.layers.Dense(inputs, 300, act=tf.nn.relu, name='relu2_1')
    [TL]   Dense relu2_1: 300, relu
    >>> net = tl.layers.Concat([net1, net2], 1, name ='concat_layer')
    [TL]   Concat concat, 1100
    >>> tl.layers.initialize_global_variables(sess)
    >>> net.print_params()
    [TL]   param   0: relu1_1/W:0          (784, 800)         float32_ref
    [TL]   param   1: relu1_1/b:0          (800,)             float32_ref
    [TL]   param   2: relu2_1/W:0          (784, 300)         float32_ref
    [TL]   param   3: relu2_1/b:0          (300,)             float32_ref
        num of params: 863500
    >>> net.print_layers()
    [TL]   layer   0: relu1_1/Relu:0       (?, 800)           float32
    [TL]   layer   1: relu2_1/Relu:0       (?, 300)           float32
    [TL]   layer   2: concat:0       (?, 1100)          float32

    """

    def __init__(
            self,
            concat_dim=-1,
            name=None, #'concat',
    ):

        # super(ConcatLayer, self).__init__(prev_layer=prev_layer, name=name)
        super().__init__(name)
        self.concat_dim = concat_dim
        logging.info("Concat %s: axis: %d" % (self.name, concat_dim))

    def build(self, inputs):
        pass

    def forward(self, inputs):
        """

        prev_layer : list of :class:`Layer`
            List of layers to concatenate.
        """
        outputs = tf.concat(inputs, self.concat_dim, name=self.name)

        return outputs


class Elementwise(Layer):
    """A layer that combines multiple :class:`Layer` that have the same output shapes
    according to an element-wise operation.

    Parameters
    ----------
    combine_fn : a TensorFlow element-wise combine function
        e.g. AND is ``tf.minimum`` ;  OR is ``tf.maximum`` ; ADD is ``tf.add`` ; MUL is ``tf.multiply`` and so on.
        See `TensorFlow Math API <https://www.tensorflow.org/versions/master/api_docs/python/math_ops.html#math>`__ .
    act : activation function
        The activation function of this layer.
    name : None or str
        A unique layer name.

    Examples
    --------
    >>> import tensorflow as tf
    >>> import tensorlayer as tl
    >>> x = tf.placeholder(tf.float32, shape=[None, 784])
    >>> inputs = tl.layers.Input(x, name='input')
    >>> net_0 = tl.layers.Dense(inputs, n_units=500, act=tf.nn.relu, name='net_0')
    >>> net_1 = tl.layers.Dense(inputs, n_units=500, act=tf.nn.relu, name='net_1')
    >>> net = tl.layers.Elementwise([net_0, net_1], combine_fn=tf.minimum, name='minimum')
    >>> net.print_params(False)
    [TL]   param   0: net_0/W:0            (784, 500)         float32_ref
    [TL]   param   1: net_0/b:0            (500,)             float32_ref
    [TL]   param   2: net_1/W:0            (784, 500)         float32_ref
    [TL]   param   3: net_1/b:0            (500,)             float32_ref
    >>> net.print_layers()
    [TL]   layer   0: net_0/Relu:0         (?, 500)           float32
    [TL]   layer   1: net_1/Relu:0         (?, 500)           float32
    [TL]   layer   2: minimum:0            (?, 500)           float32
    """

    def __init__(
            self,
            combine_fn=tf.minimum,
            act=None,
            name=None, #'elementwise',
    ):

        # super(Elementwise, self).__init__(prev_layer=prev_layer, act=act, name=name)
        super().__init__(name)

        logging.info(
            "Elementwise %s: fn: %s act: %s" % (self.name, combine_fn.__name__, ('No Activation' if self.act is None else self.act.__name__))
        )

    def build(self, inputs):
        pass

    def forward(self, inputs):
        """

        Parameters
        ----------
        prev_layer : list of :class:`Layer`
            The list of layers to combine.
        """
        outputs = inputs[0]
        for input in inputs[1:]:
            outputs = combine_fn(outputs, input, name=self.name)

        outputs = self.act(outputs)
        return outputs
