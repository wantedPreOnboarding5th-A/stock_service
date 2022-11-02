from django.apps import AppConfig


class SchedulerAppConfig(AppConfig):
    name = "scheduler"

    def ready(self):
        # print("this is Django-apps.py ready function()")
        from scheduler.scheduler import start

        start()
