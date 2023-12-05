from pydantic import BaseModel


class Traffic(BaseModel):
    code: str
    quantity: int
