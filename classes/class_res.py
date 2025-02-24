from pydantic import BaseModel,Field
from typing import Union
from typing import List
import datetime
class case_list(BaseModel):
    case_id  : str
    case_name: str
    case_info: str
    case_type: str
    case_owner:str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)