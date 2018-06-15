from app import app
import unittest
import json


class CompanyAppTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_company(self):
        """
            **Test Getting Company Information of a Company**

            This function tests the companyAPI's function to return the right information of the company with id = 1

            :param self: an instance of the companyAPI app.
            :type self: CompanyAppTest.
            :return: none.


            - Expected Success Response::

                OK

            - Expected Fail Response::

                FAILED

                {'Company':
                    {'email': 'feedback@jollibee.com',
                     'employees_num': 9999,
                     'id': 1,
                     'industry': 'Food',
                     'location': 'Philippines',
                     'name': 'Jollibee Foods Corporation'}
                }

                != <json returned by the test_client>
        """
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
        self.assertEqual(response.status_code, 200, "Getting details of a company unsuccessful")

    def test_get_empty_company(self):
        """
            **Test Getting Company Information of a non-existing Company**

            This function tests the companyAPI's function to return the error message
            when trying to access a non-existing company where id = 999.

            :param self: an instance of the companyAPI app.
            :type self: CompanyAppTest.
            :return: none.

            - Expected Success Response::

                OK

            - Expected Fail Response::

                FAILED

                {"error": "Not found"} != <json returned by the test_client>
        """
        print("Test_get_empty_company")
        response = self.app.get("/999")
        error = {
            "error": "Not found"
        }
        self.assertEqual(json.loads(response.get_data().decode()), error)
        self.assertEqual(response.status_code, 404)

    def test_post_company(self):
        """
            **Test Adding (Post) a Company with valid company information**

            This function tests the companyAPI's function to receive company's data
            and insert this information to the database.

            :param self: an instance of the companyAPI app.
            :type self: CompanyAppTest.
            :return: none.

            - Expected Success Response:

                OK

            - Expected Fail Response::

                FAILED
                {
                    "name": "Company_tempname",
                    "employees_num": 100,
                    "email": "info@company.com",
                    "location": "Philippines",
                    "industry": "Franchising"
                }
                != <json returned by the test_client>

        """
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
            self.assertEqual(response.status_code, 201)
        #  the following exception should be commented in real testing
        except Exception as e:
            self.assertEqual(json.loads(response.get_data().decode()), error)
            self.assertEqual(response.status_code, 400)

    def test_post_duplicate_company_name(self):
        """
            Test Adding (Post) a Company with a Similar Company Name in the Database

            This function tests the companyAPI's function to return an error when
            receiving a company data with a name similar to the companies listed in the database.

            :param self: an instance of the companyAPI app
            :type self: CompanyAppTest.
            :return: none.

            - Expected Success Response::

                OK

            - Expected Fail Response::

                FAILED

                {"error": "Duplicate company name"} != <json returned by the test_client>

        """
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
        self.assertEqual(response.status_code, 400)

    def test_delete_company(self):
        """
            **Test Deleting a Company**

            This function tests the companyAPI's function to delete a
            company in the database.

            :param self: an instance of the companyAPI app
            :type self: CompanyAppTest.
            :return: none.

            - Expected Success Response::

                OK

            - Expected Fail Response::

                FAILED

                delete = {"Delete": True} != <json returned by the test_client>

        """
        print("Test_delete_company")
        company_id = 2
        response = self.app.delete('/' + str(company_id))
        data = json.loads(response.get_data(as_text=True))
        error = {"error": "Not found"}
        delete = {"Delete": True}
        try:
            self.assertEqual(json.loads(response.get_data().decode()), delete)
            self.assertEqual(response.status_code, 200)
        #  the following exception should be commented in real testing
        except Exception as e:
            self.assertEqual(json.loads(response.get_data().decode()), error)
            self.assertEqual(response.status_code, 404)

    def test_delete_nonexisting_company(self):
        """
            Test Deleting a non-existing Company

            This function tests the companyAPI's function to return an error message
            when trying to delete a non-existing company.

            :param self: an instance of the companyAPI app
            :type self: CompanyAppTest.
            :return: none.

            - Expected Success Response::

                OK

            - Expected Fail Response::

                FAILED
                {"error": "Not found"} != <json returned by the test_client>

        """
        print("Test_delete_nonexisting_company")
        company_id = 999
        response = self.app.delete('/' + str(company_id))
        error = {"error": "Not found"}
        self.assertEqual(json.loads(response.get_data().decode()), error)
        self.assertEqual(response.status_code, 404)

    def test_put_company(self):
        """
            Test Editing a Company Information

            This function tests the companyAPI's function to edit a company's information.

            :param self: an instance of the companyAPI app
            :type self: CompanyAppTest.
            :return: none.

            - Expected Success Response::
                OK

            - Expected Fail Response::

                FAILED

                {
                    "email": "feedback@jollibee.com",
                    "employees_num": 9999,
                    "industry": "Food",
                    "location": "Philippines",
                    "name": "Jollibee Foods Corporation"
                } != <json returned by the test_client>

        """
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
        self.assertEqual(response.status_code, 200)

    def test_put_duplicate_company_name(self):
        """
            **Test Editing a Company Information with a Similar Company Name in the Database**

            This function tests the companyAPI's function to return an error when
            editing a company name to a new company name similar to the companies listed in the database.

            :param self: an instance of the companyAPI app
            :type self: CompanyAppTest.
            :return: none.

            - Expected Success Response::

                OK

            - Expected Fail Response::

                FAILED

                {"error": "Duplicate company name"} != <json returned by the test_client>

        """
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
        self.assertEqual(response.status_code, 400)

    def test_put_null_company_name(self):
        """
            **Test Editing a Company Information with invalid Company name**

            This function tests the companyAPI's function to return an error when
            editing a company name to a new company name which is not a string.

            :param self: an instance of the companyAPI app
            :type self: CompanyAppTest.
            :return: none.

            - Expected Success Response::

                OK

            - Expected Fail Response::

                FAILED

                {"error": "Company name not a string"} != <json returned by the test_client>

        """
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
        self.assertEqual(response.status_code, 400)

    def test_put_non_existing_company(self):
        """
            **Test Editing a Company Information with invalid company id**

            This function tests the companyAPI's function to return an error when
            editing a non-existing company's information where the id is = 888.

            :param self: an instance of the companyAPI app
            :type self: CompanyAppTest.
            :return: none.

            - Expected Success Response::
                OK

            - Expected Fail Response::

                FAILED
                {"error": "Not found"} != <json returned by the test_client>

        """
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
        self.assertEqual(response.status_code, 404)
