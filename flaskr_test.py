import unittest

import os
import tempfile

import flaskr


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()
        flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        self.assertIn(b'No entries here so far', rv.data)

    def test_login_logout(self):
        rv = self.login('admin', 'p@ssw0rd')
        self.assertIn(b'You were logged in', rv.data)
        rv = self.logout()
        self.assertIn(b'You were logged out', rv.data)
        rv = self.login('adminx', 'p@ssw0rd')
        self.assertIn(b'Invalid username', rv.data)
        rv = self.login('admin', 'p@ssw0rdx')
        self.assertIn(b'Invalid password', rv.data)

    def test_messages(self):
        self.login('admin', 'p@ssw0rd')
        rv = self.app.post('/add', data={
            'title': '<Hello>',
            'text': '<strong>HTML</strong> allowed here',
        }, follow_redirects=True)
        self.assertNotIn(b'No entries here so far', rv.data)
        self.assertIn(b'&lt;Hello&gt;', rv.data)
        self.assertIn(b'<strong>HTML</strong> allowed here', rv.data)

    def login(self, username, password):
        return self.app.post('/login', data={
            'username': username,
            'password': password,
        }, follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

if __name__ == '__main__':
    unittest.main()
