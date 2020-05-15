import random


def get_status(probability):
    """以probability概率返回True"""
    true_probability = random.uniform(0, 1)
    return "1" if true_probability < probability else "0"


if __name__ == '__main__':

    result_list = []

    for i in range(100000):
        # 1. 1-20000以0.001概率生成数据
        if i < 20000:
            result_list.append(get_status(0.001))
        # 2. 20000-25000以0.5概率生成数据
        elif i < 25000:
            result_list.append(get_status(0.2))
        else:
            result_list.append(get_status(0.001))

    with open("test_data.txt", "w", encoding="utf-8") as writer:
        writer.writelines(["{}\n".format(status) for status in result_list])
