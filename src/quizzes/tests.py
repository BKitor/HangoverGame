from rest_framework.renderers import JSONRenderer

from quizzes.models import Quiz, Question
from quizzes.views import QuizListCreate, QuestionListCreate
from quizzes.serializers import QuizSerializer
from account.models import User
from django.test import TestCase, Client

# Create your tests here.


class QuizTestCase(TestCase):

    def create_quiz(self, quiz_name):
        new_quiz_map = self.test_quiz_map
        new_quiz_map['name'] = quiz_name
        new_quiz = Quiz.objects.get_or_create(**new_quiz_map)
        return (new_quiz, new_quiz_map)

    def setUp(self):
        new_quiz_data = {
            "author": self.author
        }

        new_quiz_data["name"] = "test_quiz_1"
        Quiz.objects.get_or_create(**new_quiz_data)
        new_quiz_data["name"] = "test_quiz_2"
        Quiz.objects.get_or_create(**new_quiz_data)
        new_quiz_data["name"] = "test_quiz_3"
        Quiz.objects.get_or_create(**new_quiz_data)

    @property
    def test_quiz_map(self):
        return {
            "author": str(self.author.id),
            "name": "test_quiz"}

    @property
    def author(self):
        author, _ = User.objects.get_or_create(
            email="quiz@test.test", username="TestQuizUser", first_name="Quiz", last_name="Test")
        return author

    def test_quiz_post(self):
        c = Client()
        req_body = self.test_quiz_map
        req_url = "/api/quizzes"

        res = c.post(req_url, req_body, content_type="application/json")
        res_json = res.json()
        test_obj = Quiz.objects.get(**req_body)

        self.assertEqual(req_body["author"], str(test_obj.author.id))
        self.assertEqual(req_body["name"], test_obj.name)
        self.assertEqual(res_json["author"], str(test_obj.author.id))
        self.assertEqual(res_json["name"], test_obj.name)

    def test_quiz_get(self):
        c = Client()
        req_url = "/api/quizzes"

        res = c.get(req_url)
        res_json = res.json()

        # can't check uuid, so delete it to pass the test
        # probaby a better way to do this, figure it out later
        for quiz in res_json:
            del quiz["uuid"]

        for i in range(1, 4):
            assert_obj = {
                "author": str(self.author.id),
                "name": f"test_quiz_{i}",
                "questions": []
            }
            self.assertIn(assert_obj, res_json,
                          f"\n\n{assert_obj} not in {res_json}")

    def test_quiz_put(self):
        c = Client()
        req_url = "/api/quizzes"
        quiz_map = self.test_quiz_map

        new_quiz, _ = Quiz.objects.get_or_create(
            name="put_test_quiz", author=self.author)
        new_question, _ = Question.objects.get_or_create(
            prompt="test question")

        quiz_map["uuid"] = str(new_quiz.uuid)
        quiz_map["questions"] = [str(new_question.uuid)]

        c.put(req_url, quiz_map, content_type="application/json")

        self.assertEqual(new_quiz.questions.first(
        ).uuid, new_question.uuid, "put request didn't add question to quiz")

    def test_quiz_delete(self):
        c = Client()
        req_url = "/api/quizzes"

        new_quiz, _ = Quiz.objects.get_or_create(
            name="delete_test_quiz", author=self.author)
        c.delete(req_url, {"uuid": str(new_quiz.uuid)},
                 content_type="application/json")

        try:
            Quiz.objects.get(uuid=new_quiz.uuid)
            self.assertEqual(1, 0, "Quiz instance was not deleted")
        except Quiz.DoesNotExist:
            self.assertEqual(1, 1)


class QuestionTestCase(TestCase):

    def test_question_post(self):
        c = Client()
        req_url = "/api/questions"
        req_body = {
            "prompt": "This is a test"
        }

        res = c.post(req_url, req_body, content_type="application/json")
        res_dict = res.json()

        db_obj = Question.objects.get(uuid=res_dict["uuid"])

        for key in res_dict:
            if not key == "uuid":
                self.assertEqual(res_dict[key], req_body[key])
        self.assertEqual(db_obj.prompt, req_body["prompt"])

    def test_question_delete(self):
        c = Client()
        req_url = "/api/questions"
        to_be_deleted_prompt = "This shouldn't exist"

        to_be_deleted, _ = Question.objects.get_or_create(
            prompt=to_be_deleted_prompt)

        req_body = {
            "uuid": str(to_be_deleted.uuid)
        }

        c.delete(req_url, req_body, content_type="application/json")

        q_queryset = Question.objects.filter(prompt=to_be_deleted_prompt)
        for q in q_queryset:
            self.assertNotEqual(to_be_deleted.uuid, q.uuid)
