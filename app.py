"""Flask app for Cupcakes"""

import requests
from flask import Flask, request, redirect, render_template, flash, jsonify
from flask_pretty import Prettify
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/api/cupcakes')
def get_all_cupcakes():
    """Respond with JSON for all cupcakes"""
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)

@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    """Respond with JSON for one cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes', methods=["POST"])
def add_cupcake():
    """Send post request to add a cupcake, then respond with corresponding JSON"""

    new_cupcake = Cupcake(flavor=request.json["flavor"], size=request.json["size"], rating=request.json["rating"], image=request.json["image"] or None)
    
    # print(request.form["flavor"])
    # new_cupcake = Cupcake(flavor=request.form["flavor"], size=request.form["size"], rating=request.form["rating"], image=request.form["image"])

    db.session.add(new_cupcake)
    db.session.commit()
    
    res = jsonify(cupcake=new_cupcake.serialize())

    return(res, 201)

@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    """Sends patch request to update cupcake details, responds with 404 if not found"""
    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image']

    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = flavor
    cupcake.size = size
    cupcake.rating = rating
    cupcake.image = image
    db.session.commit()

    res = jsonify(cupcake=cupcake.serialize())
    return res
 
@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    """Sends delete request to delete cupcake from db"""
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Cupcake deleted.")

@app.route('/')
def show_home():
    """Loads home page"""

    return render_template('home.html')