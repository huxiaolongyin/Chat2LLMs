from importlib.metadata import version, PackageNotFoundError

try:
    __VERSION__ = version("chat2llms")
except PackageNotFoundError:
    # 包未安装，可能处于开发模式
    __VERSION__ = "unknown"
