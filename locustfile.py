from locust import HttpUser, task

SERVER_IP_ADDR = "95.163.235.40"
#nanSERVER_IP_ADDR = "trainingportal.space"



class LoadTestingTraining_Portal(HttpUser):
    @task
    def test_some_pages_open(self):
        # Mainapp
        self.client.get(f"http://{SERVER_IP_ADDR}/mainapp/")
        self.client.get(f"http://{SERVER_IP_ADDR}/mainapp/catalog/")
        self.client.get(f"http://{SERVER_IP_ADDR}/mainapp/founders/")
        self.client.get(f"http://{SERVER_IP_ADDR}/mainapp/contacts/")
        self.client.get(f"http://{SERVER_IP_ADDR}/mainapp/news_list/")
        self.client.get(f"http://{SERVER_IP_ADDR}/mainapp/course_create/")
        self.client.get(f"http://{SERVER_IP_ADDR}/mainapp/course_update/1/")
        self.client.get(f"http://{SERVER_IP_ADDR}/mainapp/lesson/1/")
        self.client.get(f"http://{SERVER_IP_ADDR}/mainapp/categories/")
        self.client.get(f"http://{SERVER_IP_ADDR}/mainapp/ckeditor/")
        self.client.get(f"http://{SERVER_IP_ADDR}/mainapp/cabinet/")
        self.client.get(f"http://{SERVER_IP_ADDR}/mainapp/courses_category/1/")
        # Authapp
        self.client.get(f"http://{SERVER_IP_ADDR}/authapp/register/")
        self.client.get(f"http://{SERVER_IP_ADDR}/authapp/login/")
        self.client.get(f"http://{SERVER_IP_ADDR}/mainapp/logout/")
