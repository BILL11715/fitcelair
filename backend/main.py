from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def Hello():
    return "Hello World"


@app.get("/users")
def users():
    return ["Adam", "David"]


@app.get("/books")
def books():
    return ["book 1", "book 2", "book 3"]
