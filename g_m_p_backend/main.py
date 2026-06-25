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

# 2. READ : Récupérer tous les comptes stockés
@app.get("/passwords", response_model=List[passwordResponse])
def get_all_passwords():
    return fake_db

# 2b. READ : Récupérer un compte spécifique par son ID
@app.get("/passwords/{entry_id}", response_model=passwordResponse)
def get_password(entry_id: int):
    for entry in fake_db:
        if entry["id"] == entry_id:
            return entry
    raise HTTPException(status_code=404, detail="Entrée introuvable")

# 3. UPDATE : Modifier un compte (Changer le mot de passe ou l'user)
@app.put("/passwords/{entry_id}", response_model=PasswordResponse)
def update_password(entry_id: int, item: PasswordItem):
    for index, entry in enumerate(fake_db):
        if entry["id"] == entry_id:
            updated_entry = {
                "id": entry_id,
                "site_name": item.site_name,
                "username": item.username,
                "password": item.password # Mis à jour avec la nouvelle valeur fournie
            }

            fake_db[index] = updated_entry
            return updated_entry
        raise HTTPException(status_code=404, detail="Entrée introuvable")

# 4. DELETE : Supprimer un compte
@app.delete("/passwords/{entry_id}")
def delete_password(entry_id: int):
    for index, entry in enumerate(fake_db):
        if entry["id"] == entry_id:
            fake_db.pop(index)
        return {"message": f"Les identifiants pour {entry['site_name']} ont été supprimés."}
    raise HTTPException(status_code=404, detail="Entrée introuvable")
