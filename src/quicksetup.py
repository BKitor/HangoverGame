import os
import sys
import requests

print(sys.argv)

host_url = "192.168.1.30"
if len(sys.argv) > 1:
    host_url = sys.argv[1]

os.system("python manage.py flush --noinput")

user = requests.post(f"http://{host_url}:8000/users/create/", json={
    "email": "test@test.test",
    "username": "test",
    "first_name": "test",
    "last_name": "test",
    "password": "test",
    "date_joined": "2019-10-20T00:00",
    "last_joined": "2019-10-20T00:00",
}).json()

questions = []
for i in range(0, 3):
    res = requests.post(f"http://{host_url}:8000/api/questions", json={"prompt": f"test_question{i}"}, )
    questions.append(res.json()['uuid'])

quiz = requests.post(f"http://{host_url}:8000/api/quizzes", json={
    "name": "test_quiz",
    "author": user["id"],
    "questions": []
}).json()

quiz = requests.put(f"http://{host_url}:8000/api/quizzes", json={
    "uuid": quiz['uuid'],
    'questions': questions
}).json()

game = requests.post(f"http://{host_url}:8000/api/games", json={
    "game_name": "g",
    "quiz_uuid": quiz['uuid'],
    "host_uuid": user['id'],
}).json()
