import numpy as np

import rospy
from std_msgs.msg import Int16MultiArray, MultiArrayLayout, MultiArrayDimension

def gen_dim(label, size, stride):
    dim = MultiArrayDimension()
    dim.label = label
    dim.size = size
    dim.stride = stride
    return dim

def gen_layout(shape):
    layout = MultiArrayLayout()
    layout.dim = [gen_dim('dim{}'.format(i), size, 1) for i, size in enumerate(shape)]
    layout.data_offset = 0
    return layout

class ROSAdapter(object):
    def __init__(self, circuit, inputs, output):
        self.circuit = circuit

        self.subscribers = []
        self.callbacks = []

        for i, topic in enumerate(inputs):
            def callback(msg):
                shape = [dim.size for dim in msg.layout.dim]
                array = np.array(msg.data, dtype=np.int16).reshape(shape)
                self.circuit.in_ports[i].send(array)

            self.callbacks.append(callback)
            sub = rospy.Subscriber(topic, Int16MultiArray, self.callbacks[i])
            self.subscribers.append(sub)

        self.publisher = rospy.Publisher(output, Int16MultiArray, queue_size=10)

        def watcher(data):
            if data is None:
                return
            msg = Int16MultiArray()
            msg.data = data
            msg.layout = gen_layout(data.shape)
            self.publisher.pub(msg)

        self.circuit.out_port.watch(watcher)

    @property
    def components(self):
        return self.circuit.components
