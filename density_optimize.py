from utils import merge_seed


class DensityOptimize(object):
    """密度优化算法"""

    def __init__(self,
                 seed,
                 spare_capacity,
                 dense_step=10,
                 threshold=0.01
                 ):
        self.seed = seed
        self.spare_capacity = spare_capacity
        self.dense_step = dense_step
        self.threshold = threshold

        self.window_size = int(1 / self.threshold / self.dense_step)
        self.window_size = 1 if self.window_size < 1 else self.window_size

        self.max_index = pow(10, self.spare_capacity)

        self.status_list = []
        self.useful_sparse_set = set()

    def sparse_waybill_list(self):
        for index in range(0, self.max_index, self.dense_step):
            yield merge_seed(self.seed, str(index).zfill(self.spare_capacity))

    def feed_status(self, status):
        self.status_list.append(status)

    def process_slide_ratio(self):
        for slide_index in range(len(self.status_list) - self.window_size + 1):
            sub_status_list = self.status_list[slide_index: slide_index + self.window_size]
            if any(sub_status_list):
                for index in range(slide_index, slide_index + self.window_size):
                    self.useful_sparse_set.add(index)

    def get_final_waybill_list(self):
        result_waybill_list = []
        for sparse_index in self.useful_sparse_set:
            result_waybill_list.extend([merge_seed(self.seed, str(index + sparse_index * self.dense_step)
                                                   .zfill(self.spare_capacity))
                                        for index in range(self.dense_step)])

        return result_waybill_list
