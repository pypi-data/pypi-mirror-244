from .base_metric import BaseMetric
from .utils.schemas import intent_schema
from .utils.prompts import intent_prompt
from .model_provider import model_provider
import json

class IntentMetric(BaseMetric):
    key = 'intent'
    def __init__(self, api_key, base_url, model_provider='openai'):
        self.api_key = api_key
        self.base_url = base_url 
        self.model = model_provider

    def evaluate(self, chat, model='openai'):
        system_message = intent_prompt
        conversation = f"user-query:\n{chat.user_query}\nbot-response:\n{chat.ai_response}"

        messages = [
            {"role": "user", "content": system_message},
            {"role": "user", "content": conversation},
        ]

        functions = [{"name": "intent_schema", "parameters": intent_schema}]
        function_call = {"name": "intent_schema"}

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

            return parsed_response['intent_check']

        except Exception as e:
            return e
