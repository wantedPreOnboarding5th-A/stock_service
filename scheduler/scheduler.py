from apscheduler.schedulers.background import BackgroundScheduler
from batch.get_csv_script import get_csv_and_save
from django.conf import settings

cron_command = settings.BATCH_SCRIPT_CRON_COMMAND


def start():
    scheduler = BackgroundScheduler(
        {
            "apscheduler.jobstores.default": {
                "type": "sqlalchemy",
                "url": "sqlite:///jobs.sqlite",
            },
            "apscheduler.executors.default": {
                "class": "apscheduler.executors.pool:ThreadPoolExecutor",
                "max_workers": "1",
            },
            "apscheduler.executors.processpool": {
                "type": "processpool",
                "max_workers": "1",
            },
            "apscheduler.job_defaults.coalesce": "false",
            "apscheduler.job_defaults.max_instances": "1",
            "apscheduler.timezone": "Asia/Seoul",
        }
    )
    scheduler.add_job(
        get_csv_and_save,
        "cron",
        id="csv_save_batch",
        replace_existing=True,
        **cron_command
    )
    scheduler.start()
