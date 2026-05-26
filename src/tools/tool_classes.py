from pydantic import BaseModel, Field
from typing import Optional, Any

class InternetSearch(BaseModel):
    requirements: Optional[str] = Field(description="Detailed user query for searching real-time or latest information from the internet.")

class LatestAINews(BaseModel):
    information: Optional[str] = Field(description="User requirement to fetch to real time or latest news articles related to the world of AI.")

class FetchLinkedinMetadata(BaseModel):
    user_query: Optional[str] = Field(description="User query related to fetch linkedin account details.")

class PostContentOnLinkedin(BaseModel):
    content: Optional[str] = Field(description="Content generated based on the user requirements as per linkedin formatting.")

class UpdateContentInDocument(BaseModel):
    content: Optional[str] = Field(description="Content generated based on the user requirements.")
    file_name: Optional[str] = Field(description="Name of the file")

class PostWriterInput(BaseModel):
    tone: Optional[str] = Field(
        default=None, description=(
            "Defines how the post should sound and feel. "
            "Examples: Formal, Friendly, Casual, Professional, "
            "Diplomatic, Confident, Simplified, Engaging, Direct, Viral."
        ),
        examples=["Professional", "Engaging", "Confident"])
    pitch: Optional[str] = Field(
        default=None, description=(
            "Defines the core message, intent, or angle of the post. "
            "Example: 'Announcing a new AI project', "
            "'Sharing a learning experience', "
            "'Explaining a GenAI concept simply'."
        ),
        examples=[
            "Explaining AI agents in simple words",
            "Sharing production deployment lessons",
            "Creating a viral LinkedIn post on RAG"])
    content: str = Field(description="The final generated post content based on the provided tone and pitch.")

class GenerateThoughtfulCommentOnPost(BaseModel):
    comment: Optional[str] = Field(description="Thoughtfull comment generated based on the provided post or article.")

class ViralTopicSuggestions(BaseModel):
    topics: Optional[list] = Field(description="List of viraltopics generated based on the ")
    
class LikeOnLinkedinPost(BaseModel):
    post_urn: str = Field(description="URN of the linkedin post to like")
    reaction_type: Optional[str] = Field(
        default="LIKE", description=(
            "Type of reaction to give on the linkedin post. "
            "Examples: LIKE, LOVE, CELEBRATE, SUPPORT, INSIGHTFUL, CURIOUS."
        ),
        examples=["LIKE", "LOVE", "CELEBRATE", "SUPPORT", "INSIGHTFUL", "CURIOUS"]
    )
    
class CommentOnLinkedinPost(BaseModel):
    post_urn: str = Field(description="URN of the linkedin post to like")
    comment: str = Field(description="Comment to be posted on the linkedin post")
