from density_optimize import DensityOptimize
from utils import *


def exceed_test_file(file_path="test_data.txt"):
    with open(file_path, "r", encoding="utf-8") as reader:
        lines = reader.readlines()

    lines = [True if line.strip() == "1" else False for line in lines]

    return lines


validation_list = exceed_test_file()


def predict_waybill(sub_waybill):
    """判断某个运单是否有效"""
    return validation_list[int(sub_waybill[-5:])]


if __name__ == '__main__':
    # 种子为123456，5位子区间；
    seed = "123456"
    spare_capacity = 5

    # 遍历统计数据；
    total_cal_nums = 0
    total_useful_nums = 0
    for i in range(pow(10, 5)):
        new_waybill = merge_seed(seed, str(i).zfill(spare_capacity))
        total_cal_nums += 1
        if predict_waybill(new_waybill):
            total_useful_nums += 1

    print("遍历算法，检测总次数为{}，\t 有效运单数量为{}".format(total_cal_nums, total_useful_nums))

    density_optimize = DensityOptimize(seed, spare_capacity, 10, 0.01)

    total_cal_nums = 0
    total_useful_nums = 0
    for waybill in density_optimize.sparse_waybill_list():
        density_optimize.feed_status(predict_waybill(waybill))
        total_cal_nums += 1

    density_optimize.process_slide_ratio()

    for new_waybill in density_optimize.get_final_waybill_list():
        total_cal_nums += 1
        if predict_waybill(new_waybill):
            total_useful_nums += 1

    print("密度优化算法，检测总次数为{}，\t 有效运单数量为{}".format(total_cal_nums, total_useful_nums))
