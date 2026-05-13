import requests
import os
from dotenv import load_dotenv

load_dotenv()

def generate_access_token_from_linkedin():
    url = "https://www.linkedin.com/oauth/v2/accessToken"
    payload = {
        "grant_type": "authorization_code",
        "code": "CODE_FROM_STEP_3",
        "redirect_uri": os.getenv("OAUTH2_REDIRECT_URL"),
        "client_id": os.getenv("LINKEDIN_CLIENT_ID"),
        "client_secret": os.getenv("LINKEDIN_CLIENT_SECRET"),
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(url, data=payload, headers=headers)
    token_data = response.json()
    print(token_data)
    # Your valid API token
    #access_token = token_data["access_token"]
    return token_data

if __name__ == "__main__":
    print(generate_access_token_from_linkedin())