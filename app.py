from flask import Flask, request, jsonify
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from pydantic import BaseModel
from typing import Optional
from tinydb import TinyDB, Query

app = Flask(__name__)
spec = FlaskPydanticSpec("api-flask", title="api-flask")
spec.register(app)
database = TinyDB("database.json")


class User (BaseModel):
    id: Optional[int]
    name: str
    age: int


class Users (BaseModel):
    users: list[User]
    count: int


@app.get("/users")
@spec.validate(resp=Response(HTTP_200=Users))
def get_users():
    """Retorna todos os Users"""
    return jsonify(
        Users(
            users=database.all(),
            count=len(database.all())
        ).dict()
    )


@app.post("/users")
@spec.validate(body=Request(User), resp=Response(HTTP_200=User))
def set_user():
    """Insere um user no banco de dados"""
    body = request.context.body.dict()
    database.insert(body)
    return body

@app.put("/users/<int:id>")
@spec.validate(body=Request(User), resp=Response(HTTP_200=User))
def update_user(id):
    """Atualiza um user no banco de dados"""
    User = Query()
    body = request.context.body.dict()
    database.update(body, User.id == id)
    return jsonify(body)

@app.delete("/users/<int:id>")
@spec.validate(resp=Response(HTTP_200=User))
def delete_user(id):
    """Deleta um user no banco de dados"""
    User = Query()
    database.remove(User.id == id)
    return jsonify({})


app.run()
