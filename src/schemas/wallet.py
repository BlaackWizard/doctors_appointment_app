from pydantic import BaseModel


class SWalletRequest(BaseModel):
    amount: float


class SWalletResponse(BaseModel):
    message: str
    balance: float
