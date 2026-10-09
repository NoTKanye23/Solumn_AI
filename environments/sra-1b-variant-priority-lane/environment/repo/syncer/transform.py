import re


def transform(row: dict) -> dict:
    """CSV row -> record shape the directory API stores."""
    digits = re.sub(r"\D", "", row["phone"])
    return {
        "id": row["id"],
        "name": " ".join(row["name"].split()),
        "email": row["email"].strip().lower(),
        "phone": "+" + digits if digits else "",
    }
