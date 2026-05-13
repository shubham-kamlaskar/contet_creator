# LinkedIn OAuth Authentication System

A complete Python-based LinkedIn OAuth 2.0 authentication system that allows you to log in to your LinkedIn account and get access tokens for API calls.

## 🚀 Features

- ✅ Full OAuth 2.0 flow implementation
- ✅ Secure state parameter for CSRF protection
- ✅ Beautiful web interface
- ✅ Access token retrieval and storage
- ✅ Profile information display
- ✅ Ready-to-use API wrapper for LinkedIn operations
- ✅ Examples for posting, sharing, and fetching data

## 📋 Prerequisites

1. **LinkedIn Developer Account**
   - Go to [LinkedIn Developers](https://www.linkedin.com/developers/)
   - Sign in with your LinkedIn account

2. **Create a LinkedIn App**
   - Visit [LinkedIn Developer Apps](https://www.linkedin.com/developers/apps)
   - Click "Create App"
   - Fill in required details:
     - App name: Your choice
     - LinkedIn Page: Select or create one
     - App logo: Upload any image
     - Legal agreement: Accept terms

3. **Configure OAuth Settings**
   - In your app, go to the "Auth" tab
   - Under "Authorized redirect URLs", add: `http://localhost:5000/callback`
   - Under "Products", request access to:
     - Sign In with LinkedIn using OpenID Connect
     - Share on LinkedIn (for posting)

4. **Get Credentials**
   - In the "Auth" tab, copy:
     - **Client ID**
     - **Client Secret**

## 🛠️ Installation

### Step 1: Install Required Packages

```bash
pip install flask requests python-dotenv --break-system-packages
```

### Step 2: Set Up Environment Variables

Create a `.env` file in the repo root from the example:

```bash
copy .env.example .env
```

Edit `.env` and add your credentials:

```env
LINKEDIN_CLIENT_ID=your_actual_client_id
LINKEDIN_CLIENT_SECRET=your_actual_client_secret
LINKEDIN_REDIRECT_URI=http://localhost:5000/callback
FLASK_SECRET_KEY=replace_with_a_random_secret
```

## 🎯 Usage

### Method 1: Run the OAuth Server

```bash
python linkedin_oauth.py
```

Then:
1. Open your browser: `http://localhost:5000`
2. Click "Sign in with LinkedIn"
3. Authorize the app
4. You'll be redirected back with your access token

### Method 2: Use the Access Token

After getting your access token, you can use it in your scripts:

```python
from linkedin_api_usage import LinkedInAPI

# Initialize with your access token
linkedin = LinkedInAPI('your_access_token_here')

# Get profile
profile = linkedin.get_profile()
print(profile)

# Post a text update
result = linkedin.post_share("Hello LinkedIn! 🚀")
print(result)

# Post an article
linkedin.post_article(
    title="My Article Title",
    text="Check out my new article!",
    url="https://example.com/article"
)
```

## 📚 Available API Methods

### Profile Methods
```python
# Get basic profile (OpenID Connect)
profile = linkedin.get_profile()

# Get detailed profile
details = linkedin.get_profile_details()

# Get email
email = linkedin.get_email()
```

### Posting Methods
```python
# Post text update
linkedin.post_share("Your text here", visibility='PUBLIC')

# Post article with link
linkedin.post_article(
    title="Article Title",
    text="Your commentary",
    url="https://example.com"
)
```

## 🔑 Access Token Scopes

The app requests these permissions:
- `openid` - Basic authentication
- `profile` - Read profile data
- `email` - Access email address
- `w_member_social` - Post on LinkedIn

To request additional scopes, modify the `SCOPES` list in `linkedin_auth.py`:

```python
SCOPES = [
    'openid',
    'profile',
    'email',
    'w_member_social',
    # Add more scopes as needed
]
```

## 🔒 Security Notes

1. **Never commit credentials** - Use `.env` files or environment variables
2. **State parameter** - Protects against CSRF attacks
3. **HTTPS in production** - Always use HTTPS for production apps
4. **Token expiry** - Access tokens expire (default 60 days), implement refresh logic
5. **Keep secrets secret** - Never expose client secret in client-side code

## 🐛 Troubleshooting

### Error: "Redirect URI mismatch"
- Ensure `http://localhost:5000/callback` is added in LinkedIn Developer Portal
- Check that the URL matches exactly (no trailing slashes)

### Error: "Invalid client credentials"
- Double-check your Client ID and Client Secret
- Make sure there are no extra spaces

### Error: "Scope not authorized"
- Request access to required products in LinkedIn Developer Portal
- Some scopes require approval from LinkedIn

### Token Expired
- Access tokens expire after ~60 days
- Re-run the OAuth flow to get a new token
- For production, implement token refresh logic

## 📖 Official Documentation

- [LinkedIn OAuth 2.0](https://learn.microsoft.com/en-us/linkedin/shared/authentication/authentication)
- [LinkedIn API Documentation](https://learn.microsoft.com/en-us/linkedin/)
- [Share API](https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/share-on-linkedin)

## 🎓 Learning Resources

### OAuth Flow Explained:
1. **Authorization Request** - User clicks "Sign in with LinkedIn"
2. **User Consent** - User approves permissions on LinkedIn
3. **Authorization Code** - LinkedIn redirects back with a code
4. **Token Exchange** - App exchanges code for access token
5. **API Access** - Use access token to call LinkedIn APIs

### Token Storage Options:
- **Session** (current implementation) - Temporary, cleared on logout
- **Database** - For production apps with multiple users
- **Environment Variables** - For personal scripts
- **Secure Storage** - Use encryption for sensitive data

## 💡 Next Steps

1. **Implement Token Refresh** - Add logic to refresh expired tokens
2. **Add Error Handling** - Improve error messages and logging
3. **Database Integration** - Store tokens securely for multiple users
4. **Rate Limiting** - Respect LinkedIn's API rate limits
5. **Webhooks** - Listen for LinkedIn events (if available)

## 📝 License

This is a learning/demo project. Use it as a starting point for your own applications.

## 🤝 Contributing

Feel free to fork, modify, and improve this code for your needs!

## ⚠️ Disclaimer

This is an educational project. Always follow LinkedIn's API Terms of Service and rate limits. Do not spam or violate LinkedIn's policies.

---

**Made with ❤️ for learning LinkedIn OAuth**