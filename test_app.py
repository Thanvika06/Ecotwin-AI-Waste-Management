"""
Automated unit & integration test suite for EcoTwin.
Tests all endpoints using Flask's test client.
"""
import unittest
import json
from app import app

class TestEcoTwin(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_01_index_page(self):
        # Test landing page
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'EcoTwin', response.data)
        self.assertIn(b'PROBLEM STATEMENT', response.data)
        
        # Test dashboard page
        res_dash = self.client.get('/dashboard')
        self.assertEqual(res_dash.status_code, 200)
        self.assertIn(b'Digital Twin', res_dash.data)
        self.assertIn(b'Computer Vision', res_dash.data)

    def test_02_twin_state(self):
        response = self.client.get('/api/twin/state')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(len(data['state']['bins']), 24)
        self.assertEqual(len(data['state']['trucks']), 4)
        self.assertEqual(len(data['state']['facilities']), 4)
        self.assertIn('kpis', data['state'])

    def test_03_cv_gallery(self):
        response = self.client.get('/api/cv/gallery')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertGreaterEqual(len(data['samples']), 8)
        self.assertEqual(data['samples'][0]['category'], 'Plastics')

    def test_04_cv_classification(self):
        payload = {
            "image": "sample:sample_pet_bottle",
            "features": {
                "avg_r": 40,
                "avg_g": 120,
                "avg_b": 220,
                "brightness": 130,
                "aspect_ratio": 1.4
            }
        }
        response = self.client.post('/api/cv/classify', 
                                    data=json.dumps(payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        res = data['result']
        self.assertIn('category', res)
        self.assertIn('confidence', res)
        self.assertIn('recyclability_score', res)
        self.assertIn('bounding_box', res)
        self.assertIn('prep_instructions', res)

    def test_05_conveyor_stream(self):
        response = self.client.get('/api/cv/conveyor/step')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertIn('item', data)
        self.assertIn('target_bunker', data['item'])

    def test_06_twin_simulation_step(self):
        response = self.client.post('/api/twin/step',
                                    data=json.dumps({"delta_seconds": 30}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertGreaterEqual(data['state']['sim_tick'], 1)

    def test_07_truck_dispatch(self):
        response = self.client.post('/api/twin/dispatch',
                                    data=json.dumps({"truck_id": "TRUCK-01"}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])

    def test_08_ai_recommendations(self):
        response = self.client.get('/api/ai/recommendations')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(len(data['recommendations']), 4)
        rec_categories = [r['category'] for r in data['recommendations']]
        self.assertIn('Segregation & Contamination', rec_categories)
        self.assertIn('Dynamic Route Optimization', rec_categories)

    def test_09_copilot_chat(self):
        payload = {"message": "Which sector has the highest contamination?", "history": []}
        response = self.client.post('/api/ai/chat',
                                    data=json.dumps(payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertIn('reply', data)

    def test_10_analytics_report(self):
        response = self.client.get('/api/analytics')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertIn('stream_distribution', data['analytics'])
        self.assertIn('top_overflow_risks', data['analytics'])

if __name__ == '__main__':
    unittest.main()
