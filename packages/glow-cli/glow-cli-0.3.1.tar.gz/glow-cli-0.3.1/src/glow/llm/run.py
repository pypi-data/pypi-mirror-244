from typing import Any, Dict, Optional

from glow.colors import cprint
from glow.configs import GLOW_CONFIGS
from glow.llm.openai import build_openai_llm
from glow.llm.anthropic import build_anthropic_llm


def run_llm(question: str, system_content: Optional[str] = None) -> None:
    llm_provider = GLOW_CONFIGS["GLOW_LLM"]

    if llm_provider == "openai":
        model = build_openai_llm()
    elif llm_provider == "anthropic":
        model = build_anthropic_llm()
    else:
        cprint(f"llm provider {llm_provider} not supported for now", "yellow")
        return
    if hasattr(model, "stream"):
        try:
            for token in model.stream(
                question,
                system=system_content,
            ):
                print(token, end="")
        except KeyboardInterrupt:
            cprint("\n=========== generation interrupted by user ===========", "yellow")
        except Exception as e:
            raise e
    else:
        print(model(question, system=system_content))
