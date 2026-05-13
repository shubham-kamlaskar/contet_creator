from langchain.tools import tool
from pydantic import BaseModel, Field
from typing import Optional, Any
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import create_sync_playwright_browser
from src.agents.ollama_llm_provider import LLMProvider
from src.api.linkedin_api_methods import LinkedInAPI

llm_provider = LLMProvider()
linkedin_api = LinkedInAPI()

class InternetSearch(BaseModel):
    requirements: Optional[str] = Field(description="User requirement to related to real time or latest information.")
    
@tool("internet_search", args_schema=InternetSearch)
def internet_search(requirements: str) -> list:
    """This tool is useful to fetch information from internet,when user needs real time or latest information"""
    search = DuckDuckGoSearchResults(output_format="json", num_results=3)
    content = search.ainvoke(requirements)
    return content

# sync_browser = create_sync_playwright_browser()
# toolkit = PlayWrightBrowserToolkit.from_browser(
#     sync_browser=sync_browser
# )
# # Get tools
# playwright_tools = toolkit.get_tools()

class FetchLinkedinMetadata(BaseModel):
    user_query: Optional[str] = Field(description="User query related to fetch linkedin account details.")

@tool("fetch_linkedin_metadata", args_schema=FetchLinkedinMetadata)
def fetch_linkedin_metadata(user_query: str):
    """This tool is used to fetch information of linkedin user account."""
    profile_details = linkedin_api.get_profile_details()
    return {"response": profile_details}

class PostContentOnLinkedin(BaseModel):
    content: Optional[str] = Field(description="Content generated based on the user requirements as per linkedin formatting.")

@tool("post_content_on_linkedin", args_schema=PostContentOnLinkedin)
def post_content_on_linkedin(content: str):
    """This tool is used to post the content created based on user requirements on user linkedin account."""
    linkedin_api.post_share(text=content)
    return {"response": "Post successfully posted on your Linkedin profile. "}

def create_document(file_name: str, content: str):
    with open(f"{file_name}.txt", "w", encoding="utf-8") as file:
        file.write(f"{content}")
        
class UpdateContentInDocument(BaseModel):
    content: Optional[str] = Field(description="Content generated based on the user requirements.")
    file_name: Optional[str] = Field(description="Name of the file")

@tool('update_content_in_document', args_schema=UpdateContentInDocument)
def update_content_in_document(content: str, file_name: str):
    """This tool is used to create a .txt document based on the user requirements to create a document."""
    create_document(file_name, content)
    return {"response": f"A file is created with name {file_name}, as per your request."}

getTools = [internet_search, update_content_in_document, post_content_on_linkedin, fetch_linkedin_metadata]