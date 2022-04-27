from flask import Flask, request, render_template, flash, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcakes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def show_index():
    """Return index.html"""
    
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    
    return render_template('index.html', cupcakes=cupcakes)

@app.route('/api/cupcakes', methods=['GET', 'POST'])
def handle_all_cupcakes():
    """Handles both GET and POST methods"""

    if request.method == 'GET':
        """Return {cupcakes: [{id, flavor, size, rating, image}, ...]}"""
        cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]

        return jsonify(cupcakes=cupcakes)

    if request.method == 'POST':
        """Return JSON like: {cupcake: {id, flavor, size, rating, image}}."""
        json = request.json
        new_cupcake = Cupcake(
            flavor = json["flavor"],
            size = json["size"],
            rating = json["rating"],
            image = json["image"] or None
        )

        db.session.add(new_cupcake)
        db.session.commit()
        

        return (jsonify(cupcake=new_cupcake.serialize()), 201)

@app.route('/api/cupcakes/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def handle_single_cupcake(id):

    cupcake = Cupcake.query.get_or_404(id)

    if request.method == 'GET':
        """Return single cupcake as {cupcake: {id, flavor, size, rating, image}}"""

        return jsonify(cupcake=cupcake.serialize())

    if request.method == 'PATCH':
        """Respond with JSON of the newly-updated cupcake, like this: {cupcake: {id, flavor, size, rating, image}}."""

        cupcake.flavor = request.json["flavor"]
        cupcake.size = request.json["size"]
        cupcake.rating = request.json["rating"]
        cupcake.image = request.json["image"]

        db.session.commit()

        return jsonify(cupcake=cupcake.serialize())

    if request.method == 'DELETE':
        """Respond with JSON like {message: "Deleted"}"""

        db.session.delete(cupcake)
        db.session.commit()

        return {'message': 'Deleted'}