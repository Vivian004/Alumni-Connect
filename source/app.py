from flask import Flask
from flask_restx import Resource, Api

app = Flask(__name__)
app.config["DEBUG"] = True

api = Api(app)


@api.route("/hello")
class Hello(Resource):
    def get(self):
        return {"hello": "world"}


if __name__ == "__main__":
    app.run()