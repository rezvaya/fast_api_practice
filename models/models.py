from sqlmodel import SQLmodel, Field
import uuid

class URL(SQLmodel, table=True):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:6], primary_key=True)
    original_url: str
    clicks: int = 0 