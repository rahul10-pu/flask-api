import json
import random
import sys
import uuid

import requests


class RunExpenseTests:
    def __init__(self):
        self.url = sys.argv[1]
        self.run_number = str(uuid.uuid4())
        self.employee_count = 0
        self.vendor_count = 0
        self.setup_urls()
        self.total_score = 0
        self.max_score = 0
        self.request_number = 1

    def setup_urls(self):
        self.add_employee_url = self.url + 'add-employee/'
        self.get_employee_url = self.url + 'get-employee/'
        self.add_vendor_url = self.url + 'add-vendor/'
        self.get_vendor_url = self.url + 'get-vendor/'
        self.add_expense_url = self.url + 'add-expense/'
        self.get_employee_expense_url = self.url + 'get-expense-for-employee/'
        self.get_vendor_expense_url = self.url + 'get-expense-for-vendor/'

    def get_next_employee_code(self, increment=True):
        if increment:
            self.employee_count = self.employee_count + 1

        return 'EMP-{}-{}'.format(self.run_number, self.employee_count)

    def get_next_employee_name(self):
        return 'EMP {}'.format(self.employee_count)

    def get_next_vendor_code(self, increment=True):
        if increment:
            self.vendor_count = self.vendor_count + 1

        return 'VEN-{}-{}'.format(self.run_number, self.vendor_count)

    def get_next_vendor_name(self):
        return 'VEN {}'.format(self.vendor_count)

    def increment_score(self):
        self.total_score += 1

    def test_response(self, response, code, message=None):
        test_score = 0
        test_max_score = 1

        if response.status_code == code:
            self.increment_score()
            test_score += 1

        if message and response.json() == message:
            self.increment_score()
            test_score += 1

        if message:
            test_max_score += 1

        self.max_score += test_max_score

        print('------- Start Request Number #{} -------'.format(
            self.request_number))
        print(
            'Request : {} {}'.format(
                response.request.method,
                response.request.url
            )
        )
        if response.request.method == 'POST':
            print('Request body: {}'.format(
                response.request.body.decode('utf-8')))
        print('Response body: {}'.format(response.content.decode('utf-8')))

        if message:
            print('Expected Response body: {}'.format(
                  json.dumps(message)))

        print('Response Status Code : {}'.format(response.status_code))
        print('Expected Status Code : {}'.format(code))
        print('======= End Request Number #{} ======='.format(
            self.request_number))

        self.request_number += 1

    def test_add_employee(self):
        # Test name not passed.
        response = requests.post(self.add_employee_url, json={})
        self.test_response(response, 400, {'message': 'name not passed.'})

        # Test employee code not passed.
        response = requests.post(
            self.add_employee_url,
            json={'name': self.get_next_employee_name()} 
        )
        self.test_response(
            response,
            400,
            {'message': 'employee_code not passed.'}
        )

        # Test employee code correct.
        code = self.get_next_employee_code()
        response = requests.post(
            self.add_employee_url,
            json={
                'employee_code': code,
                'name': self.get_next_employee_name()
            }
        )
        self.test_response(
            response,
            201,
            {'message': 'employee created.'}
        )

        # Test employee code duplicate.
        response = requests.post(
            self.add_employee_url,
            json={
                'employee_code': code,
                'name': self.get_next_employee_name()
            }
        )
        self.test_response(
            response,
            400,
            {'message': 'duplicate employee_code passed.'}
        )

    def test_get_employee(self):
        # employee code not passed.
        response = requests.get(self.get_employee_url)
        self.test_response(
            response,
            400,
            {'message': 'employee code not passed.'}
        )

        # invalid employee code passed.
        response = requests.get(
            '{}?employee_code=1234'.format(self.get_employee_url)
        )
        self.test_response(
            response,
            400,
            {'message': 'invalid employee code passed.'}
        )

        # valid employee code passed.
        response = requests.get(
            '{}?employee_code={}'.format(
                self.get_employee_url,
                self.get_next_employee_code(False)
            )
        )
        self.test_response(
            response,
            200,
            {
                'employee_code': self.get_next_employee_code(False),
                'name': self.get_next_employee_name()
            }
        )

    def test_add_vendor(self):
        # Test name not passed.
        response = requests.post(self.add_vendor_url, json={})
        self.test_response(response, 400, {'message': 'name not passed.'})

        # Test vendor code not passed.
        response = requests.post(
            self.add_vendor_url,
            json={'name': self.get_next_vendor_name()} 
        )
        self.test_response(
            response,
            400,
            {'message': 'vendor_code not passed.'}
        )

        # Test vendor code correct.
        code = self.get_next_vendor_code()
        response = requests.post(
            self.add_vendor_url,
            json={
                'vendor_code': code,
                'name': self.get_next_vendor_name()
            }
        )
        self.test_response(
            response,
            201,
            {'message': 'vendor created.'}
        )

        # Test vendor code duplicate.
        response = requests.post(
            self.add_vendor_url,
            json={
                'vendor_code': code,
                'name': self.get_next_vendor_name()
            }
        )
        self.test_response(
            response,
            400,
            {'message': 'duplicate vendor_code passed.'}
        )

    def test_get_vendor(self):
        # employee code not passed.
        response = requests.get(self.get_vendor_url)
        self.test_response(
            response,
            400,
            {'message': 'vendor code not passed.'}
        )

        # invalid vendor code passed.
        response = requests.get(
            '{}?vendor_code=1234'.format(self.get_vendor_url)
        )
        self.test_response(
            response,
            400,
            {'message': 'invalid vendor code passed.'}
        )

        # valid vendor code passed.
        response = requests.get(
            '{}?vendor_code={}'.format(
                self.get_vendor_url,
                self.get_next_vendor_code(False)
            )
        )
        self.test_response(
            response,
            200,
            {
                'vendor_code': self.get_next_vendor_code(False),
                'name': self.get_next_vendor_name()
            }
        )

    def test_add_expense(self):
        # No vendor code passed.
        response = requests.post(self.add_expense_url, json={})
        self.test_response(
            response,
            400,
            {'message': 'vendor code not passed.'}
        )

        # No employee code passed.
        response = requests.post(
            self.add_expense_url,
            json={'vendor_code': '1234'}
        )
        self.test_response(
            response,
            400,
            {'message': 'employee code not passed.'}
        )

        # No expense comment passed.
        response = requests.post(
            self.add_expense_url,
            json={'vendor_code': '1234', 'employee_code': '1234'}
        )
        self.test_response(
            response,
            400,
            {'message': 'expense comment not passed.'}
        )

        # Expense done on not passed.
        response = requests.post(
            self.add_expense_url,
            json={
                'vendor_code': '1234',
                'employee_code': '1234',
                'expense_comment': 'Test Comment'
            }
        )
        self.test_response(
            response,
            400,
            {'message': 'expense done on not passed.'}
        )

        # Expense amount not passed.
        response = requests.post(
            self.add_expense_url,
            json={
                'vendor_code': '1234',
                'employee_code': '1234',
                'expense_comment': 'Test Comment',
                'expense_done_on': '1234'
            }
        )
        self.test_response(
            response,
            400,
            {'message': 'expense amount not passed.'}
        )

        # Vendor code invalid.
        response = requests.post(
            self.add_expense_url,
            json={
                'vendor_code': '1234',
                'employee_code': '1234',
                'expense_comment': 'Test Comment',
                'expense_done_on': '1234',
                'expense_amount': '123.45s'
            }
        )
        self.test_response(
            response,
            400,
            {'message': 'vendor code invalid.'}
        )

        # employee code invalid.
        response = requests.post(
            self.add_expense_url,
            json={
                'vendor_code': self.get_next_vendor_code(False),
                'employee_code': '1234',
                'expense_comment': 'Test Comment',
                'expense_done_on': '1234',
                'expense_amount': '123.45s'
            }
        )
        self.test_response(
            response,
            400,
            {'message': 'employee code invalid.'}
        )

        # empty comment provided.
        response = requests.post(
            self.add_expense_url,
            json={
                'vendor_code': self.get_next_vendor_code(False),
                'employee_code': self.get_next_employee_code(False),
                'expense_comment': '',
                'expense_done_on': '1234',
                'expense_amount': '123.45s'
            }
        )
        self.test_response(
            response,
            400,
            {'message': 'empty expense comment provided.'}
        )

        # invalid expense done on date format
        response = requests.post(
            self.add_expense_url,
            json={
                'vendor_code': self.get_next_vendor_code(False),
                'employee_code': self.get_next_employee_code(False),
                'expense_comment': 'Test comment',
                'expense_done_on': '1234',
                'expense_amount': '123.45s'
            }
        )
        self.test_response(
            response,
            400,
            {'message': 'expense done on is not in valid format.'}
        )

        # invalid expense amount format provided
        response = requests.post(
            self.add_expense_url,
            json={
                'vendor_code': self.get_next_vendor_code(False),
                'employee_code': self.get_next_employee_code(False),
                'expense_comment': 'Test comment',
                'expense_done_on': '12-Aug-2019',
                'expense_amount': '123.45s'
            }
        )
        self.test_response(
            response,
            400,
            {'message': 'expense amount is not in valid format.'}
        )

        # invalid expense amount format provided
        response = requests.post(
            self.add_expense_url,
            json={
                'vendor_code': self.get_next_vendor_code(False),
                'employee_code': self.get_next_employee_code(False),
                'expense_comment': 'Test comment',
                'expense_done_on': '12-Aug-2019',
                'expense_amount': '123.45'
            }
        )
        self.test_response(
            response,
            400,
            {'message': 'expense amount not an integer.'}
        )

        # expense created successfully
        response = requests.post(
            self.add_expense_url,
            json={
                'vendor_code': self.get_next_vendor_code(False),
                'employee_code': self.get_next_employee_code(False),
                'expense_comment': 'Test comment',
                'expense_done_on': '12-Aug-2019',
                'expense_amount': '123'
            }
        )
        self.test_response(
            response,
            201,
            {'message': 'expense created.'}
        )

    def test_get_expense_for_employee(self):
        # No employee code passed.
        response = requests.get(self.get_employee_expense_url)
        self.test_response(
            response,
            400,
            {'message': 'employee code not passed.'}
        )

        # Invalid employee code passed.
        response = requests.get(
            '{}?employee_code=1234'.format(self.get_employee_expense_url)
        )
        self.test_response(
            response,
            400,
            {'message': 'invalid employee code passed.'}
        )

        # Valid employee code passed.
        response = requests.get(
            '{}?employee_code={}'.format(
                self.get_employee_expense_url,
                self.get_next_employee_code(False)
            )
        )
        self.test_response(
            response,
            200,
            {
                'name': self.get_next_employee_name(),
                'expenses': [
                    {
                        'vendor': self.get_next_vendor_name(),
                        'expense_comment': 'Test comment',
                        'expense_done_on': '12-Aug-2019',
                        'expense_amount': 123
                    }
                ]
            }
        )

    def test_get_expense_for_vendor(self):
        # No vendor code passed.
        response = requests.get(self.get_vendor_expense_url)
        self.test_response(
            response,
            400,
            {'message': 'vendor code not passed.'}
        )

        # Invalid employee code passed.
        response = requests.get(
            '{}?vendor_code=1234'.format(self.get_vendor_expense_url)
        )
        self.test_response(
            response,
            400,
            {'message': 'invalid vendor code passed.'}
        )

        # Valid vendor code passed.
        response = requests.get(
            '{}?vendor_code={}'.format(
                self.get_vendor_expense_url,
                self.get_next_vendor_code(False)
            )
        )
        self.test_response(
            response,
            200,
            {
                'name': self.get_next_vendor_name(),
                'expenses': [
                    {
                        'employee': self.get_next_employee_name(),
                        'expense_comment': 'Test comment',
                        'expense_done_on': '12-Aug-2019',
                        'expense_amount': 123
                    }
                ]
            }
        )

    def test_overall(self):
        employees = []
        for i in range(3):
            # Create 3 employees
            code = self.get_next_employee_code()
            response = requests.post(
                self.add_employee_url,
                json={
                    'employee_code': code,
                    'name': self.get_next_employee_name()
                }
            )
            self.test_response(response, 201)
            employees.append(code)

        vendors = []
        for i in range(3):
            code = self.get_next_vendor_code()
            response = requests.post(
                self.add_vendor_url,
                json={
                    'vendor_code': code,
                    'name': self.get_next_vendor_name()
                }
            )
            self.test_response(response, 201)
            vendors.append(code)

        employee_expenses = [0, 0, 0]
        vendor_expenses = [0, 0, 0]

        for i in range(18):
            employee_index = random.choice([0, 1, 2])
            vendor_index = random.choice([0, 1, 2])
            expense = int(random.random() * 1000)
            response = requests.post(
                self.add_expense_url,
                json={
                    'employee_code': employees[employee_index],
                    'vendor_code': vendors[vendor_index],
                    'expense_comment': 'Test comment',
                    'expense_done_on': '12-Aug-2019',
                    'expense_amount': expense
                }
            )
            self.test_response(response, 201)
            employee_expenses[employee_index] += expense
            vendor_expenses[vendor_index] += expense

        for i in range(3):
            response = requests.get(
                '{}?employee_code={}'.format(
                    self.get_employee_expense_url,
                    employees[i]
                )
            )
            self.test_response(response, 200)
            total = sum([
                x['expense_amount'] for x in response.json()['expenses']])
            if employee_expenses[i] == total:
                self.total_score += 1
            self.max_score += 1

        for i in range(3):
            response = requests.get(
                '{}?vendor_code={}'.format(
                    self.get_vendor_expense_url,
                    vendors[i]
                )
            )
            self.test_response(response, 200)
            total = sum([
                x['expense_amount'] for x in response.json()['expenses']])
            if vendor_expenses[i] == total:
                self.total_score += 1
            self.max_score += 1

    def print_instructions(self):
        instruction = '''
Usage of the script is `python test.py <your_project_url>`.

Here are some examples to help you determine what should be passed in
the proeject URL:
1. Suppose you have hosted your add-employee URL at
   http://localhost:8000/add-employee then you have to pass
   <your_project_url> as http://localhost:8000/
2. If you have hosted add-employee URL at
   http://127.0.0.1/some-django-app/add-employee then you have to pass
   <your_project_url> as http://localhost:8000/some-django-app/
        '''

        print(instruction)

    def run(self):
        self.print_instructions()
        self.test_add_employee()
        self.test_get_employee()
        self.test_add_vendor()
        self.test_get_vendor()
        self.test_add_expense()
        self.test_get_expense_for_employee()
        self.test_get_expense_for_vendor()
        self.test_overall()
        print('Total Score: ', self.total_score)
        print('Maximum Score: ', self.max_score)

        print(
            'If score is less than maximum score. For each request sent '
            'to your server, the actual request, response received is '
            'printed along with the expected response and status codes. '
            'Verify each request and response body, to increase your score.'
        )


if __name__ == '__main__':
    RunExpenseTests().run()
