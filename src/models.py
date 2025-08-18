from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv
import os

dotenv_path = Path( Path(__file__).parent.parent, ".env" )
load_dotenv(dotenv_path=dotenv_path)


def get_client(model: str):
    if model == "grok-4-0709":
        return OpenAI(
            api_key=os.getenv("XAI_API_KEY"),
            base_url="https://api.x.ai/v1"
        )
    elif model == "gpt-4o-mini":
        return OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url="https://api.openai.com/v1"
        )
    else:
        raise ValueError(f"Model {model} not supported")