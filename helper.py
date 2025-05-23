import json
from pathlib import Path
from cat.db.crud import get_users

import json
from pathlib import Path


def aggiorna_users_tags():
    users_db = get_users()  # Richiama direttamente la funzione CRUD
    users_data = list(users_db.values())

    # Carica i tag dal file JSON
    tags_file = Path("cat/static/tags.json")
    with tags_file.open("r", encoding="utf-8") as f:
        tags_data = json.load(f)
        # Extract the tags array from the object
        tags = tags_data.get("tags", [])

    # Crea il dizionario base dei tag
    base_tags_dict = {tag: False for tag in tags}

    # Crea il dizionario utente-tag
    user_tags_mapping = {}
    for user in users_data:
        username = user['username']
        # Crea una copia indipendente del dizionario base per ogni utente
        user_tags_mapping[username] = base_tags_dict.copy()

    # Salva il dizionario nel file JSON
    output_path = Path("cat/static/user_status.json")
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(user_tags_mapping, f, indent=4, ensure_ascii=False)
        
    return

def aggiorna_users_tags_solo_nuovi():
    users_db = get_users()  # Richiama direttamente la funzione CRUD
    users_data = list(users_db.values())

    # Carica i tag dal file JSON
    tags_file = Path("cat/static/tags.json")
    with tags_file.open("r", encoding="utf-8") as f:
        tags_data = json.load(f)
        # Extract the tags array from the object
        tags = tags_data.get("tags", [])

    # Crea il dizionario base dei tag
    base_tags_dict = {}

    # Carica il file user_status.json esistente se esiste
    output_path = Path("cat/static/user_status.json")
    user_tags_mapping = {}
    if output_path.exists():
        with output_path.open("r", encoding="utf-8") as f:
            try:
                user_tags_mapping = json.load(f)
            except json.JSONDecodeError:
                # Se il file è vuoto o non è un JSON valido, inizializza un dizionario vuoto
                user_tags_mapping = {}

    # Aggiunge solo gli utenti non ancora presenti nel dizionario
    for user in users_data:
        username = user['username']
        if username not in user_tags_mapping:
            # Crea una copia indipendente del dizionario base solo per i nuovi utenti
            user_tags_mapping[username] = base_tags_dict.copy()

    # Salva il dizionario nel file JSON
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(user_tags_mapping, f, indent=4, ensure_ascii=False)
    
    return
