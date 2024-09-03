from haystack_integrations.components.generators.ollama import OllamaChatGenerator
from haystack.components.generators.utils import print_streaming_chunk


def Ollama(
    model: str = "llama3",
    url: str = "http://192.168.30.66:11434/api/chat",
    is_streaming: bool = False,
):

    def streaming_callback(chunk):
        yield chunk.content

    if is_streaming:
        llm = OllamaChatGenerator(
            model=model,
            url=url,
            generation_kwargs={
                "num_predict": 256,
                "temperature": 0.4,
            },
            streaming_callback=lambda chunk: print(chunk.content, flush=True, end=""),
            # streaming_callback=lambda  chunk: streaming_callback(chunk),
            
        )
    else:
        llm = OllamaChatGenerator(
            model=model,
            url=url,
            generation_kwargs={
                "num_predict": 256,
                "temperature": 0.4,
            },
        )

    return llm
