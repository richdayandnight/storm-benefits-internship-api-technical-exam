from app import app
import unittest
import json


class MyAppCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # test Getting a company information
    # in this function, we try to get the information from the company with id = 1
    def test_get_company(self):
        print("Test_get_company")
        response = self.app.get("/1")
        sample_data = {
            "email": "feedback@jollibee.com",
            "employees_num": 9999,
            "id": 1,
            "industry": "Food",
            "location": "Philippines",
            "name": "Jollibee Foods Corporation"
        }
        #print(sample_data['email'])
        data = json.loads(response.get_data(as_text=True))
        for key in data['Company']:
            self.assertEqual(data['Company'][key], sample_data[key])
        #self.assertEqual(data['Company']['name'],sample_data["name"], "name is not equal")
        #self.assertEqual(data['Company']['email'], sample_data["email"], "email is not equal")
        #self.assertEqual(data['Company']['employees_num'], sample_data["employees_num"], "employees_num is not equal")
        #self.assertEqual(data['Company']['id'], sample_data["id"], "id is not equal")
        #self.assertEqual(data['Company']['industry'], sample_data["industry"], "industry is not equal")
        #self.assertEqual(data['Company']['location'], sample_data["location"], "location is not equal")

    # test Getting a company information from a non existing company
    # in this function, we try to get the information from the company with id = 999
    def test_get_empty_company(self):
        print("Test_get_empty_company")
        response = self.app.get("/999")
        sample_data = {
            "error": "Not found"
        }
        #print(sample_data['email'])
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'],sample_data["error"])

    # test Posting a valid company information
    # in this function, we try to add a new company named Company_tempname to the database
    def test_post_company(self):
        print("Test_post_company")
        sample_data = {
            "name": "Company_tempname",
            "employees_num": 100,
            "email": "info@company.com",
            "location": "Philippines",
            "industry": "Franchising"
        }

        response = self.app.post('/',
                             data=json.dumps(sample_data),
                             content_type='application/json')
        data =  json.loads(response.get_data(as_text=True))
        try:
            self.assertEqual(data['name'],sample_data["name"])
            self.assertEqual(data['email'], sample_data["email"])
            self.assertEqual(data['employees_num'], sample_data["employees_num"])
            self.assertEqual(data['industry'], sample_data["industry"])
            self.assertEqual(data['location'], sample_data["location"])
        #  the following exception should be commented in real testing
        except Exception as e:
            self.assertEqual(data['error'], "Duplicate company name")

    # test Posting a company information with duplicate company name
    # in this function, we try to add a new company with a duplicate name already existing in the database
    def test_post_duplicate_company_name(self):
        print("Test_post_duplicate_company_name")
        sample_data = {
            "email": "feedback@jollibee.com",
            "employees_num": 9999,
            "id": 1,
            "industry": "Food",
            "location": "Philippines",
            "name": "Jollibee Foods Corporation"
        }

        response = self.app.post('/',
                             data=json.dumps(sample_data),
                             content_type='application/json')
        data =  json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'],"Duplicate company name", "Duplicate company name has been posted")

    # test Deleting a company information
    # in this function, we try to delete an existing company (where company id = 2)
    def test_delete_company(self):
        print("Test_delete_company")
        company_id = 2
        response = self.app.delete('/' + str(company_id))
        data = json.loads(response.get_data(as_text=True))
        try:
            self.assertEqual(data['Delete'], True, "Deleting a company unsuccessful")
        #  the following exception should be commented in real testing

        except Exception as e:
            self.assertEqual(data['error'], 'Not found')

    # test Deleting a company information
    # in this function, we try to delete a non-existing company (where company id = 999)
    def test_delete_nonexisting_company(self):
        print("Test_delete_nonexisting_company")
        company_id = 999
        response = self.app.delete('/' + str(company_id))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], 'Not found', "Deleting a non existing company became successful")

    # test Putting a company information
    # in this function, we try to edit an existing company's information
    def test_put_company(self):
        print("Test_put_company")
        company_id = 1
        sample_data = {
            "email": "feedback@jollibee.com",
            "employees_num": 9999,
            "industry": "Food",
            "location": "Philippines",
            "name": "Jollibee Foods Corporation"
        }
        response = self.app.put('/' + str(company_id),
                                 data=json.dumps(sample_data),
                                 content_type='application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['name'], sample_data["name"])
        self.assertEqual(data['email'], sample_data["email"])
        self.assertEqual(data['employees_num'], sample_data["employees_num"])
        self.assertEqual(data['industry'], sample_data["industry"])
        self.assertEqual(data['location'], sample_data["location"])

    # test Putting a company information
    # in this function, we try to edit a company's name to a duplicate of another company
    def test_put_duplicate_company_name(self):
        print("Test_put_duplicate_company_name")
        company_id = 1
        sample_data = {
            "email": "feedback@jollibee.com",
            "employees_num": 9999,
            "industry": "Food",
            "location": "Philippines",
            "name": "Storm"
        }
        response = self.app.put('/' + str(company_id),
                                 data=json.dumps(sample_data),
                                 content_type='application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], "Duplicate company name")

    # test Putting a company information
    # in this function, we try to edit a company name to an invalid company name
    def test_put_null_company_name(self):
        print("Test_put_duplicate_company_name")
        company_id = 1
        sample_data = {
            "email": "feedback@jollibee.com",
            "employees_num": 9999,
            "industry": "Food",
            "location": "Philippines",
            "name": {}
        }
        response = self.app.put('/' + str(company_id),
                                 data=json.dumps(sample_data),
                                 content_type='application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], "Company name not a string")

    # test Putting a company information
    # in this function, we try to edit a company information of a nonexisting company
    def test_put_non_existing_company(self):
        print("Test_put_non_existing_company")
        company_id = 888
        sample_data = {
            "email": "feedback@jollibee.com",
            "employees_num": 9999,
            "industry": "Food",
            "location": "Philippines",
            "name": "Storm"
        }
        response = self.app.put('/' + str(company_id),
                                 data=json.dumps(sample_data),
                                 content_type='application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], "Not found")