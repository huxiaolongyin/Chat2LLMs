# import asyncio
# import io

# from pydub.playback import play
# from pydub import AudioSegment


# # async def play_audio_data():
# #     text = "本文不仅系统性地概述了数据质量提升的关键步骤，还强调了每一阶段的重点与核心策略，旨在为企业提供一个清晰、可行的数据治理路径。希望每一位读者都能从中获得灵感，开启属于自己的数据治理与质量提升之旅。推荐收藏，以备不时之需"
# #     audio_data = b""
# #     async for chunk in TTS.tts_stream(text):
# #         audio_data += chunk
# #     await play(AudioSegment.from_mp3(io.BytesIO(audio_data)))

# # def play_audio_data()

# if __name__ == "__main__":
#     text = "本文不仅系统性地概述了数据质量提升的关键步骤，还强调了每一阶段的重点与核心策略，旨在为企业提供一个清晰、可行的数据治理路径。希望每一位读者都能从中获得灵感，开启属于自己的数据治理与质量提升之旅。推荐收藏，以备不时之需"
#     audio_generator=TTS.tts_stream(text)
#     audio_data = io.BytesIO(b''.join(audio_generator))
#     # asyncio.run(play_audio_data())

from chat2llm import TTS
import time

def text_steam():
    """创建一个实时流文本"""
    text = "本文不仅系统性地概述了数据质量提升的关键步骤，还强调了每一阶段的重点与核心策略，旨在为企业提供一个清晰、可行的数据治理路径。希望每一位读者都能从中获得灵感，开启属于自己的数据治理与质量提升之旅。推荐收藏，以备不时之需"
    for i in text:
        time.sleep(0.5)
        yield i

def deal_text(text):
    for text_chunk in text:

        if text_chunk:
            pass

