import os
import unittest

from app import DB_FILE, app, db


class AppTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)
        db.create_all()

    def tearDown(self):
    	os.remove(DB_FILE) if os.path.exists(DB_FILE) else None

    def test_get_locations(self):
    	response = self.app.get('/api/v1/locations')
    	self.assertEqual(response.status_code, 200)
    	self.assertListEqual(response.json, [])

    def test_get_departments(self):
    	response = self.app.get('/api/v1/departments')
    	self.assertEqual(response.status_code, 200)
    	self.assertListEqual(response.json, [])

    def test_get_categorys(self):
    	response = self.app.get('/api/v1/categorys')
    	self.assertEqual(response.status_code, 200)
    	self.assertListEqual(response.json, [])

    def test_get_subcategorys(self):
    	response = self.app.get('/api/v1/subcategorys')
    	self.assertEqual(response.status_code, 200)
    	self.assertListEqual(response.json, [])

    def test_get_skus(self):
    	response = self.app.get('/api/v1/skus')
    	self.assertEqual(response.status_code, 200)
    	self.assertListEqual(response.json, [])

    def test_post_skus(self):
        response = self.app.post(
            '/api/v1/skus', 
            json={
            "sku_name": "sku1", 
            "location_id": 1, 
            "department_id": 1,
            "category_id": 1,
            "sub_category_id": 1
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json,
            {'id': 1, 'sku_name': 'sku1'}
        )
