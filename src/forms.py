from pydantic import BaseModel
from typing import Optional

class PhotoCreateForm(BaseModel):
    title: str
    description: Optional[str] = None
    image: str