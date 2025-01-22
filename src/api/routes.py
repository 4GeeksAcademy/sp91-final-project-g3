"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, Users, Hosts, Players, Tournaments, Matches, Participants, Match_participants, Teams
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/signup', methods=['POST'])
def register():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    player = request.json.get ('player', None)
   

    if not email or not password or not player:
        return jsonify({'msg': 'Todos los campos son necesarios'}), 400


    exist = Users.query.filter_by(email=email).first()
    if exist: 
        return jsonify({'success': False, 'msg': 'El correo electronico ya existe'}), 400
    
    hashed_password = generate_password_hash(password)
    print(hashed_password)
    new_user = Users(email=email, password=hashed_password, player=player)
    
    db.session.add(new_user)
    db.session.commit()
    
    token = create_access_token(identity=str(new_user.id))
    return jsonify({'users': new_user.serialize(), 'token': token}), 200

@api.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    
    if not email or not password:
        return jsonify({'msg': 'Email y contraseña son obligatorios'}), 400
    
    user = Users.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({'msg': 'Usuario no encontrado'}), 404
    
    if not check_password_hash (user.password, password):
        return jsonify ({'msg': 'email/contraseña incorrectos'}), 404

    
    token = create_access_token(identity=str(user.id))
    return jsonify({'msg': 'ok', 'token': token}), 200

@api.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    identity = get_jwt_identity()
    users = Users.query.get(identity)   
    if users: 
        print(users.serialize()) 
        return jsonify({'success': True, 'msg': 'OK', 'user': users.serialize()})
    return jsonify({'success': False, 'msg': 'Token erroneo'})

@api.route('/completePlayer/<int:player_id>', methods=['POST'])
def completePlayer(player_id):
    name = request.json.get('name', None)
    gender = request.json.get('gender', None)
    age = request.json.get ('age', None)
    rating = request.json.get ('rating', None)
    side = request.json.get ('side', None)
    hand = request.json.get ('hand', None)

    if not name or not gender or not age or not rating or not side or not hand:
        return jsonify({'msg': 'Todos los campos son necesarios'}), 400
    
    player = Players.query.get(player_id)
    if not player:
        return jsonify({'msg': 'El jugador no existe'}), 404

    # Actualizar los datos del jugador
    player.name = name
    player.gender = gender
    player.age = age
    player.rating = rating
    player.side = side
    player.hand = hand
    
    db.session.commit()



@api.route('/editPlayer/<int:player_id>', methods=['PUT'])
def editPlayer(player_id):
    data = request.json
    name = data.get('name')
    gender = data.get('gender')
    age = data.get('age')
    rating = data.get('rating')
    side = data.get('side')
    hand = data.get('hand')

    if not name or not gender or not age or not rating or not side or not hand:
        return jsonify({'msg': 'Todos los campos son necesarios'}), 400

    # Buscar al jugador por ID
    player = Players.query.get(player_id)
    if not player:
        return jsonify({'msg': 'El jugador no existe'}), 404

    player.name = name
    player.gender = gender
    player.age = age
    player.rating = rating
    player.side = side
    player.hand = hand

    db.session.commit()
    return jsonify({'msg': 'Jugador actualizado con éxito', 'player': player.serialize()}), 200


