__author__ = 'Hoang Thanh Lam'
__date__ = '31/03/17'
import numpy as np



# This class is designed to get sum of square error with respect to mean value of X ={x1,x2,...,xn}
# SE = (x1-mean)^2 + (x2-mean)^2 + ...+ (xn-mean)^2
# mean = (x1+x2+...+xn)/n
# We can rewrite SE as:
# SE = (x1^2+x2^2+...+xn^2) - 2*mean*(x1+x2+...+xn) + n*mean^2
#    = (x1^2+x2^2+...+xn^2) - 2*n*mean^2 + n*mean^2
#    = (x1^2+x2^2+...+xn^2)  - n*mean^2
#    = (x1^2+x2^2+...+xn^2) - (x1+x2+...+xn)^2/n
#    = sum_x2 - sum^2_x/n
# where sum_x2 = (x1^2+x2^2+...+xn^2), and sum_x = x1+x2+...+xn
# Therefore, in order to calculate SE we just need to keep sum_x2 and sum_x. This enables us to efficiently update SE
# if the set X  is changed (add or remove new elements) without re-calculating SE from scratch
class SquareError:
    def __init__(self):
        self.sum_x2 = 0  # sum of square of xi
        self.sum_x = 0  # sum of of xi
        self.n = 0  # the number of elements in the set

    def add(self, x):
        """
        add a new element x
        :param x: an np.array
        :return: None
        """

        self.sum_x2 += np.multiply(x,x)
        self.sum_x += x
        self.n += 1

    def remove(self, x):
        """
        remove an element x
        :param x: an np.array
        :return:
        """
        self.sum_x2 -= np.multiply(x,x)
        self.sum_x -= x
        self.n -= 1

    def sum_of_square_error(self):
        """
        get sum of square error
        :return:
        """
        vector_error = self.sum_x2 - np.multiply(self.sum_x,self.sum_x)/self.n
        return np.dot(vector_error,vector_error)

    def add_list(self, x):
        """
        add all elements in the list of np.array
        :param x: a list of np.array
        :return:
        """
        for i in range(len(x)):
            self.add(x[i])