from haystack_integrations.components.generators.ollama import OllamaChatGenerator
from haystack.components.generators.utils import print_streaming_chunk


def Ollama(
    model: str = "llama3.1",
    url: str = "http://192.168.30.66:11434/api/chat",
    is_streaming: bool = False,
    token_length: int = 512,
):

    def streaming_callback(chunk):
        yield chunk.content

    if is_streaming:
        llm = OllamaChatGenerator(
            model=model,
            url=url,
            generation_kwargs={
                "num_predict": token_length,
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
                "num_predict": token_length,
                "temperature": 0.4,
            },
        )

    return llm
