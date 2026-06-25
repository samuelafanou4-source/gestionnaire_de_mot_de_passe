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

# --- LES OPÉRATIONS CRUD ---

# 1. CREATE : Stocker un mot de passe existant

@app.post("/passwords", response_model=passwordResponse, status_code=201)
def create_password(item: passwordItem):
    global id_counter

    # Éviter les doublons pour un même site
    for entry in fake_db:
        if entry["site_name"].lower() == item.site_name.lower():
            raise HTTPException(status_code=400, detail="Un mot de passe existe déjà pour ce site")
        new_entry = {
        "id": id_counter,
        "site_name": item.site_name,
        "username": item.username,
        "password": item.password  # Reçu directement du client
    }
    fake_db.append(new_entry)
    id_counter += 1
    return new_entry