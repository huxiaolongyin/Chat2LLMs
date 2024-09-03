import random
import string


def generate_id(len: int = 16):
    """生成一个16位的随机字符串"""
    return "".join(random.choices(string.ascii_letters + string.digits, k=len))
