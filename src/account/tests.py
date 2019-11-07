from django.test import TestCase, Client
from account.models import User
# Create your tests here.


class UserTestCase(TestCase):

    def assert_user_and_dict(self, user_dict, user_obj):
        self.assertEqual(user_obj.email, user_dict['email'])
        self.assertEqual(user_obj.username, user_dict['username'])
        self.assertEqual(user_obj.first_name, user_dict['first_name'])
        self.assertEqual(user_obj.last_name, user_dict['last_name'])
        self.assertEqual(user_obj.password, user_dict['password'])

    @property
    def sample_user_dict(self):
        return {
            "email": "test@test.test",
            "username": "test",
            "first_name": "test",
            "date_joined": "2019-10-20T00:00",
            "last_joined": "2019-10-20T00:00",
            "last_name": "test",
            "password": "test",
        }

    @property
    def sample_user(self):
        new_user, _ = User.objects.get_or_create(username="test")
        return new_user

    def test_user_create(self):
        c = Client()
        req_url = "/users/create/"
        req_body = self.sample_user_dict

        res = c.post(req_url, req_body, content_type="application/json")
        res_json = res.json()

        new_user = User.objects.get(id=res_json['id'])
        self.assert_user_and_dict(user_dict=req_body, user_obj=new_user)

    def test_user_get(self):
        c = Client()
        test_user = self.sample_user
        req_url = f'/users/{test_user.id}'

        res = c.get(req_url)
        res_json = res.json()

        self.assert_user_and_dict(user_dict=res_json, user_obj=test_user)

    def test_user_put(self):
        c = Client()
        old_user = self.sample_user
        req_url = f"/users/{old_user.id}/update/"

        update_dict = self.sample_user_dict
        update_dict['username'] = 'updated_username'

        c.put(req_url, update_dict, content_type="application/json")

        new_user = User.objects.get(id=old_user.id)

        self.assertNotEqual(old_user.username, new_user.username)

    def test_user_delete(self):
        c = Client()
        test_user = self.sample_user
        req_url = f"/users/{test_user.id}/delete/"

        c.delete(req_url)

        try:
            new_usr = User.objects.get(id=test_user.id)
            print(new_usr)
            self.assertNotEqual(0, 0, "user didn't delete")
        except User.DoesNotExist:
            self.assertEqual(0, 0)

    def test_get_user_quizzes(self):
        c = Client()
        test_user = self.sample_user
        test_url = f"/users/{test_user.id}/quizzes/"

        quiz = {
                "name": "test_quiz",
                "author": test_user.id,
                "questions": []
            }

        res = c.post("/api/quizzes", quiz, content_type="application/json")
        self.assertEquals(res.status_code, 201)

        quizzes = c.get(test_url).json()

        self.assertEqual(len(quizzes), 1)
        self.assertEqual(res.json(), quizzes[0])
