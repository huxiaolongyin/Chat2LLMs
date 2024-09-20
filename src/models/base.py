from sqlalchemy.ext.declarative import declarative_base
import random
import string

Base = declarative_base()


def generate_id(len: int = 16):
    """生成一个16位的随机字符串"""
    return "".join(random.choices(string.ascii_letters + string.digits, k=len))
