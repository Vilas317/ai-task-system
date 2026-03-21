import requests

BASE = "http://localhost:8000"

def register(username, email, password, role):
    res = requests.post(f"{BASE}/auth/register", json={
        "username": username, "email": email,
        "password": password, "role": role
    })
    if res.status_code == 201:
        print(f"✅ Created {role}: {username}")
    else:
        print(f"ℹ️  {username}: {res.json().get('detail', res.text)}")

if __name__ == "__main__":
    register("admin", "admin@example.com", "admin123", "admin")
    register("john",  "john@example.com",  "user123",  "user")
    register("jane",  "jane@example.com",  "user123",  "user")
    print("\n✅ Done! Open: http://localhost:8000/docs")
    print("Admin → admin / admin123")
    print("User  → john  / user123")