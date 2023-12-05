from glow.colors import cprint
from glow.configs import GLOW_CONFIGS
from glow.secrets import GLOW_SECRETS
from important.llmsdk.openai import ChatOpenAI


def build_openai_llm() -> ChatOpenAI:
    OPENAI_API_KEY = GLOW_SECRETS["OPENAI_API_KEY"]
    OPENAI_MODEL = GLOW_CONFIGS["OPENAI_MODEL"]
    llm = ChatOpenAI(
        model_name=OPENAI_MODEL,
        api_key=OPENAI_API_KEY,
    )
    return llm
