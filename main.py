import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.projet import router as ProjetRouter
from routes.auth import router as AuthRouter

app = FastAPI()
app.include_router(ProjetRouter, tags=["Projet"], prefix="/projet")
app.include_router(AuthRouter, tags=["Auth"], prefix="/auth")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "Status": "Success",
        "Message": "Guerrout"
    }

if __name__ == '__main__':
    uvicorn.run(f"main:app", host="127.0.0.1", port=8888, reload=True)
