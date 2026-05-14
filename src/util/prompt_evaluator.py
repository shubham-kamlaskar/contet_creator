token_utilized = 0
def calculate_total_token_count(existing_tokens: int, total_tokens: int):
    if total_tokens > 0:
        token_utilized = existing_tokens + total_tokens
        return token_utilized