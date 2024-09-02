from dotenv import load_dotenv


def set_env():
    """加载环境变量"""
    dotenv_path = "D:/code/chat2LLMs/.env"
    load_dotenv(dotenv_path=dotenv_path)
