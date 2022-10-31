from unicodedata import name
from flask import Flask,request, flash, url_for, redirect, render_template, Response, jsonify
from flask_restful import Api, Resource, reqparse
from models import CustomerModel, db

app = Flask(__name__, template_folder='template')

#for cors error
from flask_cors import CORS, cross_origin
CORS(app)

#db connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db.init_app(app)

#to create table
@app.before_first_request
def create_table():
    db.create_all()

class CustomersView(Resource):
    def get(self):
        customers = CustomerModel.query.all()
        return { 'Customers':list(x.json() for x in customers)}
    
    def post(self):
        request_data = request.get_json()

        ncustomer_name = request_data["name"]
        ncustomer_ic = request_data["ic"]
        ncustomer_phone = request_data["phone"]
        ncustomer_email = request_data["email"]

        new_customer = CustomerModel(name=ncustomer_name, ic=ncustomer_ic, phone=ncustomer_phone, email=ncustomer_email)
        db.session.add(new_customer)
        db.session.commit()
        return new_customer.json()
       

class SingleCustomerView(Resource):

    def get(self,id):
        customer = CustomerModel.query.filter_by(id=id).first()
        if customer:
            return customer.json()
        return {'message: product id is no found'}, 404

    def put(self,id):
        data = request.get_json()
        customer = CustomerModel.query.filter_by(id=id).first()

        if customer:
            customer.name = data["name"]
            customer.ic = data["ic"]
            customer.phone = data["phone"]
            customer.email = data["email"]
        else:
            customer = CustomerModel(id=id, **data)
        
        db.session.add(customer)
        db.session.commit()

        return customer.json()
    
    def delete(self,id):
        customer = CustomerModel.query.filter_by(id=id).first()
        if customer:
            db.session.delete(customer)
            db.session.commit()
            return {'message': 'deleted'}
        return {'message: product id is no found'}, 404


#api
api.add_resource(CustomersView, '/customers')
api.add_resource(SingleCustomerView, '/customers/<int:id>')

app.debug = True
if __name__ == '__main__':
    app.run(host='localhost', port=5000)
