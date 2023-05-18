import unittest
from authentication import AUTH_APP, login, logout

class TestAuthentication(unittest.TestCase):
    def setUp(self):
        self.app = AUTH_APP.test_client()
        
    def test_login_valid_creds(self): 
     response = self.app.post('/login', data=dict(
        email=os.environ.get('VALID_EMAIL'),
        password=os.environ.get('VALID_PASSWORD')
    ))
     self.assertEqual(response.status_code, 302)

    def test_login_renders_error_with_invalid_email_and_password(self):
        response = self.app.post('/login', data=dict(
            email='invalid@email.com',
            password='invalid'
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid UserId / Password', response.data)
        
    def test_logout_removes_email_from_session(self):
        with self.app.session_transaction() as sess:
            sess['email'] = 'test@example.com'
            
        response = self.app.get('/logout')
        self.assertEqual(response.status_code, 302)
        
        with self.app.session_transaction() as sess:
            self.assertNotIn('email', sess)  
            
    def test_empty_email_and_password(self):
        response = self.app.post('/login', data=dict(
            email='',
            password=''
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email and password cannot be empty', response.data)
    
    def test_login_with_invalid_email(self):
     response = self.app.post('/login', data=dict(
        email='invalid_email',
        password='valid'
    ))
     self.assertEqual(response.status_code, 200)
     self.assertIn(b'Invalid email', response.data)

            
if __name__ == '__main__':
    unittest.main()
