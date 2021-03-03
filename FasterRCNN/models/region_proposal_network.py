import tensorflow as tf
import tensorflow.keras
from tensorflow.keras import models
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense

def layers(input_map, anchors_per_location):
  assert len(input_map.shape) == 4
  
  # We can infer the total number of anchors from the input map size
  height = input_map.shape[1]
  width = input_map.shape[2]
  num_anchors = anchors_per_location * height * width

  # 3x3 convolution over input map producing 512-d result at each output. The center of each output is an anchor point (k anchors at each point).
  anchors = Conv2D(name = "rpn_conv1", kernel_size = (3,3), strides = 1, filters = 512, padding = "same", activation = "relu", kernel_initializer = "normal")(input_map)

  # Classification layer: predicts whether there is an object at the anchor or not. We use a sigmoid function, where > 0.5 is indicates a positive result.
  classifier = Conv2D(name = "rpn_class", kernel_size = (1,1), strides = 1, filters = num_anchors, padding = "same", activation = "sigmoid", kernel_initializer = "uniform")(anchors)
  
  # Regress
  regressor = Conv2D(name = "rpn_boxes", kernel_size = (1,1), strides = 1, filters = 4 * num_anchors, padding = "same", activation = "linear", kernel_initializer = "zero")(anchors)

  return [ classifier, regressor ]