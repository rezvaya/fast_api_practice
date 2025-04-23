from sqlmodel import SQLModel, Field
import uuid

class URL(SQLModel, table=True):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:6], primary_key=True)
    original_url: str
    clicks: int = 0 

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str