# coding=utf-8
"""
Python module for computing coverage number
"""
import pybloomfilter


class CoveringNumber(object):
    """
    Class to implement Eq.(4) of the paper
    """

    def __init__(self, num_samples, expected_num_points, batch_size, error_rate=0.0000001):
        self._num_samples = num_samples
        self._batch_size = batch_size
        self._expected_num_points = num_samples
        self._denominator = self._expected_num_points
        self._numerator = 0.0

        self._bf = pybloomfilter.BloomFilter(expected_num_points*100, error_rate)
        self._actual_num_points = 0.

    def update(self, point):

        pt_np = point.numpy().tolist()
        is_not_in = not self._bf.add(hash(str(pt_np)))
        self._numerator += int(is_not_in)
        if is_not_in:
            print("NEW POINT")
        return(self._numerator/(self._num_samples))
        
    def ratio(self):
        """
        :return: the ratio of the visited samples to the maximum expected ones
        """
        return self._numerator * 1. / self._denominator

