from locust import HttpUser, task, between, TaskSet
import time
import requests


class OrderTaskSet(TaskSet):

    @task
    def getIndex(self):
        ...
        self.client.get("/")

    @task
    def getStream(self):
        ...
        st = time.time()
        params = {
            "user_query": "x-api-tran-id에 대해 알려주세요.",
            "session_id": "foo",
        }
        with self.client.post(
            "/v1/chat/gpt/stream",
            headers={"Content-Type": "application/json"},
            json=params,
            name="/v1/chat/gpt/stream",
            stream=True,
        ) as response:
            streamed_test = ""
            for chunk in response.iter_content(chunk_size=16, decode_unicode="utf-8"):
                streamed_test += chunk

        print(time.time() - st)


class OrderTask(HttpUser):
    wait_time = between(1, 4)
    host = "http://localhost:8000"  # 테스트 대상 호스트 주소 지정

    tasks = [OrderTaskSet]
