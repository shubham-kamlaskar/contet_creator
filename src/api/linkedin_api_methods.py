"""
LinkedIn API Usage Examples
Use this script after getting your access token from the OAuth flow
"""

import requests
import json
import os
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()


class LinkedInAPI:
    """Simple LinkedIn API wrapper"""
    
    def __init__(self):
        self.linkedin_version = os.getenv("LINKEDIN_API_VERSION", "202605")
        self.access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
        self.base_url = 'https://api.linkedin.com'
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0',
            'LinkedIn-Version': self.linkedin_version
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
        author_urn = f"urn:li:person:{profile['sub']}"
        
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
    
    def like_the_post(self, post_urn, reaction_type):
        """Like reaction on a linkedin post given its post URN"""
        profile = self.get_profile()
        author_urn = f"urn:li:person:{profile['sub']}"
        
        post_data = {
            "actor": author_urn,
            "reactionType": reaction_type.upper(),
            "root": f"urn:li:activity:{post_urn}"
            }
        
        # Correct endpoint for likes/reactions
        url = f"{self.base_url}/rest/reactions"
        
        response = requests.post(url, headers=self.headers, json=post_data)
        # A successful creation returns status 201 with no body
        if response.status_code == 201:
            return {"status": "success", "message": "Post liked successfully"}
            
        return {
        "status_code": response.status_code,
        "response": response.text
    }

    def comment_on_post(self, post_urn, comment_text):
        """
        Comment on a post given its URN (e.g., 'urn:li:share:12345').
        To reply to a comment, pass the comment URN to 'post_urn'.
        """
        profile = self.get_profile()
        author_urn = f"urn:li:person:{profile['sub']}"
        
        encoded_urn = quote(post_urn, safe='')
        
        post_data = {
            "actor": author_urn,
            "message": {
                "text": comment_text
            },
            "object": post_urn  # Target post or parent comment URN
        }
        
        # Correct endpoint for social actions (comments)
        url = f"{self.base_url}/rest/socialActions/{encoded_urn}/comments"
        
        response = requests.post(url, headers=self.headers, json=post_data)
        
        # A successful comment creation returns HTTP 201
        if response.status_code == 201:
            return {"status": "success", "message": "Comment posted successfully"}
            
        return {
        "status_code": response.status_code,
        "response": response.text
    }
