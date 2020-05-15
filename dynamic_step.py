from math import sqrt

from utils import merge_seed

from queue import Queue


class DynamicStep(object):
    """动态步长算法"""

    def __init__(self,
                 seed,
                 spare_capacity,
                 max_step=10,
                 compact_step=20):
        """
        :param seed:  种子
        :param spare_capacity:  种子后缀的长度
        :param max_step:  最大步长
        :param compact_step:  碰撞到运单后需要检测之后的compact_step内的所有运单；
        """

        self.seed = seed
        self.spare_capacity = spare_capacity
        self.max_step = max_step
        self.compact_step = compact_step

        self.max_index = pow(10, self.spare_capacity)

        self.step = 0
        self.current_index = 0

        self.pass_status_num = None
        self.accumulate_queue = Queue()
        self.nearest_waybill_list = []

        self.proper_nearest_list_size = sqrt(2 * self.compact_step)

    def next_waybill(self):
        while not self.accumulate_queue.empty():
            index = self.accumulate_queue.get()
            if index in self.nearest_waybill_list:
                continue
            return True, merge_seed(self.seed, str(index).zfill(self.spare_capacity))
        if self.pass_status_num and self.pass_status_num > 0:
            self.pass_status_num -= 1

        self.current_index += self.step
        if self.current_index < self.max_index:
            self.nearest_waybill_list.append(self.current_index)
            if len(self.nearest_waybill_list) > self.proper_nearest_list_size:
                self.nearest_waybill_list.pop(0)

            return True, merge_seed(self.seed, str(self.current_index).zfill(self.spare_capacity))
        return False, None

    def feed_status(self, status):
        if not self.accumulate_queue.empty():
            return None
        if status:
            self.pass_status_num = self.compact_step
            self.step = 1
        if self.pass_status_num:
            return None
        if status and self.step == self.max_step:
            for index in range(max(self.current_index - self.compact_step + 1, 0), self.current_index):
                self.accumulate_queue.put(index)
        if not status:
            if self.step != self.max_step:
                self.step += 1

