from utils import merge_seed


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

        self.step = 1
        self.current_index = 0
        self.current_compact = 0

    def next_waybill(self):
        self.current_index += self.step
        if self.current_index < self.max_index:
            return True, merge_seed(self.seed, str(self.current_index).zfill(self.spare_capacity))
        return False, None

    def feed_status(self, status):
        if status:
            self.step = 1
            self.current_compact = 0
        else:
            if self.current_compact >= self.compact_step and self.step != self.max_step:
                self.step += 1
            self.current_compact += 1

