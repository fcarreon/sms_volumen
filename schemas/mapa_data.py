def mapa_dataEntity(item) -> dict:
    return {
        "id":str(item["_id"]),
        "date":item["date"],
        "type_data":item["type_data"],
        "data":item["data"]

    }

def datasEntity(entity) -> list:
    return [mapa_dataEntity(item) for item in entity]
