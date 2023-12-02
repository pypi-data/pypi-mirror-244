from .types.log_entry import LogEntry

class OpenTelemetryAdapter:
    def adapt_log_entry(self, log_entry):
        user_query = log_entry.get('user_query')
        ai_query = log_entry.get('ai_query')
        ai_response = log_entry.get('ai_response')
        adapted_entry = LogEntry(user_query, ai_query, ai_response)
        return adapted_entry
