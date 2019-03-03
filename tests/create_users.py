import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import unittest
from app import base_model
from config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User, Department
import json
from app import create_app
import argparse

app = create_app()
app.app_context().push()


_verboseprint=None

class Tests(unittest.TestCase, Config):

    def setUp(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-v', '--verbosity', action="count",
                            help="increase output verbosity (e.g., -vv is more than -v)")

        args = parser.parse_args()
        if args.verbosity:
            def _verboseprint(*verb_args):
                if verb_args[0] > (3 - args.verbosity):
                    print(verb_args[1])
        else:
            _verboseprint = lambda *a: None  # do-nothing function

        global verboseprint
        verboseprint = _verboseprint


        engine = create_engine(self.SQLALCHEMY_DATABASE_URI)
        DBSession = sessionmaker(bind=engine)

        self.session = DBSession()

    def tearDown(self):
        pass

    def testGetAdmin(self):
        user = self.session.query(User).filter(User.username == 'admin').first()
        verboseprint(1, json.dumps(user.to_dict(), indent=2, default=str))
        self.assertTrue(user, "No admin user found")

    def testAddDepartment(self):
        deparment= {'designation':'Test',
        'name': 'Testing Department',
        'location': 'Virtual',
        'users':[{'id':1, 'username':'admin'}]}
        dep = Department()
        verboseprint(1, "Trying to add department:")
        verboseprint(1, json.dumps(deparment, default=str))
        dep.from_dict(**deparment)
        self.session.add(dep)

    def test_starting_out(self):
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()
