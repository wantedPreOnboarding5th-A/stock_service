import json
import jwt
from django.test import TestCase
from django.test import Client
from requests import RequestException
from user.models import User
from transfer.models import Transfer
from invest.models import Account 
from datetime import datetime
from django.conf import settings
from transfer.enums import TransferStatus


class TransferAPITest(TestCase):
    def setUp(self):
        User.objects.create(
            id = 1,
            name = "kim",
            email = "kim@gamil.com",
            password = "kim12345"
        )


        Account.objects.create(
            id = 1,
            user = User.objects.get(id=1),
            brokerage ="하나은행",
            number = "1234512345123",
            name = "계좌1",
            investment_principal = 100000
        )


    def tearDown(self):
        User.objects.all().delete()
        Account.objects.all().delete()
        Transfer.objects.all().delete()


    def test_success_Transfer_post(self):
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        data = {
                "id":1,
                "user_name": "kim",
                "account_number":"1234512345123",
                "transfer_amount" : 5000
                }
        
        headers     = {'HTTP_AUTHORIZATION' : token}
        response = client.post('/transfer/', json.dumps(data),content_type='application/json', **headers)
        self.assertEqual(response.json(), {"transfer_identifier": 3})
        self.assertEqual(response.status_code, 201)


    def test_fail_Transfer_TransferSchema_invalid_error_post(self):
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        data = {
                "id":1,
                # "user_name": "kim",
                "account_number":"1234512345123",
                "transfer_amount" : 5000
                }
        
        headers     = {'HTTP_AUTHORIZATION' : token}
        response = client.post('/transfer/', json.dumps(data),content_type='application/json', **headers)
        self.assertEqual(response.json(), {'msg': {'user_name': ['This field is required.']}})
        self.assertEqual(response.status_code, 400)


    def test_fail_Transfer_DoesNotSameName_error_post(self):
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        data = {
                "id":1,
                "user_name": "lee",
                "account_number":"1234512345123",
                "transfer_amount" : 5000
                }
        
        headers     = {'HTTP_AUTHORIZATION' : token}
        response = client.post('/transfer/', json.dumps(data),content_type='application/json', **headers)
        self.assertEqual(response.json(), {'msg': 'The Name does not same'})
        self.assertEqual(response.status_code, 400)


    def test_fail_Transfer_NegativeAmount_error_post(self):
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        data = {
                "id":1,
                "user_name": "kim",
                "account_number":"1234512345123",
                "transfer_amount" : -5000
                }
        
        headers     = {'HTTP_AUTHORIZATION' : token}
        response = client.post('/transfer/', json.dumps(data),content_type='application/json', **headers)
        self.assertEqual(response.json(), {'msg': 'The amount can not be Negative Number'})
        self.assertEqual(response.status_code, 400)


    def test_fail_Transfer_NotFoundErrorAccount_error_post(self):
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        data = {
                "id":1,
                "user_name": "kim",
                "account_number":"123451234512",
                "transfer_amount" : 5000
                }
        
        headers     = {'HTTP_AUTHORIZATION' : token}
        response = client.post('/transfer/', json.dumps(data),content_type='application/json', **headers)
        self.assertEqual(response.json(), {'msg': 'Data Not Found. Account-Number'})
        self.assertEqual(response.status_code, 400)


class PayAPITest(TestCase):
    def setUp(self):
        User.objects.create(
            id = 1,
            name = "kim",
            email = "kim@gamil.com",
            password = "kim12345"
        )


        Account.objects.create(
            id = 1,
            user = User.objects.get(id=1),
            brokerage ="하나은행",
            number = "1234512345123",
            name = "계좌1",
            investment_principal = 100000
        )


        Transfer.objects.create(
            id = 1,
            user = User.objects.get(id=1),
            account = Account.objects.get(id=1),
            account_number = Account.objects.get(id=1).number,
            status = TransferStatus.CREATED.value,
            transfer_amount = 10000
        )


        Transfer.objects.create(
            id = 2,
            user = User.objects.get(id=1),
            account = Account.objects.get(id=1),
            account_number = Account.objects.get(id=1).number,
            status = TransferStatus.SCCUESS.value,
            transfer_amount = 10000
        )
        
        
    def tearDown(self):
        User.objects.all().delete()
        Account.objects.all().delete()
        Transfer.objects.all().delete()


    def test_success_Pay_post(self):
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        data = {
                "id" : 1,
                "signature": "4075D9A748600EECFAE8ABC7C5762E0A3D6DCAE9E5D96BD1D24C54E53FE92C43",
                "transfer_identifier": 1
                }
        
        headers     = {'HTTP_AUTHORIZATION' : token}
        response = client.post('/pay/', json.dumps(data),content_type='application/json', **headers)
        self.assertEqual(response.json(), {'status': True})
        self.assertEqual(response.status_code, 201)


    def test_fail_Pay_fail_post(self):
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        data = {
                "id":1,
                "signature": "잘못된해쉬값",
                "transfer_identifier": 1
                }
        
        headers     = {'HTTP_AUTHORIZATION' : token}
        response = client.post('/pay/', json.dumps(data),content_type='application/json', **headers)
        self.assertEqual(response.json(), {'status': False})
        self.assertEqual(response.status_code, 201)


    def test_fail_Pay_TransferIDSchema_Invalid_error_post(self):
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        data = {
                "id":1,
                # "signature": "4075D9A748600EECFAE8ABC7C5762E0A3D6DCAE9E5D96BD1D24C54E53FE92C43",
                "transfer_identifier": 1
                }
        
        headers     = {'HTTP_AUTHORIZATION' : token}
        response = client.post('/pay/', json.dumps(data),content_type='application/json', **headers)
        self.assertEqual(response.json(), {'msg': {'signature': ['This field is required.']}})
        self.assertEqual(response.status_code, 400)


    def test_fail_Pay_NotFoundError_Transfer_error_post(self):
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        data = {
                "id":1,
                "signature": "4075D9A748600EECFAE8ABC7C5762E0A3D6DCAE9E5D96BD1D24C54E53FE92C43",
                "transfer_identifier": 100
                }
        
        headers     = {'HTTP_AUTHORIZATION' : token}
        response = client.post('/pay/', json.dumps(data),content_type='application/json', **headers)
        self.assertEqual(response.json(), {'msg': 'Data Not Found. Transfer-Number'})
        self.assertEqual(response.status_code, 400)


    def test_fail_Pay_AlreadyPayed_error_post(self):
        client      = Client()
        token       = jwt.encode({'id': User.objects.get(id=1).id, 'exp' : settings.JWT_EXPIRE_TIME + datetime.now().timestamp()}, settings.JWT_KEY, algorithm="HS256")
        data = {
                "id":1,
                "signature": "4075D9A748600EECFAE8ABC7C5762E0A3D6DCAE9E5D96BD1D24C54E53FE92C43",
                "transfer_identifier": 2
                }
        
        headers     = {'HTTP_AUTHORIZATION' : token}
        response = client.post('/pay/', json.dumps(data),content_type='application/json', **headers)
        self.assertEqual(response.json(), {'msg': 'This Transfer is already Paied'})
        self.assertEqual(response.status_code, 400)