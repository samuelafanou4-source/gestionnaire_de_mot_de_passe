from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="gestionnaire de mot de passe")

class passwordItem(BaseModel):
    nom_site: str
    username: str
    password: str

class passwordResponse(BaseModel):
    id: int
    nom_site: str
    username: str
    password: str

fake_db: List[dict] = []
id_counter = 1