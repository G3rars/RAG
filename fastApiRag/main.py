from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag.queryEngine import query

app = FastAPI()

# Configurar el middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permitir solicitudes GET, POST y OPTIONS
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.get("/")
async def read_root():
    return {"message": "Welcome to the bookstore assistant API. Use /pregunta to query."}

@app.post("/pregunta")
async def ask_question(query_request: QueryRequest):
    response = await query(query_request.question)
    return {"message": response.response}

# Manejar errores CORS pre-vuelo
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    if exc.status_code == 405:
        return {"message": "Method Not Allowed"}, 405
    return {"message": "Unhandled HTTP Exception"}, 500
