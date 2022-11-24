import locust

from utils import get_random_string


# class CpuUser(locust.HttpUser):
#     @locust.task
#     def basic(self):
#         self.client.get("/posts/cpu/")


# class PostCreateUser(locust.HttpUser):
#     @locust.task
#     def basic(self):
#         self.client.post(
#             "/posts/io_create/",
#             data={
#                 "title": f"Post {get_random_string(10)}",
#                 "content": f"Content {get_random_string(100)}",
#             },
#         )


class PostReadUser(locust.HttpUser):
    @locust.task
    def basic(self):
        self.client.get("/posts/io_read/")
