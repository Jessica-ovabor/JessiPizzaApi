from flask import request
from flask import request
from flask_restx import Namespace,Resource,fields
from ..utils import db
from ..models.users import User 
from werkzeug.security import generate_password_hash,check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt_identity
auth_namespace =Namespace("auth" , description="name space for authentication")
#serialiszation of all input which is in this a user model
#what our user 
signup_model = auth_namespace.model(
    'Signup',{
        "id": fields.Integer(),
        "username": fields.String(required=True, description= "A username"),
        "email": fields.String(required=True, description= "An email"),
        "password": fields.String(required=True, description= "A password")
  
        
        
    }
)
#when are users logins all this information will be returned to the user
user_model = auth_namespace.model(
    'User',{
        "id": fields.Integer(),
        "username": fields.String(required=True, description= "A username"),
        "email": fields.String(required=True, description= "An email"),
        "password_hash": fields.String(required=True, description= "A password"),
        "is_active": fields.Boolean(description= "This shows the user is active or not"),
        "is_staff": fields.Boolean(description= "This shows if it a staff or not")
        
        
    }
)
@auth_namespace.route('/signup')
class Signup(Resource):
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user_model)#marshal_with return json rather than object in db we use it to serialise
    
    def post(self):
        """
        Sign up a user
        
        """
        data= request.get_json()#{data = "username": "Jessica","email":ovaj@gmail.com,"password":"idontknow"}
        new_user = User(
            username=data.get('username'),
            email=data.get('email'),
            password_hash=generate_password_hash(data.get('password'))
            )
        
        new_user.save()
        
        return new_user,HTTPStatus.CREATED
#login model serialiser       
login_model = auth_namespace.model(
    'Login',{
       
        "email": fields.String(required=True, description= "An email"),
        "password": fields.String(required=True, description= "A password")
  
        
        
    }
)      
@auth_namespace.route('/login')
@auth_namespace.expect(login_model)
class Login(Resource):
    def post(self):
        """
        Generate token
        """
        data= request.get_json()
        email=data.get('email')
        password=data.get('password')
        
        #checks if in the database if for instance ovaj@gmail.com exixts in our dable it grabs the whole info about that note emailmis set to be unique
        user = User.query.filter_by(email=email).first()
     
        if (user is not None) and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity= user.username)
            refresh_token = create_refresh_token(identity= user.username)  
            
            
            response ={
                'access_token':access_token,
                'refresh_token':refresh_token
            }
            
            return response, HTTPStatus.CREATED     
#it refreshes and return a username  and our authentication endpoint     
@auth_namespace.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        username =get_jwt_identity()
        
        access_token = create_access_token(identity=username)
        
        return{"access_token":access_token }, HTTPStatus.OK