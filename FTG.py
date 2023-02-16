import math
import numpy as np
from scipy.signal import medfilt

class GapFollower:
    def __init__(self, fixed_speed=True):
        self._max_range = 10.0
        self._fixed_speed = fixed_speed

    @staticmethod
    def preprocess_lidar(ranges, kernel_size=5):
        # Step 1: interpolate nan values
        proc_ranges = np.array(ranges)
        nans = np.isnan(proc_ranges)
        nan_idx = np.where(nans)
        x = np.where(~nans)[0]
        y = proc_ranges[~nans]
        proc_ranges[nan_idx] = np.interp(nan_idx, x, y)
        # Step 2: apply a median filter to the interpolated values
        proc_ranges = medfilt(proc_ranges, kernel_size)
        return proc_ranges

    @staticmethod
    def find_max_gap(free_space_ranges, min_distance):
        """ Return the start index & end index of the max gap in free_space_ranges

        """

        gaps = np.hstack(([False], free_space_ranges >= min_distance + 0.1, [False]))

        c=np.diff(gaps)

        gap_indices = np.where(c)[0].reshape(-1, 2)


        if gap_indices.size != 0:

            largest_gap = gap_indices[np.argmax(np.diff(gap_indices))]
            return largest_gap
        else:
            return np.ndarray([0, free_space_ranges.size - 1])

    @staticmethod
    def find_best_point(start_i, end_i, ranges, version="center"):
        """Start_i & end_i are start and end indicies of max-gap range, respectively
        Return index of best point in ranges

        """
        if version == "center":
            target = int((start_i + end_i) / 2)
        elif version == "demo":
            furthest = np.argmax(ranges[start_i:end_i]) + start_i

            center = (end_i + start_i) / 2
            factor = 0.65
            target = int(np.round(factor * furthest + (1.0 - factor) * center))



        else:
            target = 0.0
        return target

    @staticmethod
    def _get_angle(best_point):
        angle = (-math.pi / 2 + best_point * math.pi / 675)
        angle = np.clip(angle, -1, +1)
        return angle

    def _get_motor(self, max_range):
        """ Compute the motor force based on the maximum frontal range
         """

        if self._fixed_speed and max_range < 3.0:
            return 0.01  # very low motor force to keep low velocity (~1.5m/s)
        else:
            return max_range / self._max_range * 0.5

    def gap_action(self, lidar_obs):
        scan = lidar_obs
        if len(scan.shape) > 1:
            scan = scan.reshape(scan.shape[1])
        proc_ranges = self.preprocess_lidar(scan, kernel_size=3)

        min_index, max_index = 0, 675
        proc_ranges = proc_ranges[min_index:max_index]

        # Find closest point to LiDAR
        min_distance = np.min(proc_ranges)

        # Find max length gap
        if len(proc_ranges) < 1:
            return 0, 0
        gap = self.find_max_gap(free_space_ranges=proc_ranges, min_distance=min_distance)
        if len(gap) < 1:
            return 0, 0
        # Find the best point in the gap
        best_point = min_index + self.find_best_point(start_i=gap[0], end_i=gap[1], ranges=proc_ranges, version="demo")

        # Publish Drive message
        angle = self._get_angle(best_point)
        motor = self._get_motor(max(proc_ranges[675 // 2 - 50:675 // 2 + 50]))
       
        return np.array([angle, motor])

    def __call__(self, obs, *args):
        return np.array(self.gap_action(obs))