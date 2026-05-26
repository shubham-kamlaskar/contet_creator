from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.tools.playwright.utils import create_sync_playwright_browser
from typing import Optional

from src.tools.tool_classes import (InternetSearch, LatestAINews, FetchLinkedinMetadata, PostContentOnLinkedin, 
                                    UpdateContentInDocument, PostWriterInput, GenerateThoughtfulCommentOnPost, 
                                    ViralTopicSuggestions, LikeOnLinkedinPost, CommentOnLinkedinPost)
from src.agents.ollama_llm_provider import LLMProvider
from src.api.linkedin_api_methods import LinkedInAPI
from src.util.log_adapter import logger


def get_llm_provider():
    return LLMProvider()

def get_linkedin_api():
    return LinkedInAPI()


@tool("internet_search", args_schema=InternetSearch)
def internet_search(requirements: str):
    """This tool is useful to fetch any type of information from internet,when user needs real time or latest information."""
    try:
        search = DuckDuckGoSearchResults(output_format="json", num_results=3)
        content = search.invoke(requirements)
        return content
    except Exception as e:
        logger.error(f"An error occured during 'internet_search' tool: {str(e)}")
        return {"result": "An error occured, please try again"}

   
@tool("latest_ai_news", args_schema=LatestAINews)
def latest_ai_news(information: str):
    """This tool is useful to fetch latest news related to the world of AI and related stuffs based on the timeline provided by user."""
    try:
        search = DuckDuckGoSearchResults(backend="news", output_format='json', num_results=5)
        content = search.invoke(information)
        return {"result": content}
    except Exception as e:
        logger.error(f"An error occured during 'latest_ai_news' tool: {str(e)}")
        return {"result": "An error occured, please try again"}

@tool("fetch_linkedin_metadata", args_schema=FetchLinkedinMetadata)
def fetch_linkedin_metadata(user_query: str):
    """This tool is used to fetch information of linkedin user account."""
    try:
        profile_details = get_linkedin_api().get_profile_details()
        return {"result": profile_details}
    except Exception as e:
        logger.error(f"An error occured during 'fetch_linkedin_metadata' tool: {str(e)}")
        return {"result": "An error occured, please try again"}


@tool("post_content_on_linkedin", args_schema=PostContentOnLinkedin)
def post_content_on_linkedin(content: str):
    """This tool is used to post the content created based on user requirements on user linkedin account.
    Strictly do not post the content if not requested to do so."""
    try:
        get_linkedin_api().post_share(text=content)
        return {"result": "Post successfully posted on your Linkedin profile."}
    except Exception as e:
        logger.error(f"An error occured during 'post_content_on_linkedin' tool: {str(e)}")
        return {"result": "An error occured, please try again"}


def create_document(file_name: str, content: str):
    with open(f"generated_docs/{file_name}", "w", encoding="utf-8") as file:
        file.write(f"{content}")
        

@tool('update_content_in_document', args_schema=UpdateContentInDocument)
def update_content_in_document(content: str, file_name: str):
    """This tool is used to create a .txt document, when a user specifically mention to create a document. 
    Strictly do not create a document if not requested to do so."""
    try:
        create_document(file_name, content)
        return {"result": f"A file is created with name {file_name}, as per your request."}
    except Exception as e:
        logger.error(f"An error occured during 'update_content_in_document' tool: {str(e)}")
        return {"result": "An error occured, please try again"}


@tool("post_writer", args_schema=PostWriterInput)
def post_writer(tone: Optional[str] = None, pitch: Optional[str] = None, content: str = "") -> dict:
    """Generate or refine a social media post using the provided tone, pitch, and content."""
    try:
        return {"status": "success", "tone": tone, "pitch": pitch, "result": content.strip()}

    except Exception as e:
        logger.exception("Error occurred in 'post_writer' tool")

        return {"status": "error", "message": f"Failed to generate post: {str(e)}"
        }  

@tool('generate_thoughtful_comment_on_post', args_schema=GenerateThoughtfulCommentOnPost)
def generate_thoughtful_comment_on_post(comment: str):
    """This tool is used to generate a thoughtfull comment based on the linkedin post or article to get higher attensions from peers.
    First understand the post throughly then generate a comment.
    Sometime the post may or may not related to the field of AI but we need to write a comment there."""
    try:
        return {"result": comment}
    except Exception as e:
        logger.error(f"An error occured during 'generate_thoughtful_comment_on_post' tool: {str(e)}")
        return {"result": "An error occured, please try again"}


@tool('viral_topic_suggestions', args_schema=ViralTopicSuggestions)
def viral_topic_suggestions(topics: list):
    """This tools is used to generate trending, viral topics from AI domain on internet, reddit, linkedin and other similar platforms."""
    try:
        return {"result": topics}
    except Exception as e:
        logger.error(f"An error occured during 'viral_topic_suggestions' tool: {str(e)}")
        return {"result": "An error occured, please try again"}
    
@tool('like_on_linkedin_post', args_schema=LikeOnLinkedinPost)
def like_on_linkedin_post(post_urn: str, reaction_type: str):
    """This tool is used to give a like reaction on a linkedin post given the post urn."""
    try:
        get_linkedin_api().like_the_post(post_urn, reaction_type)
        return {"result": "Liked the post successfully."}
    except Exception as e:
        logger.error(f"An error occured during 'like_on_linkedin_post' tool: {str(e)}")
        return {"result": "An error occured, please try again"}
    
@tool('comment_on_linkedin_post', args_schema=CommentOnLinkedinPost)
def comment_on_linkedin_post(post_urn: str, comment: str):
    """This tool is used to comment a linkedin post given the post urn."""
    try:
        get_linkedin_api().comment_on_post(post_urn, comment)
        return {"result": "Commented on the post successfully."}
    except Exception as e:
        logger.error(f"An error occured during 'comment_on_linkedin_post' tool: {str(e)}")
        return {"result": "An error occured, please try again"}
        
    
## post the content in group
## attached images, link, video in the post

getTools = [internet_search, update_content_in_document, post_content_on_linkedin, fetch_linkedin_metadata, latest_ai_news, generate_thoughtful_comment_on_post,
            post_writer, viral_topic_suggestions, like_on_linkedin_post, comment_on_linkedin_post]