from itertools import count
from flask import Flask, request, jsonify
from flask_pydantic_spec import FlaskPydanticSpec, Response, Request
from pydantic import BaseModel, Field
from typing import Optional
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage

app = Flask(__name__)
spec = FlaskPydanticSpec("api-flask", title="api-flask")
spec.register(app)
database = TinyDB(storage=MemoryStorage)
c = count()


class User (BaseModel):
    id: Optional[int] = Field(default_factory=lambda: next(c))
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


@app.get("/users/<int:id>")
@spec.validate(resp=Response(HTTP_200=User))
def get_user(id):
    """Retorna o User do id especificado"""
    try:
        user = database.search(Query().id == id)[0]
        return jsonify(user)
    except IndexError:
        return {"message": "User Not Found"}, 404


@app.post("/users")
@spec.validate(body=Request(User), resp=Response(HTTP_201=User))
def set_user():
    """Insere um user no banco de dados"""
    body = request.context.body.dict()
    database.insert(body)
    return body


@app.put("/users/<int:id>")
@spec.validate(body=Request(User), resp=Response(HTTP_201=User))
def update_user(id):
    """Atualiza um user no banco de dados"""
    body = request.context.body.dict()
    database.update(body, Query().id == id)
    return jsonify(body)


@app.delete("/users/<int:id>")
@spec.validate(resp=Response("HTTP_204"))
def delete_user(id):
    """Deleta um user no banco de dados"""
    database.remove(Query().id == id)
    return jsonify({})


app.run()
