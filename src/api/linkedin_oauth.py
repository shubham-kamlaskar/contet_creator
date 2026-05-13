import os
import secrets
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv
from flask import Flask, redirect, request, session, url_for, render_template_string

load_dotenv()

LINKEDIN_CLIENT_ID = os.getenv('LINKEDIN_CLIENT_ID')
LINKEDIN_CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET')
REDIRECT_URI = os.getenv('LINKEDIN_REDIRECT_URI', 'http://localhost:5000/callback')
SCOPES = ['openid', 'profile', 'email', 'w_member_social']

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', secrets.token_urlsafe(32))

AUTH_URL = 'https://www.linkedin.com/oauth/v2/authorization'
TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'

HOME_PAGE = '''
<!doctype html>
<title>LinkedIn OAuth Helper</title>
<h1>LinkedIn OAuth Helper</h1>
<p>Use this page to generate an access token for LinkedIn API calls.</p>
<ul>
  <li><a href="{{ login_url }}">Sign in with LinkedIn</a></li>
</ul>
<p>After authorization, LinkedIn will redirect back here and display your access token.</p>
'''

@app.route('/')
def index():
    if not LINKEDIN_CLIENT_ID or not LINKEDIN_CLIENT_SECRET:
        return (
            '<h2>Missing LinkedIn credentials</h2>'
            '<p>Set <code>LINKEDIN_CLIENT_ID</code> and <code>LINKEDIN_CLIENT_SECRET</code> in a .env file or environment variables.</p>'
        )

    state = secrets.token_urlsafe(16)
    session['oauth_state'] = state

    params = {
        'response_type': 'code',
        'client_id': LINKEDIN_CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': ' '.join(SCOPES),
        'state': state,
    }

    login_url = f"{AUTH_URL}?{urlencode(params)}"
    return render_template_string(HOME_PAGE, login_url=login_url)

@app.route('/callback')
def callback():
    error = request.args.get('error')
    if error:
        return f'<h2>Authorization error</h2><p>{error}</p>', 400

    code = request.args.get('code')
    state = request.args.get('state')
    saved_state = session.pop('oauth_state', None)

    if not code or not state or state != saved_state:
        return '<h2>Invalid authorization response</h2>', 400

    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': LINKEDIN_CLIENT_ID,
        'client_secret': LINKEDIN_CLIENT_SECRET,
    }

    response = requests.post(TOKEN_URL, data=token_data)
    response.raise_for_status()
    token_response = response.json()
    access_token = token_response.get('access_token')
    expires_in = token_response.get('expires_in')

    return (
        f'<h2>LinkedIn Access Token</h2>'
        f'<p><strong>access_token</strong>: <code>{access_token}</code></p>'
        f'<p><strong>expires_in</strong>: {expires_in} seconds</p>'
        '<p>Copy this token into your LinkedInAPI initialization.</p>'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
