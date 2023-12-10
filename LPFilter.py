import numpy
import math


# 'alpha' is the smoothing factor of the low pass filter, where
#   alpha = DT / (RC + DT)
#   DT = 1 and RC are not passed, instead caller must pass the value of alpha directly
# The filter follows the discrete implementation, where:
#   out[n] = alpha * in[n] + (1 - alpha) * out[n-1] 
class LowPassFilter():

    __x_out = 0
    __y_out = 0

    def __init__(self, alpha = 0.5):

        if alpha > 1 or alpha < 0:
            raise ValueError("Error: alpha must be between 0 and 1, setting alpha to default value 0.5...")
            self.__alpha = 0.5
        else:
            self.__alpha = alpha

    def apply(self, x, y):
        self.__x_out = int(self.__alpha * x + (1 - self.__alpha) * self.__x_out)
        self.__y_out = int(self.__alpha * y + (1 - self.__alpha) * self.__y_out)
        return self.__x_out, self.__y_out
