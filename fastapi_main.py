from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- MongoDB ----------------
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.my_database
collection = db.users


# ---------------- Model ----------------
class User(BaseModel):
    name: str
    email: str
    age: int = None


# ---------------- HTML PAGE ----------------
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>FastAPI User Form</title>
    <style>
        body { font-family: Arial; max-width: 500px; margin: 50px auto; }
        input { width: 100%; padding: 10px; margin: 8px 0; }
        button { width: 100%; padding: 10px; background: green; color: white; border: none; }
        #result { margin-top: 15px; }
    </style>
</head>
<body>

<h2>Create User</h2>

<form id="userForm">
    <input type="text" id="name" placeholder="Name" required>
    <input type="email" id="email" placeholder="Email" required>
    <input type="number" id="age" placeholder="Age">
    <button type="submit">Submit</button>
</form>

<div id="result"></div>

<script>
document.getElementById("userForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const data = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        age: document.getElementById("age").value ? Number(document.getElementById("age").value) : null
    };

    const res = await fetch("/users", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    const result = await res.json();

    document.getElementById("result").innerHTML =
        "<pre>" + JSON.stringify(result, null, 2) + "</pre>";
});
</script>

</body>
</html>
"""


# ---------------- Create User ----------------
@app.post("/users")
async def create_user(user: User):
    result = await collection.insert_one(user.dict())
    return {
        "id": str(result.inserted_id),
        "message": "User created successfully"
    }


# ---------------- Get Users ----------------
@app.get("/users")
async def get_users():
    users = []
    cursor = collection.find()

    async for user in cursor:
        user["_id"] = str(user["_id"])
        users.append(user)

    return users
