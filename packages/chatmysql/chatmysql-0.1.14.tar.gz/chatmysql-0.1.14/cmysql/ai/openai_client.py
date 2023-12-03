from openai import OpenAI
import httpx
from cmysql.config import (
    OPENAI_API_KEY,
    OPENAI_PROXY,
    OPENAI_LLM_MODEL_NAME,
    OPENAI_LLM_MAX_TOKENS,
    OPENAI_EMBEDDING_MODEL_NAME,

)
from cmysql.logs import log
from cmysql.exceptions import PromptTooLong


class OpenAILLM:

    def __init__(self):
        log.info(f"PROXY: {OPENAI_PROXY}")
        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
            http_client=httpx.Client(
                proxies=OPENAI_PROXY,
            ),
            timeout=300,
        )

    def predict(self, prompt, json_format=False):
        max_prompt_length = OPENAI_LLM_MAX_TOKENS * 2
        if len(prompt) > max_prompt_length:
            raise PromptTooLong(f"Prompt is too long: {len(prompt)} > {max_prompt_length}")

        log.debug(f"LLM PROMPT: {prompt}")
        if json_format:
            kwargs = {
                "response_format": {"type": "json_object"},
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                    {"role": "user", "content": prompt}
                ],
            }
        else:
            kwargs = {
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
            }

        response = self.client.chat.completions.create(
            model=OPENAI_LLM_MODEL_NAME,
            temperature=0,
            max_tokens=OPENAI_LLM_MAX_TOKENS,
            **kwargs
        )
        output = response.choices[0].message.content
        log.debug(f"LLM OUTPUT:  {output}")
        return output

    def embedding(self, text):
        text = text.replace("\n", " ")
        return self.client.embeddings.create(
            input=[text],
            model=OPENAI_EMBEDDING_MODEL_NAME,
        ).data[0].embedding

    def embedding_batch(self, text_list):
        text_list = [text.replace("\n", " ") for text in text_list]
        log.info(f"embedding_batch: {text_list}")
        response = self.client.embeddings.create(
            input=text_list,
            model=OPENAI_EMBEDDING_MODEL_NAME,
            encoding_format="float"
        ).data
        return [data.embedding for data in response]


openai_llm = OpenAILLM()
