def vendor_helper(vendor) -> dict:
    return {
        "id": str(vendor["_id"]),
        "name": vendor["name"],
        "email": vendor["email"],
        "phone": vendor.get("phone")
    }