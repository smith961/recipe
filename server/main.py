from flask import Flask,make_response,jsonify,request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token,create_refresh_token,get_jwt_identity,jwt_required
from flask_cors import CORS

from models import db, Recipe, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)
db.init_app(app)

jwt=JWTManager(app)

api = Api(app)
# bcrypt = Bcrypt(app)

class Signup(Resource):
    def post(self):
        data = request.get_json()

        username = data.get('username')

        db_user = User.query.filter_by(username=username).first()
        
        if db_user is not None:
            return jsonify({"message": f"User with username {username} already exist"})
        
        
        
        new_user = User(
            username = data.get('username'),
            email = data.get('email'),
            password = generate_password_hash(data.get('password'))
        )

        # new_user.save()
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully"})

api.add_resource(Signup, '/signup')

class Login(Resource):
    def post(self):
        data = request.get_json()

        username = data.get('username')
        password = data.get('password')
        
        db_user = User.query.filter_by(username=username).first()

        if db_user and check_password_hash(db_user.password, password):

            access_token = create_access_token(identity=db_user.username)
            refresh_token = create_refresh_token(identity=db.user.username)

            return jsonify(
                {"access_token": access_token, 
                 "refresh_token": refresh_token}
            )
        else:
            return jsonify({"message": "Invalid username or password"})

api.add_resource(Login, '/login')

class RefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(slef):

        current_user = get_jwt_identity()

        new_access_token = create_access_token(identity=current_user)

        return make_response(jsonify({"access_token": new_access_token}),200)

api.add_resource(RefreshResource, '/refresh')


class HelloResource(Resource):
    def get(self):
        message_dict = {"message": "Hello world"}
        response = make_response(message_dict,200)
        return response

api.add_resource(HelloResource, '/home')

class RecipesResource(Resource):
    def get(self):
        recipes = Recipe.query.all()
        recipes_dict = recipes.to_dict()
        response = make_response(recipes_dict, 200)
        return response

      
    def post(self):
        data = request.get_json()

        new_recipe = Recipe(
            title= data.get('title'),
            decription = data.get('description')
        )
        # new_recipe.save()
        db.session.add(new_recipe)
        db.session.commit()

        recipe_dict = new_recipe.to_dict()
        response = make_response(recipe_dict, 201)


        return response

api.add_resource(RecipesResource, '/recipes')

class RecipeResource(Resource):
    def get(self, id):
        recipe = Recipe.query.filter_by(id=id).first()
        recipe_dict = recipe.to_dict()
        response = make_response(recipe_dict, 200)
        return response

    @jwt_required() 
    def put(self, id):
        recipe_to_update = Recipe.query.filter_by(id=id).first()

        data = request.get_json()
        recipe_to_update.update(
           data.get('title'),
           data.get('description') 
        )
        recipe_to_update_dict= recipe_to_update.to_dict()

        response = make_response(recipe_to_update_dict, 200)

        return response
   
    @jwt_required()
    def delete(self, id):
        recipe_to_delete = Recipe.query.filter_by(id=id).first()

        recipe_to_delete.delete()

        return recipe_to_delete

api.add_resource(RecipeResource, '/recipe/<int:id>')



if __name__ == '__main__':
    app.run()