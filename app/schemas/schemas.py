from pydantic import BaseModel

class URLRequest(BaseModel):
    user_url: str

class Token(BaseModel):
    access_token: str
    token_type: str