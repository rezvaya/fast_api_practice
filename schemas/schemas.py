from pydantic import BaseModel

class URLRequest(BaseModel):
    user_url: str