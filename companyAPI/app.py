"""
.. module:: app
   :platform: Unix, Windows
   :synopsis: A useful module indeed.

.. moduleauthor:: Rich Yap


"""

from flask import Flask, request, jsonify, abort, make_response
from companyAPI.database import db_session
from companyAPI.models import Company
from sqlalchemy import exc

# initialize Flask app
app = Flask(__name__)


# GET all company records from the index route
@app.route('/', methods=['GET'])
def index():
    """
        **Get List of Companies**

        This function allows user to get a list of the companies with their respective information.

        :return: company information of all companies in json and http status code

        - Example::

              curl -X GET http://127.0.0.1:5000/ -H 'cache-control: no-cache' -H 'content-type: application/json'

        - Expected Success Response::

            HTTP Status Code: 200

            {
            "Companies": [
                    {
                        "email": "feedback@jollibee.com",
                        "employees_num": 9999,
                        "id": 1,
                        "industry": "Food",
                        "location": "Philippines",
                        "name": "Jollibee Foods Corporation"
                    },
                    {
                        "email": "storm@storm.com",
                        "employees_num": 100,
                        "id": 3,
                        "industry": "Technology",
                        "location": "Philippines",
                        "name": "Storm"
                    },
                    {
                        "email": "info@company.com",
                        "employees_num": 100,
                        "id": 6,
                        "industry": "Franchising",
                        "location": "Philippines",
                        "name": "Company_tempname"
                    }
                ]
            }

    """
    companies = Company.query.all()
    return make_response(jsonify(Companies=[Company.serialize() for Company in companies]), 200)


# POST/Insert new company records at the index route
@app.route('/', methods=['POST'])
def create_company():
    """
        **Create company**

        This function allows user to create(post) a company.

        :return: company information of the company added by user in json and http status code

        - Example::

            curl -X POST http://127.0.0.1:5000/ -H 'cache-control: no-cache' -H 'content-type: application/json' -H 'postman-token: c0db7776-aa16-7702-7467-7a3bca90a5a7' \
            -d '{
            "name": "Company_tempname",
            "employees_num": 100,
            "email": "info@company.com",
            "location": "Philippines",
            "industry": "Franchising"
            }'

        - Expected Success Response::

            HTTP Status Code: 201

            {
              "email": "info@company.com",
              "employees_num": 100,
              "industry": "Franchising",
              "location": "Philippines",
              "name": "Company_tempname"
            }

        - Expected Fail Response::

            HTTP Status Code: 400
            {'error': 'Duplicate company name'}

    """
    if not request.json:
        abort(400)
    content = request.get_json()
    if type(content['name']) != str:
        return make_response(jsonify({'error':'Company name should be a string'}), 400)
    # used a try - except to know if the json sent by the client
    # is a json object or a json array
    #try:
    #    i = 0
    #    while i != len(content):
    #        # Add the company records to the database
    #        company_temp = Company(name=content[i]['name'],
    #                               employees_num=content[i]['employees_num'],
    #                               location=content[i]['location'],
    #                               email=content[i]['email'],
    #                               industry=content[i]['industry'])
    #        db_session.add(company_temp)
    #        db_session.commit()
    #        i = i + 1
    #    return jsonify(content), 201'''
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
    """
        **Get information of a specific company**

        This function allows user to get a specific company's information through their company_id.

        :param company_id: id of the company
        :type company_id: int
        :return: company information of the company accessed by user in json and http status code

        - Example::

            curl -X GET http://127.0.0.1:5000/1 -H 'cache-control: no-cache' -H 'content-type: application/json'

        - Expected Success Response::

            HTTP Status Code: 200

            {
            "Company": {
                    "email": "feedback@jollibee.com",
                    "employees_num": 9999,
                    "id": 1,
                    "industry": "Food",
                    "location": "Philippines",
                    "name": "Jollibee Foods Corporation"
                }
            }

        - Expected Fail Response::

            HTTP Status Code: 404

            {'error': 'Not found'}

    """
    companies = Company.query.all()
    company = [company for company in companies if company.id == company_id]
    if len(company) == 0:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return make_response(jsonify(Company=Company.serialize(company[0])), 200)


# PUT/Update a specific company record through their company_id (primary key)
@app.route('/<int:company_id>', methods=['PUT'])
def update_company(company_id):
    """
        **Update information of a specific company**

        This function allows user to get a specific company's information through their company_id.

        :param company_id: id of the company
        :type company_id: int
        :return: company information of the company updated by user in json and http status code

        - Example::

            curl -X PUT http://127.0.0.1:5000/2 -H 'cache-control: no-cache' -H 'content-type: application/json' -H 'postman-token: 423a3668-cdaf-5581-5465-0ad4ed1a50c2'
            -d '{
                "email": "google_drive@gmail.com",
                "employees_num": 9999,
                "industry": "Software",
                "location": "USA",
                "name": "Google Drive"
            }'

        - Expected Success Response::

            HTTP Status Code: 200

            {
                "email": "google_drive@gmail.com",
                "employees_num": 9999,
                "industry": "Software",
                "location": "USA",
                "name": "Google Drive"
            }

        - Expected Fail Response::

            HTTP Status Code: 404

            {'error': 'Not found'}

            or

            HTTP Status Code: 404

            {'error': 'Duplicate company name'}

    """
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
        return make_response(jsonify(content), 200)
    except exc.IntegrityError as e:
        return make_response(jsonify({'error': 'Duplicate company name'}), 400)

# DELETE a specific company record through their company_id (primary key)
@app.route('/<int:company_id>', methods=['DELETE'])
def delete_company(company_id):
    """
        **Delete company**

        This function allows user to delete a company.

        :param company_id: id of the company
        :type company_id: int
        :return: delete status in json and http status code

        - Example::

            curl -X DELETE http://127.0.0.1:5000/3 -H 'cache-control: no-cache' -H 'content-type: application/json'

        - Expected Success Response::

            HTTP Status Code: 200

            {
                "Delete": true
            }

        - Expected Fail Response::

            HTTP Status Code: 404

            {'error': 'Not found'}

    """
    companies = Company.query.all()
    company = [company for company in companies if company.id == company_id]
    if len(company) == 0:
        abort(404)
    Company.query.filter_by(id=company_id).delete()
    db_session.commit()
    return make_response(jsonify({'Delete': True}), 200)

# SEARCH a company using filter and 'like'
@app.route('/search', methods=['POST'])
def search():
    """
        **Search company**

        This function allows user to search for companies through substring search of company names.

        :return: searched companies in json and http status code

        - Example::

            curl -X POST http://127.0.0.1:5000/search -H 'cache-control: no-cache' -H 'content-type: application/json' -H 'postman-token: f2c027be-acda-3a8e-51b6-3b64036df882'
            -d '{
                "value": "Jollibee"
            }'

        - Expected Success Response::

            HTTP Status Code: 200

            {
                "Companies": [
                    {
                        "email": "feedback@jollibee.com",
                        "employees_num": 9999,
                        "id": 1,
                        "industry": "Food",
                        "location": "Philippines",
                        "name": "Jollibee Foods Corporation"
                    }
                ]
            }

    """
    if not request.json:
        abort(400)
    if 'value' in request.json and type(request.json['value']) is not str:
        abort(400)
    content = request.get_json()
    companies = Company.query.filter(Company.name.like('%' + content['value']+ '%'))
    return make_response(jsonify(Companies=[Company.serialize() for Company in companies]), 200)

# Act as an error handler when a page is not found
@app.errorhandler(404)
def not_found():
    """
        **Error handler**

        This function returns a not found error in json when called.

        :return: not found error in json

    """
    return make_response(jsonify({'error': 'Not found'}), 404)


# Shutdown connection with database after the connection teardown
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# main
if __name__ == '__main__':
    app.run()
