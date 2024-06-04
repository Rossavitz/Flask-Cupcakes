"""Flask app for Cupcakes"""

from flask import Flask, jsonify, request, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcakes_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "chickenzarecool21837"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

app.app_context().push()
connect_db(app)


@app.route("/")
def show_homepage():
    """show homepage"""
    return render_template("index.html")


@app.route("/api/cupcakes")
def list_cupcakes():
    """show data about cupcakes"""
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)


@app.route("/api/cupcakes/<int:id>")
def get_cupcake(id):
    """returns JSON for one cupcake in particular"""
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())


@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Creates a new cupcake and returns JSON of that created cupcake"""
    data = request.json

    new_cupcake = Cupcake(
        flavor=data["flavor"],
        rating=data["rating"],
        size=data["size"],
        image=data["image"] or None,
    )

    db.session.add(new_cupcake)
    db.session.commit()
    response_json = jsonify(cupcake=new_cupcake.serialize())
    return (response_json, 201)


@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
def update_cupcake(id):
    """updates a cupcake and response w/ JSON of that updated cupcake"""
    data = request.json
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = data["flavor"]
    cupcake.size = data["size"]
    cupcake.rating = data["rating"]
    cupcake.image = data["image"]

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())


@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
def delete_cupcake(id):
    """deletes a cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="deleted")
