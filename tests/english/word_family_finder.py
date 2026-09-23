from langchain_core.messages import HumanMessage

from playground.utils.openai_runner import llm_invoke


@llm_invoke
def find_word_family(word: str):
    return [HumanMessage(f"Xác định word family của từ sau: {word}")]
