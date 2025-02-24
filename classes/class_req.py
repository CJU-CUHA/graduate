from pydantic import BaseModel
from typing import Union
from typing import List
class join(BaseModel):
    username: str
    password: str

class login(BaseModel):
    username: str
    password: str
    email   : str

class File(BaseModel):
    case_id : int
    pc_name : str
    files   : List[bytes]

class case_req(BaseModel):
    case_name: str
    case_info: str
    case_type: str
    case_owner: str






