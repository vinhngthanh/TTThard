import datetime
import unittest
from flask import current_app
from app import create_app, db
import os
import sys
from app.models import Player, Match
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class TestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_app_exists(self):
        self.assertFalse(current_app is None)
        
    def test_app_is_testing(self):
        self.assertTrue(current_app.config["TESTING"])
        
    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome", response.data)

    def test_players(self):
        response = self.client.get("/players")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"All Players", response.data)

    def test_ttt_not_login(self):
        response = self.client.get("/tic-tac-toe", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)

    def test_profile_not_login(self):
        response = self.client.get("/player/1", follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_new_player(self):
        # Test New Player
        response = self.client.post("/player/new", data={
            "username" : "test_user1",
            "email" : "test_user1@gmail.com",
            "password" : "testpassword"
        })

        self.assertEqual(response.status_code, 302)
        player = Player.query.filter_by(username='test_user1').first()
        self.assertTrue(player)


        # Test Profile
        response = self.client.get(f"/player/1", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Delete", response.data)

        # Test TTT Login
        response = self.client.get(f"/tic-tac-toe", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Bot", response.data)

        # Test Logout
        response = self.client.get(f"/logout", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"All Players", response.data)

        # Test Login
        response = self.client.post("/login", data={
            "email" : "test_user1@gmail.com",
            "password" : "testpassword"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"test_user1", response.data)

        # Test add match
        data = {
            'status': 'win',
            'moves': 20,
            'start_time': 'Sat Apr 22 2023 12:40:59 GMT-0400 (Eastern Daylight Time)',
            'duration': 60
        }
        response = self.client.post('/update_match', data=data)
        self.assertEqual(response.status_code, 200)

        # Test Delete Account Wrong info
        response = self.client.post(f"/delete_player/{player.id}", data={
            "email" : "test_user2@gmail.com",
            "password" : "testpassword"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Password:", response.data)
        self.assertTrue(Player.query.filter_by(username='test_user1').first())

        # Test Delete Account
        response = self.client.post(f"/delete_player/{player.id}", data={
            "email" : "test_user1@gmail.com",
            "password" : "testpassword"
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Player.query.filter_by(username='test_user1').first())

