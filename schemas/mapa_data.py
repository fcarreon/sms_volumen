def mapa_dataEntity(item) -> dict:
    return {
        "id":str(item["_id"]),
        "date":item["date"],
        "type":item["type"],
        "data":item["data"]

    }

def datasEntity(entity) -> list:
    return [mapa_dataEntity(item) for item in entity]
