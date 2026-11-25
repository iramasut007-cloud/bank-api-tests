from src.main.api.models.base_model import BaseModel



class CreditResponse(BaseModel):
    id: int
    amount:float
    balance:int
    creditId:float