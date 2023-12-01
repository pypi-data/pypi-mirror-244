"""
A simple wrapper for the official ChatGPT API
"""
import argparse
import json
import os
import sys
from importlib.resources import path
from pathlib import Path
from typing import AsyncGenerator
from typing import NoReturn

import httpx
import openai
import requests
import tiktoken

from . import __version__
from . import typings as t
from .utils import create_completer
from .utils import create_keybindings
from .utils import create_session
from .utils import get_filtered_keys_from_object
from .utils import get_input
from openai import OpenAIError, APIError


class Chatbot:
    """
    Official ChatGPT API
    """

    def __init__(
        self,
        max_reply=500,
        api_key: str='',
        engine: str = "gpt-3.5-turbo-0613",
        proxy: str = None,
        timeout: float = None,
        max_tokens: int = None,
        temperature: float = 0.5,
        top_p: float = 1.0,
        presence_penalty: float = 0.0,
        frequency_penalty: float = 0.0,
        reply_count: int = 1,
        truncate_limit: int = None,
        sysprompt_for_hints:str="You are a question generator. Your objective is to generate three questions that the user might find intriguing, based on their previous inquiries and the most recent response from the system. Questions can be extensions of previous ones, but they must not be repetitive.",
        system_prompt: str = "You are ChatGPT, a large language model trained by OpenAI. Respond conversationally",

    ) -> None:
        """
        Initialize Chatbot with API key (from https://platform.openai.com/account/api-keys)
                    "gpt-3.5-turbo-0613",
            "gpt-3.5-turbo-16k-0613",
        """

        self.engine: str = engine

        self.max_reply: int=max_reply
        self.system_prompt: str = system_prompt
        self.sysprompt_for_hints=sysprompt_for_hints
        self.max_tokens: int = max_tokens or (
            31000 if engine=="gpt-4-32k" or engine =="gpt-4-1106-preview" else 7000 if engine == "gpt-4" else 15500 if engine=="gpt-3.5-turbo-1106" or engine=="gpt-3.5-turbo-16k-0613" else 4000
        )
        self.truncate_limit: int = truncate_limit or (
            30500 if engine =="gpt-4-32k" or engine=="gpt-4-1106-preview" else 6500 if engine == "gpt-4" else 15250 if engine=="gpt-3.5-turbo-1106" or engine=="gpt-3.5-turbo-16k-0613" else 3500
        )
        self.temperature: float = temperature

        self.top_p: float = top_p
        self.presence_penalty: float = presence_penalty
        self.frequency_penalty: float = frequency_penalty
        self.reply_count: int = reply_count
        self.api_key: str = api_key
        openai.api_key = api_key
        self.timeout: float = timeout
        openai.api_timeout = timeout  # 设置全局的超时时间
        self.proxy = proxy
        self.session = requests.Session()
        self.session.proxies.update(
            {
                "http": proxy,
                "https": proxy,
            },
        )
        if proxy := (
            proxy or os.environ.get("all_proxy") or os.environ.get("ALL_PROXY") or None
        ):
            if "socks5h" not in proxy:
                self.aclient = httpx.AsyncClient(
                    follow_redirects=True,
                    proxies=proxy,
                    timeout=timeout,
                )
        else:
            self.aclient = httpx.AsyncClient(
                follow_redirects=True,
                proxies=proxy,
                timeout=timeout,
            )

        self.conversation: dict[str, list[dict]] = {
            "default": [
                {
                    "role": "system",
                    "content": system_prompt,
                },
            ],
        }
        self.questions: dict[str, list[dict]]={
            "default": [
                {
                    "role": "system",
                    "content": sysprompt_for_hints,
                },
            ],
        }

        if self.get_token_count("default") > self.max_tokens:
            raise t.ActionRefuseError("System prompt is too long")

    def add_to_conversation(
        self,
        message: str,
        role: str,
        convo_id: str = "default",
    ) -> None:
        """
        Add a message to the conversation
        """
        if convo_id not in self.conversation:
            self.reset(convo_id=convo_id, system_prompt=self.system_prompt)
        self.conversation[convo_id].append({"role": role, "content": message})

    def __truncate_conversation(self, convo_id: str = "default",count_prompts: int=0) -> None:
        """
        Truncate the conversation
        """
        while True:
            if (
                self.get_token_count(convo_id) > self.truncate_limit
                and len(self.conversation[convo_id]) > 1
            ):
                # Don't remove the first message
                self.conversation[convo_id].pop(1+count_prompts)
            else:
                break
    def truncate_conversation(self, convo_id: str = "default",count_prompts: int=0) -> None:
        """
        Truncate the conversation
        """
        try:
            self.conversation[convo_id].pop(1+int(count_prompts))
            self.conversation[convo_id].pop(1+int(count_prompts))
        except:
            pass
    # https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
    def get_token_count(self, convo_id: str = "default") -> int:
        """
        Get token count
        """
        if self.engine not in [
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-0301",
            "gpt-3.5-turbo-0613",
            "gpt-3.5-turbo-16k-0613",
            "gpt-4",
            "gpt-4-0314",
            "gpt-4-32k",
            "gpt-4-32k-0314",
            "gpt-4-1106-preview",
            "gpt-3.5-turbo-1106"
        ]:
            raise NotImplementedError(f"Unsupported engine {self.engine}")

        tiktoken.model.MODEL_TO_ENCODING["gpt-4"] = "cl100k_base"

        encoding = tiktoken.encoding_for_model(self.engine)

        num_tokens = 0
        for message in self.conversation[convo_id]:
            # every message follows <im_start>{role/name}\n{content}<im_end>\n
            num_tokens += 5
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += 5  # role is always required and always 1 token
        num_tokens += 5  # every reply is primed with <im_start>assistant
        return num_tokens

    def get_max_tokens(self, convo_id: str) -> int:
        """
        Get max tokens
        """
        # return self.max_reply
        return self.max_tokens - self.get_token_count(convo_id)
    def get_question_hints_old(self,prompts):
        # Get response
        response = self.session.post(
            os.environ.get("API_URL") or "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": "gpt-3.5-turbo-0613",
                # "model": self.engine,
                "messages": prompts,
                "stream": False,
                "temperature":self.temperature,
                "top_p": self.top_p,
                "presence_penalty": self.presence_penalty,
                "frequency_penalty":self.frequency_penalty,
                "n": 1,
                "user": "system",
                "max_tokens": 200,
            },
            timeout=self.timeout,
            stream=False,
        )
        if response.status_code != 200:
            raise t.APIConnectionError(
                f"{response.status_code} {response.reason} {response.text}",
            )
        json_response = response.json()
        return json_response["choices"][0]["message"]["content"]

    def get_question_hints(self, prompts):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-1106",  # 模型名称
                messages=prompts,  # 提示信息
                n=1,  # 生成的独立输出的数量
                max_tokens=200,  # 生成的文本的最大长度
                temperature=self.temperature,  # 控制输出的随机性
                top_p=self.top_p,  # 采样过程中，模型将仅考虑累积概率大于此值的词汇
                frequency_penalty=self.frequency_penalty,  # 用于惩罚或奖励常见的词汇
                presence_penalty=self.presence_penalty,  # 用于惩罚或奖励新出现的词汇
            )
        except (OpenAIError, APIError) as e:
            print(f"Error: {e}")
            return

        # 获取生成的文本
        generated_text = response['choices'][0]['message']['content']

        return generated_text

    async def ask_stream_async(
        self,
        prompt: str,
        role: str = "user",
        convo_id: str = "default",
        count_prompts: int=0,
        **kwargs,
    ) -> AsyncGenerator[str, None]:
        """
        Ask a question
        """
        # Make conversation if it doesn't exist
        if convo_id not in self.conversation:
            self.reset(convo_id=convo_id, system_prompt=self.system_prompt)
        self.add_to_conversation(prompt, "user", convo_id=convo_id)
        # Get response
        async with self.aclient.stream(
            "post",
            os.environ.get("API_URL") or "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {kwargs.get('api_key', self.api_key)}"},
            json={
                "model": self.engine,
                "messages": self.conversation[convo_id],
                "stream": True,
                # kwargs
                "temperature": kwargs.get("temperature", self.temperature),
                "top_p": kwargs.get("top_p", self.top_p),
                "presence_penalty": kwargs.get(
                    "presence_penalty",
                    self.presence_penalty,
                ),
                "frequency_penalty": kwargs.get(
                    "frequency_penalty",
                    self.frequency_penalty,
                ),
                "n": kwargs.get("n", self.reply_count),
                "user": role,
                "max_tokens": self.get_max_tokens(convo_id=convo_id),
            },
            timeout=kwargs.get("timeout", self.timeout),
        ) as response:
            # if response.status_code != 200:
            #     await response.aread()
            #     raise f"{response.status_code} {response.reason_phrase} {response.text}"
            #     # raise t.APIConnectionError(
            #     #     f"{response.status_code} {response.reason_phrase} {response.text}",
            #     # )
            if response.is_error:
                await response.aread()
                raise Exception(f"{response.status_code} {response.reason_phrase} {response.text}")
            response_role: str = ""
            full_response: str = ""

            async for line in response.aiter_lines():

                line = line.strip()
                if not line:
                    continue
                # Remove "data: "
                line = line[6:]
                if line == "[DONE]":
                    break
                resp: dict = json.loads(line)
                choices = resp.get("choices")
                if not choices:
                    continue
                delta: dict[str, str] = choices[0].get("delta")
                if not delta:
                    continue
                if "role" in delta:
                    response_role = delta["role"]
                if "content" in delta:
                    content: str = delta["content"]
                    full_response += content
                    yield content
        self.add_to_conversation(full_response, response_role, convo_id=convo_id)

    async def ask_stream_async_new(
            self,
            prompt: str,
            role: str = "user",
            convo_id: str = "default",
            **kwargs,
    ) -> AsyncGenerator[str, None]:
        """
        Ask a question
        """
        # Make conversation if it doesn't exist
        if convo_id not in self.conversation:
            self.reset(convo_id=convo_id, system_prompt=self.system_prompt)
        self.add_to_conversation(prompt, "user", convo_id=convo_id)

        # Get response
        try:
            response = await openai.ChatCompletion.create(
                model=self.engine,
                messages=self.conversation[convo_id],
                stream=True,
                temperature=kwargs.get("temperature", self.temperature),
                top_p=kwargs.get("top_p", self.top_p),
                presence_penalty=kwargs.get("presence_penalty", self.presence_penalty),
                frequency_penalty=kwargs.get("frequency_penalty", self.frequency_penalty),
                n=kwargs.get("n", self.reply_count),
                user=role,
                max_tokens=self.get_max_tokens(convo_id=convo_id),
            )
            print(response)
        except (OpenAIError, APIError) as e:
            print(f"Error: {e}")
            return

        response_role: str = ""
        full_response: str = ""

        async for line in response.aiter_lines():
            line = line.strip()
            if not line:
                continue
            # Remove "data: "
            line = line[6:]
            if line == "[DONE]":
                break
            resp: dict = json.loads(line)
            choices = resp.get("choices")
            if not choices:
                continue
            delta: dict[str, str] = choices[0].get("delta")
            if not delta:
                continue
            if "role" in delta:
                response_role = delta["role"]
            if "content" in delta:
                content: str = delta["content"]
                full_response += content
                yield content
        self.add_to_conversation(full_response, response_role, convo_id=convo_id)

    def rollback(self, n: int = 1, convo_id: str = "default") -> None:
        """
        Rollback the conversation
        """
        for _ in range(n):
            self.conversation[convo_id].pop()

    def reset(self, convo_id: str = "default", system_prompt: str = None) -> None:
        """
        Reset the conversation
        """
        self.conversation[convo_id] = [
            {"role": "system", "content": system_prompt or self.system_prompt},
        ]
        self.questions[convo_id] = [
            {"role": "system", "content": self.sysprompt_for_hints},
        ]

    def save(self, file: str, *keys: str) -> None:
        """
        Save the Chatbot configuration to a JSON file
        """
        with open(file, "w", encoding="utf-8") as f:
            data = {
                key: self.__dict__[key]
                for key in get_filtered_keys_from_object(self, *keys)
            }
            # saves session.proxies dict as session
            # leave this here for compatibility
            data["session"] = data["proxy"]
            del data["aclient"]
            json.dump(
                data,
                f,
                indent=2,
            )

    def load(self, file: Path, *keys_: str) -> None:
        """
        Load the Chatbot configuration from a JSON file
        """
        with open(file, encoding="utf-8") as f:
            # load json, if session is in keys, load proxies
            loaded_config = json.load(f)
            keys = get_filtered_keys_from_object(self, *keys_)

            if (
                "session" in keys
                and loaded_config["session"]
                or "proxy" in keys
                and loaded_config["proxy"]
            ):
                self.proxy = loaded_config.get("session", loaded_config["proxy"])
                self.session = httpx.Client(
                    follow_redirects=True,
                    proxies=self.proxy,
                    timeout=self.timeout,
                    cookies=self.session.cookies,
                    headers=self.session.headers,
                )
                self.aclient = httpx.AsyncClient(
                    follow_redirects=True,
                    proxies=self.proxy,
                    timeout=self.timeout,
                    cookies=self.session.cookies,
                    headers=self.session.headers,
                )
            if "session" in keys:
                keys.remove("session")
            if "aclient" in keys:
                keys.remove("aclient")
            self.__dict__.update({key: loaded_config[key] for key in keys})

