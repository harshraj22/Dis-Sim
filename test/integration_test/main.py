import requests
import time
import logging
import unittest

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TestImageSimilarityWorkflow(unittest.TestCase):

    def setUp(self):
        # Authenticate and store the auth token for later use
        r = requests.post('http://auth:8019/login', json={'username': 'test', 'password': 'test'})
        self.assertEqual(r.status_code, 200)
        self.token = r.json()['token']

    def test_image_similarity_workflow(self):
        token = self.token

        # Submit images
        headers = {"accept": "application/json", 'Authorization': f'Bearer {token}'}
        with open('image.jpg', 'rb') as f:
            img = f.read()
        files = {"img1": img, "img2": img}
        r = requests.post('http://api:8001/submit', headers=headers, files=files)
        self.assertEqual(r.status_code, 200)
        task_id = r.json()
        logging.info(f'Task id: {task_id}')

        # Wait for task to complete
        time.sleep(3)

        # Check task status
        r = requests.get(f'http://api:8001/status/{task_id}')
  
        logging.info(f'{r.status_code} {r.json()}')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), 'SUCCESS')

        # Get task result
        r = requests.get(f'http://api:8001/result/{task_id}')
        logging.info(f'{r.status_code} {r.json()}')
        self.assertEqual(r.status_code, 200)

if __name__ == '__main__':
    unittest.main()
