from dataclasses import dataclass
from enum import Enum

@dataclass
class Prompt:
    sys_prompt: str
    usr_prompt: str


class Model(Enum):
    GROK = "grok-4-0709"
    GPT = "gpt-4o-mini"