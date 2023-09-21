"""
Test Cases TestAccountModel
"""
import json
from random import randrange
from unittest import TestCase
from models import db
from models.account import Account, DataValidationError

ACCOUNT_DATA = {}

class TestAccountModel(TestCase):
    """Test Account Model"""

    @classmethod
    def setUpClass(cls):
        """ Load data needed by tests """
        db.create_all()  # make our sqlalchemy tables
        global ACCOUNT_DATA
        with open('tests/fixtures/account_data.json') as json_data:
            ACCOUNT_DATA = json.load(json_data)

    @classmethod
    def tearDownClass(cls):
        """Disconnext from database"""
        db.session.close()

    def setUp(self):
        """Truncate the tables"""
        self.rand = randrange(1, len(ACCOUNT_DATA))
        db.session.query(Account).delete()
        db.session.commit()

    def tearDown(self):
        """Remove the session"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_all_accounts(self):
        """ Test creating multiple Accounts """
        for data in ACCOUNT_DATA:
            account = Account(**data)
            account.create()
        self.assertEqual(len(Account.all()), len(ACCOUNT_DATA))
 
    def test_create_an_account(self):
        """ Test Account creation using known data """
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        account.create()
        self.assertEqual(len(Account.all()), 1)

    def test_repr(self):
        """Test the representation of an account"""
        account = Account()
        account.name = "Foo"
        self.assertEqual(str(account), "<Account 'Foo'>") 

    def test_to_dict(self):
        """ Test account to dict """
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        result = account.to_dict()
        self.assertEqual(account.name, result["name"])
        self.assertEqual(account.email, result["email"])
        self.assertEqual(account.phone_number, result["phone_number"])
        self.assertEqual(account.disabled, result["disabled"])
        self.assertEqual(account.date_joined, result["date_joined"])

    def test_from_dict(self):
        """Test account from dict """
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        result = account.to_dict()
        resultAccount = Account()
        resultAccount.from_dict(result)
        self.assertEqual(account.name, resultAccount.name)
        self.assertEqual(account.email, resultAccount.email)
        self.assertEqual(account.phone_number, resultAccount.phone_number)
        self.assertEqual(account.disabled, resultAccount.disabled)
        self.assertEqual(account.date_joined, resultAccount.date_joined)

    def test_update(self):
        """Test account update"""
        for data in ACCOUNT_DATA:
            account = Account(**data)
            account.create()
        db.session.commit()
        randnum = self.rand
        account = Account.query.get(randnum)
        oldname = account.name
        # Get the same account twice
        result = Account.query.get(randnum) 

        # Modify some fields
        result.disabled = not account.disabled
        result.name = "Test" + account.name
        newName = result.name
        result.id = randnum
        
        # Committ the changes
        result.update()
        # Reload the account
        result = Account.query.get(randnum)
        
        # Check for changes.
        self.assertEqual(result.name, newName)
        self.assertEqual(result.name, account.name)
        self.assertNotEqual(oldname, newName)
        self.assertEqual(account.disabled, result.disabled)
   
    def test_update_fail(self):
        """Test account update DataValidationError"""
        account = Account(**ACCOUNT_DATA[self.rand])
        account.name = "NewName"
        with self.assertRaises(DataValidationError):
            account.update()

    def test_delete(self):
        """Test account delete"""
        for data in ACCOUNT_DATA:
            account = Account(**data)
            account.create()
        db.session.commit()
        randnum = self.rand
        account = Account.query.get(randnum)
        account.delete()
        print(Account.query.get(randnum))
        print(account)

    def test_find(self):
        """Test find account"""
        for data in ACCOUNT_DATA:
            account = Account(**data)
            account.create()
        db.session.commit()
        randNum = self.rand
        account = Account.find(randNum)
        result = ACCOUNT_DATA[(randNum-1)]

        self.assertEqual(account.name, result["name"])
        self.assertEqual(account.email, result["email"])
        self.assertEqual(account.phone_number, result["phone_number"])
        self.assertEqual(account.disabled, result["disabled"])
