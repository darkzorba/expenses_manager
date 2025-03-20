
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from expenses_back.fn.incomes import Incomes
router = APIRouter()


class IncomeModel(BaseModel):
    description: str
    type: str|int
    value: float
    date:str
    id:int|str = None


@router.get("/incomes/{month}")
def get_expenses(month:int):

    response = Incomes().get_incomes_by_month(month)

    return JSONResponse(content=response,status_code=response['status_code'])

@router.post("/income")
def save_expense(income:IncomeModel):

    response = Incomes().save_income(description=income.description, type=income.type, value=income.value,
                                     date=income.date,id=income.id)

    return JSONResponse(content=response,status_code=response['status_code'])

@router.delete("/income/{income_id}")
def delete_expense(id:str|int):

    response = Incomes().delete_income(income_id=id)

    return JSONResponse(content=response,status_code=response['status_code'])

