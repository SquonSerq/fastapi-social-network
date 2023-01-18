from api import api
from db.database import engine
from fastapi import FastAPI
from db.base_class import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
	return {"Hello": "Webtronics!"}

app.include_router(api.api_router)
