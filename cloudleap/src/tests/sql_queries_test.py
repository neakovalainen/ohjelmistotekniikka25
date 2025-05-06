import unittest
from database.userdata import UserData
from database.sql_connect import get_database_connection
from database.sql_queries import initialize_database

class TestSql(unittest.TestCase):
    def setUp(self):
        initialize_database()
        self.data = UserData(get_database_connection())

    def test_user_insertion_works(self):
        self.data.save_username("mimi")
        self.assertEqual(self.data.get_username("mimi"), "mimi")

    def test_score_insertion_works(self):
        self.data.update_score(5, "mimi")
        self.assertEqual(self.data.get_score("mimi"), 5)

    def test_user_deletion_works(self):
        self.data.save_username("mimi")
        self.data.delete_user("mimi")
        self.assertEqual(self.data.get_username("mimi"), False)

    def test_return_minus_2_if_no_score_exists(self):
        self.assertEqual(self.data.get_score("mumu"), -2)

    def test_score_deletion_works(self):
        self.data.update_score(5, "mimi")
        self.data.delete_score("mimi")
        self.assertEqual(self.data.get_score("mimi"), -2)
    
    def test_get_all_users_works(self):
        self.data.save_username("mimi")
        self.data.save_username("mumu")
        self.assertEqual(self.data.get_all_users(), ["mimi", "mumu"])