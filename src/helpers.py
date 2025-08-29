from dataclasses import dataclass
from enum import Enum

from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv
import os

dotenv_path = Path( Path(__file__).parent.parent, ".env" )
load_dotenv(dotenv_path=dotenv_path)


@dataclass
class Prompt:
    sys_prompt: str
    usr_prompt: str


@dataclass
class UserInfo:
    resume: str
    job_desc: str
    model: str
    usr_context: str


class Model(Enum):
    GROK4 = "grok-4-0709"
    GPT4o = "gpt-4o-mini"


def set_client(model: str) -> OpenAI:
    if model == Model.GROK4.value:
        return OpenAI(
            api_key=os.getenv("XAI_API_KEY"),
            base_url="https://api.x.ai/v1"
        )
    elif model == Model.GPT4o.value:
        return OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url="https://api.openai.com/v1"
        )
    else:
        raise ValueError(f"Model {model} not supported")