import tiktoken

def calculate_total_token_count(existing_tokens, total_tokens):
    if int(total_tokens) > 0:
        token_utilized = existing_tokens + total_tokens
    else:
        token_utilized = 0
    return token_utilized


def get_token_count(text: str):
    enc = tiktoken.get_encoding("o200k_base")
    enc_text = enc.encode(text)
    return len(enc_text)
