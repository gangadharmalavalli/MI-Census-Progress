USERS = {
    "Gangadhar": "Malavalli Taluk",
    "Siddaraju": "Mandya Taluk",
    "Prashanth": "Srirangapatna Taluk",
    "Sunil": "Maddur Taluk",
    "Nagarjun": "K.R. Pete Taluk",
    "Chethan": "Nagamangala Taluk",
    "Purushottam": "Pandavapura Taluk"
}

PASSWORD = "mandya"

def authenticate(user: str, password: str):
    if user in USERS and password == PASSWORD:
        return USERS[user]
    return None
