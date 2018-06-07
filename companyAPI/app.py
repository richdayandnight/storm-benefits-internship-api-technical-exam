from flask import Flask, request, jsonify, abort, make_response
from companyAPI.database import db_session
from companyAPI.models import Company
from sqlalchemy import exc

# initialize Flask app
app = Flask(__name__)


# GET all company records from the index route
@app.route('/', methods=['GET'])
def index():
    companies = Company.query.all()
    return jsonify(Companies=[Company.serialize() for Company in companies])


# POST/Insert new company records at the index route
@app.route('/', methods=['POST'])
def create_company():
    if not request.json:
        abort(400)
    content = request.get_json()
    if type(content['name']) != str:
        return make_response(jsonify({'error':'Company name should be a string'}), 400)
    # used a try - except to know if the json sent by the client
    # is a json object or a json array
    '''try:
        i = 0
        while i != len(content):
            # Add the company records to the database
            company_temp = Company(name=content[i]['name'],
                                   employees_num=content[i]['employees_num'],
                                   location=content[i]['location'],
                                   email=content[i]['email'],
                                   industry=content[i]['industry'])
            db_session.add(company_temp)
            db_session.commit()
            i = i + 1
        return jsonify(content), 201'''

    # Add the company record to the database

    #exists = Company.query(Company.name).filter_by(name=content['name'])).scalar()
    try:
        company_temp = Company(name=content['name'],
                               employees_num=content['employees_num'],
                               location=content['location'],
                               email=content['email'],
                               industry=content['industry'])
        db_session.add(company_temp)
        db_session.commit()
        return jsonify(content), 201
    except exc.IntegrityError as e:
        return make_response(jsonify({'error': 'Duplicate company name'}), 400)


# GET a specific company record through their company_id (primary key)
@app.route('/<int:company_id>', methods=['GET'])
def get_company(company_id):
    companies = Company.query.all()
    company = [company for company in companies if company.id == company_id]
    if len(company) == 0:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(Company=Company.serialize(company[0]))


# PUT/Update a specific company record through their company_id (primary key)
@app.route('/<int:company_id>', methods=['PUT'])
def update_company(company_id):
    companies = Company.query.all()
    company = [company for company in companies if company.id == company_id]
    # Input validation of json and checking if there's a company_id with the id == company_id
    if len(company) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) != str:
        return make_response(jsonify({'error': 'Company name not a string'}), 400)
    if 'employees_num' in request.json and type(request.json['employees_num']) is not int:
        return make_response(jsonify({'error': 'Employees_num not an int'}), 400)
    if 'location' in request.json and type(request.json['location']) is not str:
        return make_response(jsonify({'error': 'Location not a string'}), 400)
    if 'email' in request.json and type(request.json['email']) is not str:
        return make_response(jsonify({'error': 'Email not a string'}), 400)
    if 'industry' in request.json and type(request.json['industry']) is not str:
        return make_response(jsonify({'error': 'Industry not a string'}), 400)
    content = request.get_json()
    # updating the requested company record
    try:
        queried_company = Company.query.get(company_id)
        queried_company.name = content['name']
        queried_company.employees_num = content['employees_num']
        queried_company.location = content['location']
        queried_company.email = content['email']
        queried_company.industry = content['industry']
        db_session.commit()
        return jsonify(content)
    except exc.IntegrityError as e:
        return make_response(jsonify({'error': 'Duplicate company name'}), 400)

# DELETE a specific company record through their company_id (primary key)
@app.route('/<int:company_id>', methods=['DELETE'])
def delete_company(company_id):
    companies = Company.query.all()
    company = [company for company in companies if company.id == company_id]
    if len(company) == 0:
        abort(404)
    Company.query.filter_by(id=company_id).delete()
    db_session.commit()
    return make_response(jsonify({'Delete': True}), 201)

# SEARCH a company using filter and 'like'
@app.route('/search', methods=['POST'])
def search():
    if not request.json:
        abort(400)
    if 'value' in request.json and type(request.json['value']) is not str:
        abort(400)
    content = request.get_json()
    companies = Company.query.filter(Company.name.like('%' + content['value']+ '%'))
    return jsonify(Companies=[Company.serialize() for Company in companies])

# Act as an error handler when a page is not found
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# Shutdown connection with database after the connection teardown
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# main
if __name__ == '__main__':
    app.run()
