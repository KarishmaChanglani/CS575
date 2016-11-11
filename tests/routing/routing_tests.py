import unittest
from backend.routing import app


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_slash(self):
        rv = self.app.get('/static/file.test')
        assert b'test file contents' in rv.data


if __name__ == '__main__':
    unittest.main()
