from chat2llm import TextCls, Generate, Speech2Text
import pytest


class TestClass:
    # 测试文本分类
    def test_text_cls(self):
        res = TextCls.htw_text_cls(("你好", "月亮为什么会发光"))

        assert res == ["问候", "常识"]

    # 测试文本生成
    def test_generate(self):
        result = ""
        for chunk in Generate.taskai("月亮为什么会发光"):
            result += chunk

        assert result  # Check that the result is not empty
        assert "月亮" in result
        assert len(result) > 10  # Check that the response has a reasonable length

    # 测试语音识别
    def test_speech2text(self):
        audio = "D:/code/DataWarehouse/03_代码/03_chat2LLMs/tests/asr_example.wav"
        result = Speech2Text.speach_to_text(audio)
        assert result
        assert "欢迎大家来体验" in result
        assert len(result) > 10


if __name__ == "__main__":
    pytest.main(["-s", "tests/chat2llm_test.py"])
