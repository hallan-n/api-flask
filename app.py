from flask import Flask
from flask_pydantic_spec import FlaskPydanticSpec, Response
from pydantic import BaseModel

app = Flask(__name__)
spec = FlaskPydanticSpec("flask", title="api-flask")
spec.register(app)

class User(BaseModel):
    id: int
    name: str
    age: int



@app.get("/users")
@spec.validate(resp=Response(HTTP_200=User))
def get_users():
    return "Ok"

app.run()
