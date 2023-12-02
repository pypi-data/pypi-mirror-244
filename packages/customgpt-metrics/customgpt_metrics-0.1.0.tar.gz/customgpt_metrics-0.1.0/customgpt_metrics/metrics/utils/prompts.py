language_prompt = "You are an expert AI language interpreter. Please analyze the message below delimited by $$$ " \
									"and output the detected language. STRICTLY Output ONLY the ISO code of the language."

intent_prompt = "Given a user message and response, analyze the user-query and categorize the intent for the " \
								"user-query as Informational, Navigational, Greetings, Follow-up, Transactional, Troubleshooting " \
								"and Instructional. Use the bot-response as a reference for better undersrtanding."

emotion_prompt = "Given a user message and response, analyze the user-query and categorize it strictly as " \
                 "one of the five sentiments: positive, neutral, confusion, dissatisfaction or frustration. " \
                 "Use the tone and intent of the user-query too."

context_prompt = "You are an AI conversation assistant. You are provided with a conversation containing the " \
                 "context used to answer the query, user-query and the bot-response. Your goal is to detect " \
                 "whether the bot was directly able to answer, by understanding the tone and intent of the " \
                 "response.\nIf: the bot is unable to answer, return Out-of-context, Else: return In-context"