import os
import llm
from llm.default_plugins.openai_models import Chat

MODELS = (
    "meta-llama--Llama-2-7b-chat-hf",
    "autonomi-ai--Llama-2-7b-chat-hf",
)


class NOSRunChat(Chat):
    needs_key = "nosrun"

    def __str__(self):
        return "NOSRun: {}".format(self.model_id)


@llm.hookimpl
def register_models(register):
    # Only do this if the key is set
    key = llm.get_key("", "nosrun", "LLM_NOSRUN_KEY")
    if not key:
        return
    for model_id in MODELS:
        register(
            NOSRunChat(
                model_id=model_id,
                model_name=model_id,
                api_base=os.getenv("NOSRUN_API_BASE" ,"https://llama2.nos.run/v1"),
            )
        )
