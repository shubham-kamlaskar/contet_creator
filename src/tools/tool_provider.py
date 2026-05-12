from langchain.tools import tool
from pydantic import BaseModel, Field
from typing import Optional, Any
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import (
    create_sync_playwright_browser,
)
from src.agents.ollama_llm_provider import LLMProvider

llm_provider = LLMProvider()

class CreateContent(BaseModel):
    requirements: Optional[str] = Field(description="User requirements to generate a well structured and viral linkedin post")
    
@tool("create_content", args_schema=CreateContent)
def create_content(requirements: str):
    """This tool is useful in creating a viral linkedin post based on the user requirements in a pre-defined and structured format. """
    content = f"Based on the given {requirements}: we are writing the content"
    return {"response": content}

class InternetSearch(BaseModel):
    requirements: Optional[str] = Field(description="User requirement to related to real time or latest information.")
    
@tool("internet_search", args_schema=InternetSearch)
def internet_search(requirements: str) -> list:
    """This tool is useful to fetch information from internet,when user needs real time or latest information"""
    search = DuckDuckGoSearchResults(output_format="json", num_results=3)
    content = search.invoke(requirements)
    return content

class LinkedinAutomation(BaseModel):
    request: Optional[str] = Field(description="User request related to linkedin.")

@tool('linkedinautomation', args_schema=LinkedinAutomation)
def linkedinautomation(request: str):
    """This tool is useful to draft the  post, send dms, send connection request, job tracking, lead enrichment, crm auto reply and etc."""
    return {"response": f"Processing LinkedIn request: {request}"}

sync_browser = create_sync_playwright_browser()
toolkit = PlayWrightBrowserToolkit.from_browser(
    sync_browser=sync_browser
)
# Get tools
playwright_tools = toolkit.get_tools()

def create_document(file_name: str, content: str):
    with open(f"{file_name}.txt", "w", encoding="utf-8") as file:
        file.write(f"{content}")
        
class UpdateContentInDocument(BaseModel):
    user_query: Optional[str] = Field(description="User query related to document creation on the given topic or information")
    file_name: Optional[str] = Field(description="Name of the file")

@tool('update_content_in_document', args_schema=UpdateContentInDocument)
def update_content_in_document(user_query: str, file_name: str):
    """This function is used to create a .txt document based on the user requirements."""
    llm = llm_provider.llm_client()
    response = llm.invoke(user_query)
    if response:
        messages = response.get("messages", [])
        response_call = messages[-1] if messages else None
        answer = response_call.content
        
        create_document(file_name, answer)
    return {"response": f"A file is created with name {file_name}, as per your request."}

getTools = [internet_search]