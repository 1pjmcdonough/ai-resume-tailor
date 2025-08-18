from dataclasses import dataclass

@dataclass
class Prompt:
    sys_prompt: str
    usr_prompt: str