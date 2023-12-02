import openai
from .model_strategy import ModelStrategy


class OpenAIStrategy(ModelStrategy):
    def __init__(self, api_key, base_url):
        self.default_openai = openai
        self.default_openai.api_key = api_key
        self.default_openai.api_base = base_url
        self.default_openai.api_type = "open_ai"
        self.default_openai.api_version = None

    def chat_completion(self,
                        model,
                        messages,
                        **completion_api_params):

        if not model:
            model = "gpt-3.5-turbo-16k-0613"
        main_model = model
        try:
            return self.default_openai.ChatCompletion.create(model=main_model,
                                                             messages=messages,
                                                             **completion_api_params)
        except Exception as e:
            raise e
