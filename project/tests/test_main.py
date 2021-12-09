# project/server/tests/test_main.py


import unittest
import io
from base import BaseTestCase


class TestMainBlueprint(BaseTestCase):
    def test_index(self):
        # Ensure Flask is successfully setup and home page is accessible.
        response = self.client.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Specify files to compare!", response.data)

    def test_404(self):
        # Ensure route behaves correctly if accessing a route that doesn't exist.
        response = self.client.get("/404", follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"404", response.data)
    
    def test_upload(self):
        # Ensure upload endpoint is successful and redirect to results page.
        data = {}
        data['file1'] = (io.BytesIO(b"""TransactionID,TransactionAmount\n1,100"""), '1.csv')
        data['file2'] = (io.BytesIO(b"""TransactionID,TransactionAmount\n1,100"""), '2.csv')
        response = self.client.post("/upload", follow_redirects=True,
        content_type='multipart/form-data', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Unmatched Records", response.data)

if __name__ == "__main__":
    unittest.main()
