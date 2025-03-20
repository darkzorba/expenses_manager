import uvicorn
from fastapi import FastAPI
from expenses_back.routes import expenses, incomes

app = FastAPI()

app.include_router(expenses.router, prefix="/expenses", tags=["expenses"])
app.include_router(incomes.router, prefix="/incomes", tags=["incomes"])
@app.get("/")
def read_root():
    return {"message": "Servidor FastAPI rodando!"}
