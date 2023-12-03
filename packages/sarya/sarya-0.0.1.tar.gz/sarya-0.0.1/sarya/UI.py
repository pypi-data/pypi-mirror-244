from __future__ import annotations
from pydantic import BaseModel
from enum import Enum
from typing import Any

class UITypes(str, Enum):
    Text = "text"
    Image = "image"

class Text(BaseModel):
    type:UITypes = UITypes.Text
    content: str
class Image(BaseModel):
    type:UITypes = UITypes.Image
    content : str

