#unit testing
import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from flask_jwt_extended import create_access_token
from ..models.orders import Order
class OrderTestCase(unittest.TestCase):
        def setUp(self):
            self.app = create_app(config=config_dict['test'])
        #helps us to create our database
            self.appctx = self.app.app_context()
            self.appctx.push()
            self.client = self.app.test_client()
            db.create_all()
        def tearDown(self):#reset the app
            db.drop_all()
        
            self.appctx.pop()
            self.app = None
            self.client=None
        #getting all orders
        def test_get_all_order(self):
            token = create_access_token(identity='testuser')
            headers ={
                "Authorization": f"Bearer {token}"
                
            }
            response = self.client.get('/order/orders', headers=headers)
            assert response.status_code == 200
            assert response.json ==[]
        #create  all orders
        def test_create_order(self):
            token = create_access_token(identity='testuser')
            headers ={
                "Authorization": f"Bearer {token}"
                
            }
            data = {
                'size':'EXTRA_LARGE',
                'quantity': 2,
                'flavour':'peperoni'
            }
            response = self.client.post('/order/orders', json=data, headers=headers)
            #order = Order.query.filter_by(id=1).first()
            order = Order.query.all()
            assert len(order) == 1
            assert response.json['size'] == 'Sizes.EXTRA_LARGE'
            order_id = order[0].id
            assert order_id ==1
            assert response.status_code == 201
        #get an order by id
        def test_get_a_single_order_by_id(self):
            token = create_access_token(identity='testuser')
            headers ={
                "Authorization": f"Bearer {token}"
                
            }
          
            #whenever we are passing in an id we use a 404
            response = self.client.get('/order/orders/<int:order_id>', headers=headers)
            
            assert response.status_code == 404
        #update an order 
        def test_update_order_by_id(self):
            token = create_access_token(identity='testuser')
            headers ={
                "Authorization": f"Bearer {token}"
                
            }
            data = {
                'size':'SMALL',
                'quantity': 3,
                'flavour':'yam'
            }
            
          
            #whenever we are passing in an id we use a 404
            response = self.client.put('/order/orders/<int:order_id>', json=data, headers=headers)
           
            assert response.status_code == 404
        #delete an order by id
        def test_delete_order_by_id(self):
            token = create_access_token(identity='testuser')
            headers ={
                "Authorization": f"Bearer {token}"
                
            }
            response = self.client.delete('/order/orders/<int:order_id>',  headers=headers)
            order = Order.query.all()
            assert len(order) == 0
            assert response.status_code == 404
            
            
            
        def test_update_an_order_status_by_id(self):
            token = create_access_token(identity='testuser')
            headers ={
                "Authorization": f"Bearer {token}"
                
            }
            data ={
                'order_status':'DELIVERED'
            }
        
            response = self.client.patch('/order/orders/status/<int:order_id>',json=data ,headers=headers)
            #order = Order.query.all()
            #assert response.json['order_status'] == 'OrderStatus.DELIVERED'
            
            assert response.status_code == 404
        
        
     