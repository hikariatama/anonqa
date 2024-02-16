from pydantic import BaseModel


class SendRequest(BaseModel):
    recipient_tag: str
    sender: str
    message: str


class SendResponse(BaseModel):
    status: str
    message: str
