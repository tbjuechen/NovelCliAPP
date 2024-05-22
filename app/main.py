from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from sqlalchemy.orm import Session


from config.database import Base,engine
from routers import user_router, down_router, source_router, book_routers


app = FastAPI(openapi_prefix="/api")

app.include_router(user_router)
app.include_router(down_router)
app.include_router(source_router)
app.include_router(book_routers)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True, workers=1)