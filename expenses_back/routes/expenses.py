
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from expenses_back.fn.expenses import Expenses
router = APIRouter()


class ExpenseModel(BaseModel):
    description: str
    type: str|int
    value: float
    date:str
    id: int = None


@router.get("/expenses/{month}")
def get_expenses(month:int):

    response = Expenses().get_expenses_by_month(month)

    return JSONResponse(content=response,status_code=response['status_code'])

@router.post("/expense")
def save_expense(expense:ExpenseModel):

    response = Expenses().save_expanse(description=expense.description, type=expense.type, value=expense.value,
                                       date=expense.date,id=expense.id)

    return JSONResponse(content=response,status_code=response['status_code'])

@router.delete("/expense/{expense_id}")
def delete_expense(id:str|int):

    response = Expenses().delete_expense(expense_id=id)

    return JSONResponse(content=response,status_code=response['status_code'])

