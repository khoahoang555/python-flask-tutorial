from flask import Flask, request

app = Flask(__name__)

stores = [
    {
        "name": "My Store", 
        "items": [
            {
                "name": "my item", 
                "price": 15.99
            }
        ]
    }
]

@app.route('/')
def index():
    a = 1
    b = 2
    z = sum(a, b)
    return "hello"

@app.get("/store")
def get_stores():
    return {"stores": stores}

@app.post("/store")
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return new_store, 201

def sum(a, b):
    return a + b

if __name__ == "__main__":
    app.run(debug = True)