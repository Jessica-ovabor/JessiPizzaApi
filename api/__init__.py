from flask import Flask
from flask_restx import Api
from .order.views import order_namespace
from .auth.views import auth_namespace
from .config.config import config_dict
from .utils  import db
from .models.orders import Order
from .models.users import User
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound,MethodNotAllowed



def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    #configure the dev so we can use it
    app.config.from_object(config)
    db.init_app(app)
    jwt = JWTManager(app)
    authorizations={
        'Bearer Auth':{
            'type':'apiKey',
            'in' :'header',
            'name' :'Authorization',
            'description':'Add a JWT to the header wit **Bearer &lt;JWT&gt; **token to authorize'
        }
        
    }
    migrate =Migrate(app,db)
    api =Api(app,title='Pizza Delivery API',description='A simple pizza delivery RESTAPI services',authorizations=authorizations,security="Bearer Auth")
    api.add_namespace(order_namespace,path='/order')
    api.add_namespace(auth_namespace,path='/auth')
    #Error handling in api
    @api.errorhandler(NotFound)
    def not_found(error):
        return {'error': 'Not Found'},404
    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {'error': 'Method Not Allowed'},404
    
    #connect to a databasei.e create our database by migrating
    @app.shell_context_processor
    def make_shell_context():
        return{
            'db':db,
            'User':User,
            'Order':Order
        }
    
    return app
