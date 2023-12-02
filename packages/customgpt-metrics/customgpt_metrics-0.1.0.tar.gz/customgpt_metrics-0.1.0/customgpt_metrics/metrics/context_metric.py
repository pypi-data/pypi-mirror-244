from .base_metric import BaseMetric
from .utils.schemas import context_schema
from .utils.prompts import context_prompt
from .model_provider import model_provider
import json

class ContextMetric(BaseMetric):
    key = 'context' 

    def __init__(self, api_key, base_url, model_provider):
        self.api_key = api_key
        self.base_url = base_url 
        self.model = model_provider

    def evaluate(self, chat):
        system_message = context_prompt

        conversation = f"context:\n {chat.ai_query}\n " \
                       f"user-query:\n {chat.user_query}\n" \
                       f"bot-response:\n {chat.ai_response}\n"

        messages = [
            {"role": "user", "content": system_message},
            {"role": "user", "content": conversation},
        ]

        functions = [{"name": "context_schema", "parameters": context_schema}]
        function_call = {"name": "context_schema"}

        try:
            chat_response = model_provider.chat_completion(api_key=self.api_key,
                                                           base_url=self.base_url,
                                                           model_provider=self.model,
                                                           messages=messages,
                                                           functions=functions,
                                                           function_call=function_call,
                                                           temperature=0,
                                                           max_tokens=256,
                                                           top_p=1,
                                                           frequency_penalty=0.0,
                                                           presence_penalty=0.0)
            function_response = chat_response.choices[0].message.function_call.arguments

            parsed_response = json.loads(function_response)

            return parsed_response['context_check']

        except Exception as e:
            raise e

