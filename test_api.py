"""HTTP contract tests for the learning API."""
import unittest
from fastapi.testclient import TestClient
from api import app

class ApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        result = self.client.post("/sessions")
        self.assertEqual(result.status_code, 201)
        self.session_id = result.json()["session_id"]

    def test_health(self):
        self.assertEqual(self.client.get("/health").json()["status"], "ok")

    def test_end_to_end_quiz(self):
        url = f"/sessions/{self.session_id}"
        response = self.client.get(url + "/next")
        self.assertEqual(response.status_code, 200)
        question = response.json()
        self.assertNotIn("correct", question)
        answer = self.client.post(url + "/answer",
            json={"question_id": question["question_id"], "choice": 0})
        self.assertEqual(answer.status_code, 200)
        self.assertIn("correct", answer.json())
        progress = self.client.get(url + "/progress")
        self.assertEqual(progress.json()["turn"], 1)

    def test_rejects_unknown_session(self):
        self.assertEqual(self.client.get("/sessions/unknown/next").status_code, 404)

    def test_rejects_wrong_question(self):
        url = f"/sessions/{self.session_id}"
        self.client.get(url + "/next")
        self.assertEqual(self.client.post(url + "/answer",
            json={"question_id":"UNKNOWN","choice":0}).status_code, 400)

if __name__=="__main__": unittest.main()
