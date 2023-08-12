from flask import Flask

app= Flask(__name__)

@app.get("/users")
def get_users():
    return "Ok"

app.run()