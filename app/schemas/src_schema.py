from pydantic import BaseModel

class SrcInDB(BaseModel):
    spider_name: str
    name: str
    domain: str
    class config:
        orm_mode = True