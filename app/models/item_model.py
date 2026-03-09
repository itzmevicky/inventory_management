


def item_helper(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "sku": item["sku"],
        "stock": item["stock"]
    }
    
    
    