"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Product, Favorites, Review, Garage
from api.utils import generate_sitemap, APIException


import pandas as pd

from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required


app = Flask(__name__)



api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200



@api.route('car-brands', methods=['GET'])
def get_car_brands():
    cars_data = pd.read_csv('/workspaces/Watacar_v2/src/api/brands-and-models/cars-2020.csv')
    brands = cars_data['make'].unique().tolist()
    return jsonify(brands)

@api.route('car-models', methods=['GET'])
def get_car_models():
    cars_data = pd.read_csv('/workspaces/Watacar_v2/src/api/brands-and-models/cars-2020.csv')
    models = cars_data['model'].unique().tolist()
    return jsonify(models)


@api.route('moto-brands', methods=['GET'])
def get_moto_brands():
    moto_data = pd.read_csv('/workspaces/Watacar_v2/src/api/brands-and-models/motorcycles-2020.csv')
    brands = moto_data['Make'].unique().tolist()
    return jsonify(brands)

@api.route('moto-models', methods=['GET'])
def get_moto_models():
    moto_data = pd.read_csv('/workspaces/Watacar_v2/src/api/brands-and-models/motorcycles-2020.csv')
    models = moto_data['Model'].unique().tolist()
    return jsonify(models)

@api.route('/configuration', methods=['GET'])
@jwt_required()
def configuration():
    current_user = get_jwt_identity()
    user=User.query.filter_by(id=current_user).first()
    response_body = {
        "data": user.serialize()
    }

    return jsonify(response_body), 200


@api.route('/configuration', methods=['PUT'])
@jwt_required()
def update_configuration():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    if user is None:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    full_name = data.get('full_name')
    email = data.get('email')
    document_type = data.get('document_type')
    document_number = data.get('document_number')
    address = data.get('address')
    phone = data.get('phone')

    if full_name:
        user.full_name = full_name
    if email:
        user.email = email
    if document_type:
        user.document_type = document_type
    if document_number:
        user.document_number = document_number
    if address:
        user.address = address
    if phone:
        user.phone = phone

    try:
        db.session.commit()
        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error updating user"}), 500
    




@api.route('/configuration/garage', methods=['PUT'])
@jwt_required()
def update_garage_configuration():
    current_user = get_jwt_identity()
    garage = Garage.query.filter(Garage.user_id == current_user).first()
    if garage is None:
        return jsonify({"message": "No existe el Taller que buscas"}), 404
    
    data = request.get_json()
    garage.name = data.get('name')
    garage.mail = data.get('mail')
    garage.web = data.get('web')
    garage.phone = data.get('phone')
    garage.address = data.get('address')
    garage.description = data.get('description')
    garage.cif = data.get('cif')
    garage.image_id = data.get('image_id')
    garage.product_id = data.get('product_id')
    garage.user_id = data.get('user_id')
    print(garage.serialize())
    try:
       
        db.session.commit()
        return jsonify({"message": "Se ha actualizado correctamente el Taller"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": Exception}), 500



@api.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"message": "Error: email y contraseña requeridos"}), 400
    user = User.query.filter_by(email=email, password=password).first()
    if user is None:
        return("El usuario no es correcto"), 400
    token = create_access_token(identity=user.id)
    return jsonify({"token": token}), 200



@api.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')
    document_type = data.get('document_type')
    document_number = data.get('document_number')
    address = data.get('address')
    role = data.get('role')
    phone = data.get('phone')

    register = User(full_name = full_name, email=email, password=password, document_type=document_type, document_number=document_number, address=address, role=role, phone=phone)
    print(register)

    if register is None:
        return jsonify({"message" : "Complete the fields!"}), 400
    
    db.session.add(register)
    db.session.commit()

    return jsonify({"message" : "Signed up successfully!"}), 200

@api.route('/profile/onsale', methods=['GET'])
@jwt_required()
def getProducts():
    current_user = get_jwt_identity()
    products = Product.query.filter(Product.user_id == current_user).all()
    response_body = {
        "data": [product.serialize() for product in products]
    }
    return jsonify(response_body), 200

@api.route('/profile/favorites', methods=['POST'])
@jwt_required()
def saveFavorites():
    current_user = get_jwt_identity()
    data = request.get_json()
    product_id = data.get("product_id")

    usuario = User.query.get(current_user)
    producto = Product.query.get(product_id)

    if not producto:
        return jsonify({"mensaje": "Producto no encontrado"}), 404

    favorite = Favorites(user_id=usuario.id, product_id=producto.id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({"mensaje": "Producto guardado como favorito"}), 200

@api.route('/profile/favorites', methods=['GET'])
@jwt_required()
def getFavorites():
    current_user = get_jwt_identity()

    usuario = User.query.get(current_user)
    if not usuario:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    favorites = Favorites.query.filter_by(user_id=usuario.id).all()

    response = []
    for favorite in favorites:
        product = Product.query.get(favorite.product_id)
        response.append({
            "product_id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "year": product.year,
            "km": product.km
        })

    return jsonify(response), 200

@api.route('/profile/favorites/<int:product_id>', methods=['PUT'])
@jwt_required()
def removeFavorite(product_id):
    current_user = get_jwt_identity()

    usuario = User.query.get(current_user)
    producto = Product.query.get(product_id)

    if not producto:
        return jsonify({"mensaje": "Producto no encontrado"}), 404

    favorite = Favorites.query.filter_by(user_id=usuario.id, product_id=producto.id).first()

    if not favorite:
        return jsonify({"mensaje": "El producto no está marcado como favorito"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"mensaje": "Producto desmarcado como favorito"}), 200

@api.route('/profile/reviews', methods=['POST'])
@jwt_required()
def addReview():
    current_user = get_jwt_identity()
    data = request.get_json()
    product_id = data.get("product_id")
    stars = str(data.get("stars"))  # Convertir a cadena
    comment = data.get("comment")

    user = User.query.get(current_user)
    product = Product.query.get(product_id)

    if not product:
        return jsonify({"mensaje": "Producto no encontrado"}), 404

    recived_user = User.query.get(product.user_id)

    review = Review(given_review_id=user.id, recived_review_id=recived_user.id, product_id=product.id, stars=stars, comment=comment)
    db.session.add(review)
    db.session.commit()

    return jsonify({"mensaje": "Reseña agregada correctamente"}), 200







@api.route('/profile/reviews', methods=['GET'])
@jwt_required()
def getReviews():
    current_user = get_jwt_identity()

    reviews = Review.query.filter_by(given_review_id=current_user).all()
    if not reviews:
        return jsonify({"mensaje": "No se encontraron reseñas"}), 404

    review_list = []
    for review in reviews:
        stars = review.stars.value    
        product = Product.query.get(review.product_id)

        review_data = {
            "product_id": review.product_id,
            "stars": int(stars),
            "comment": review.comment,
            "given_review_id": review.given_review_id,
            "product_name": product.name,
            "recived_review_id": review.recived_review_id,
            "recived_user_id": review.recived_review_id
        }
        review_list.append(review_data)

    return jsonify(review_list), 200


@api.route('/profile/garage', methods=['GET'])
@jwt_required()
def getMyGarage():
    current_user = get_jwt_identity()
    garage = Garage.query.filter_by(user_id=current_user).first()

    if not garage:
        return jsonify({"mensaje": "No se encontró tu taller"}), 404
    
    
    garage_data = {
        "name": garage.name,
        "web": garage.web,
        "phone": garage.phone,
        "mail": garage.mail,
        "address": garage.address,
        "description": garage.description,
        "cif": garage.cif,
        "image_id": garage.image_id,
        "product_id": garage.product_id,
        "user_id": garage.user_id
    }

    return jsonify(garage_data), 200



@api.route('/garages', methods=['GET'])
def getGarages():
    garages = Garage.query.all()
    if not garages:
        return jsonify({"mensaje": "No se econtrón ningún garage"}), 500

    garages_list = []
 
    for garage in garages:
        garage_data = {
            "name": garage.name,
            "web": garage.web,
            "phone": garage.phone,
            "mail": garage.mail,
            "address": garage.address,
            "description": garage.description,
            "cif": garage.cif,
            "image_id": garage.image_id,
            "product_id": garage.product_id,
            "user_id": garage.user_id
        }
    garages_list.append(garage_data)

    return jsonify(garages_list), 200


@api.route('/create-garage', methods=['POST'])
@jwt_required()
def createGarage():
    current_user = get_jwt_identity()

    # Verificar si el garaje ya existe para el usuario actual
    existing_garage = Garage.query.filter_by(user_id=current_user).first()
    if existing_garage:
        return jsonify({"mensaje": "Ya existe un garaje asociado a este usuario"}), 400

    try:
        data = request.json
        name = data.get("name")
        mail = data.get("mail")
        phone = data.get('phone')
        cif = data.get('cif')
        address = data.get('address')
        web = data.get('web')
        description = data.get('description')
        image_id = data.get('image_id')

        if not all([name, mail, phone, address, description, cif]):
            return jsonify({"mensaje": "No se han completado todos los campos requeridos (nombre, email, teléfono, dirección, descripción o cif)"}), 400

        # Crear el nuevo garaje
        new_garage = Garage(
            name=name,
            mail=mail,
            phone=phone,
            cif=cif,
            address=address,
            description=description,
            web=web,
            image_id=image_id,
            user_id=current_user
        )
        db.session.add(new_garage)
        db.session.commit()

        return jsonify({"mensaje": "Garaje creado exitosamente"}), 200

    except Exception as e:
        # Capturar cualquier excepción y devolver una respuesta de error
        return jsonify({"mensaje": f"Error al crear el garaje: {str(e)}"}), 500
