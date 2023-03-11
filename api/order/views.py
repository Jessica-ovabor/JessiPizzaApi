
from flask_restx import Namespace,Resource,fields
from ..models.orders import Order
from ..models.users import User
from http import HTTPStatus
from ..utils import db
from flask_jwt_extended import jwt_required,get_jwt_identity


order_namespace =Namespace("order" , description="for name space order")
order_model =order_namespace.model(
    'Order', {
        
        'id':fields.Integer(description='An id'),
        'flavour':fields.String(description='flavour', required=True),
        'quantity':fields.Integer(description='Quantity', required=True),
        'size':fields.String(description='Size of an order', required=True, enum=['SMALL','MEDIUM','LARGE','EXTRA_LARGE'] 
        ),
        'order_status':fields.String(description='The status of our order',required=True,enum=['PENDING','IN_TRANSIT','DELIVERED']
        )
    }
)
#update
order_status_model= order_namespace.model(
    'OrderStatus',{
        'order_status':fields.String(required=True,description="Order Status",enum=['PENDING','IN_TRANSIT','DELIVERED']
        )
    })
    
     

@order_namespace.route('/orders')
class OrderGetCreate(Resource):
    #we dont need the expect here because it is get request
    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(
        description='Get all order'
    )
    #this protect the route
    @jwt_required()
    def get(self):
        """
        Get all orders
        """
        #querying the database and getting all orders
        orders = Order.query.all()
        return orders , HTTPStatus.OK
    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(
        description='place all order'
    )
    @jwt_required()
    def post(self):
        """
        Create or post all orders
        """
        #payload gives all the data we need i.e it gives us all the information a user enters even if it is not in the database
        username =get_jwt_identity()
        current_user = User.query.filter_by(username=username).first()
        #current_user = User.query.filter_by(username=username).first()
        data = order_namespace.payload
         
        new_order= Order(
            size = data['size'],
            quantity=data['quantity'],
            flavour=data['flavour']
        )
        new_order.user = current_user
        new_order.save()
        
        return new_order, HTTPStatus.CREATED
 
        
@order_namespace.route('/orders/<int:order_id>')
class GetUpdateDelete(Resource):
    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(
        description='retrieve an order by id'
    )
    @jwt_required()
    def get(self,order_id):
        
        '''
        retrieving order by id
        '''
        order = Order.get_by_id(order_id)
        return order, HTTPStatus.OK
        #post request uses the created


    @order_namespace.expect(order_model)  
    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(
        description='update an order by id',
        params ={
            'order_id':'An ID to update order'  
            }
    )
    @jwt_required() 
    def put(self,order_id):
        '''
       update order by id
        '''
        order_to_update = Order.get_by_id(order_id)
        data = order_namespace.payload
        order_to_update.quantity=data['quantity']
        order_to_update.size=data['size']
        order_to_update.flavour=data['flavour']#or data.quantity
        
        
        db.session.commit()
        
        return order_to_update,HTTPStatus.OK
    @order_namespace.doc(
        description='delete an order by id'
    )
    @jwt_required()   
    def delete(self,order_id):
    
        #delete order by id
        order_to_delete = Order.get_by_id(order_id)
        order_to_delete.delete
        {'message': "Deleted successfully"},HTTPStatus.OK
#get specific order by user
@order_namespace.route('/user/<int:user_id>/orders/<int:order_id>')
class GetSpecificOrderByUser(Resource):
    @order_namespace.marshal_list_with(order_model)
    @order_namespace.doc(
        description='Get user specific order by id',
        param = {
            'order_id':'An ID for order',
        }
    )
    @jwt_required()
    def get(self,user_id,order_id):
        """
        Get a user specific order
        """
        user = User.get_by_id(user_id)
        #it filters first by the order_id  and checks with or map with if the particular user = to the person that created the order
        order =Order.query.filter_by(id=order_id).filter_by(user=user).first()
        
        return order, HTTPStatus.OK
        
         
@order_namespace.route('/user/<int:user_id>/orders')
class UserOrder(Resource):
    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(
        description='Get all user order by user id',
        params={
            'user_id':'An ID for user order'
            }
    )
    @jwt_required()
    def get(self,user_id):
        """
        Get all user order
        """
        user = User.get_by_id(user_id)
        orders = user.order
        
        return orders, HTTPStatus.OK
        
@order_namespace.route('/orders/status/<int:order_id>')

class UpdateOrderStatus(Resource):
    @order_namespace.expect(order_status_model)
    @order_namespace.marshal_with(order_model)  
    @order_namespace.doc(
        description='update order status by order id',
        params={
            'order_id':'An ID for order'
        }
    )
    @order_namespace.doc(
    description='update order status',
    params={
            'order_id':'An ID for order'
        }
    )
    @jwt_required()
    def patch(self,order_id):
        """
        update an order status
        """
        data = order_namespace.payload
        order_to_update = Order.get_by_id(order_id)
        
        order_to_update.order_status = data['order_status']
        db.session.commit()
        
        return order_to_update, HTTPStatus.OK