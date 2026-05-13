"""
LinkedIn API Usage Examples
Use this script after getting your access token from the OAuth flow
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


class LinkedInAPI:
    """Simple LinkedIn API wrapper"""
    
    def __init__(self):
        self.access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
        self.base_url = 'https://api.linkedin.com'
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }
    
    def get_profile(self):
        """Get basic profile information"""
        url = f"{self.base_url}/v2/userinfo"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def get_profile_details(self):
        """Get detailed profile information"""
        url = f"{self.base_url}/v2/userinfo"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    # def get_email(self):
    #     """Get primary email address"""
    #     url = f"{self.base_url}/v2/emailAddress?q=members&projection=(elements*(handle~))"
    #     response = requests.get(url, headers=self.headers)
    #     return response.json()
    
    def post_share(self, text, visibility='PUBLIC'):
        """
        Post a text share on LinkedIn
        
        Args:
            text: Content to post
            visibility: PUBLIC or CONNECTIONS
        """
        profile = self.get_profile()
        author_urn = f"urn:li:person:{profile['sub']}"
        
        post_data = {
            "author": author_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": visibility
            }
        }
        
        url = f"{self.base_url}/v2/ugcPosts"
        response = requests.post(url, headers=self.headers, json=post_data)
        return response.json()
    
    def post_article(self, title, text, url=None):
        """
        Post an article share on LinkedIn
        
        Args:
            title: Article title
            text: Post text/commentary
            url: Article URL (optional)
        """
        profile = self.get_profile_details()
        author_urn = f"urn:li:person:{profile['id']}"
        
        post_data = {
            "author": author_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "ARTICLE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        if url:
            post_data["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = [{
                "status": "READY",
                "description": {
                    "text": title
                },
                "originalUrl": url,
                "title": {
                    "text": title
                }
            }]
        
        url = f"{self.base_url}/v2/ugcPosts"
        response = requests.post(url, headers=self.headers, json=post_data)
        return response.json()
