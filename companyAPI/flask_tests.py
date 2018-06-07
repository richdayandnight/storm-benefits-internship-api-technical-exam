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
        Company = {"Company": sample_data}
        # data = json.loads(response.get_data(as_text=True))
        # for key in data['Company']:
        # self.assertEqual(data['Company'][key], sample_data[key])
        self.assertEqual(json.loads(response.get_data().decode()), Company)
        self.assertEqual(response.status_code, 200)

    # test Getting a company information from a non existing company
    # in this function, we try to get the information from the company with id = 999
    def test_get_empty_company(self):
        print("Test_get_empty_company")
        response = self.app.get("/999")
        sample_data = {
            "error": "Not found"
        }
        # print(sample_data['email'])
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], sample_data["error"])

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
        error = {"error": "Duplicate company name"}
        try:
            self.assertEqual(json.loads(response.get_data().decode()), sample_data)
        #  the following exception should be commented in real testing
        except Exception as e:
            self.assertEqual(json.loads(response.get_data().decode()), error)

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
        error = {"error": "Duplicate company name"}
        response = self.app.post('/',
                                 data=json.dumps(sample_data),
                                 content_type='application/json')
        self.assertEqual(json.loads(response.get_data().decode()), error)

    # test Deleting a company information
    # in this function, we try to delete an existing company (where company id = 2)
    def test_delete_company(self):
        print("Test_delete_company")
        company_id = 2
        response = self.app.delete('/' + str(company_id))
        data = json.loads(response.get_data(as_text=True))
        error = {"error": "Not found"}
        delete = {"Delete": True}
        try:
            self.assertEqual(json.loads(response.get_data().decode()), delete)
        #  the following exception should be commented in real testing
        except Exception as e:
            self.assertEqual(json.loads(response.get_data().decode()), error)

    # test Deleting a company information
    # in this function, we try to delete a non-existing company (where company id = 999)
    def test_delete_nonexisting_company(self):
        print("Test_delete_nonexisting_company")
        company_id = 999
        response = self.app.delete('/' + str(company_id))
        error = {"error": "Not found"}
        self.assertEqual(json.loads(response.get_data().decode()), error)

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
        self.assertEqual(json.loads(response.get_data().decode()), sample_data)

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
        error = {"error": "Duplicate company name"}
        response = self.app.put('/' + str(company_id),
                                data=json.dumps(sample_data),
                                content_type='application/json')
        self.assertEqual(json.loads(response.get_data().decode()), error)

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
        error = {"error": "Company name not a string"}
        response = self.app.put('/' + str(company_id),
                                data=json.dumps(sample_data),
                                content_type='application/json')
        self.assertEqual(json.loads(response.get_data().decode()), error)

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
        error = {
            "error": "Not found"
        }
        response = self.app.put('/' + str(company_id),
                                data=json.dumps(sample_data),
                                content_type='application/json')
        self.assertEqual(json.loads(response.get_data().decode()), error)
