from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
    def test_homepage(self):
        with app.test_client() as client:
            #test the status code
            resp = client.get('/home-page')
            html_data = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 405)
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn(b'<p>High Score:', html_data)
            self.assertIn(b'Secs left:', html_data)
    
    #test if the valid words are correct
    def test_valid_word(self):
        with app.test_client() as client:
            #test changes in the session with session transaction
            with client.session_transaction() as session:
                session['board'] = [["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]
        resp = client.get('/check-valid-word? word = cat')
        self.assertEqual(resp.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if word is valid, or in the dict."""
        with app.test_client() as client:
            resp = client.get('/check-valid-word?word=impossible')
            self.assertEqual(resp.json['result'], 'not-on-board')
    
    #test non-english
    def non_eng_word(self):
        """Test if word exists in the board."""
        with app.test_client() as client:
            resp = client.get('/check-valid-word?word=p;oquroq')
            self.assertEqual(resp.json['result'], 'not-word')
            
    # TODO -- write tests for every view function / feature!

