from pydantic import BaseModel


class ModelRead(BaseModel):
    id: int
    model_key: str
    model_name: str
    model_type: str
    version: str
    params: dict
    is_active: bool

    model_config = {"from_attributes": True}
