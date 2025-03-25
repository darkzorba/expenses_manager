import uvicorn
from fastapi import FastAPI
from expenses_back.routes import expenses, incomes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost:4200",  # O seu frontend Angular
]

# Adiciona o middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permite apenas essas origens
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

app.include_router(expenses.router, prefix="/expenses", tags=["expenses"])
app.include_router(incomes.router, prefix="/incomes", tags=["incomes"])
@app.get("/")
def read_root():
    return {"message": "Servidor FastAPI rodando!"}
