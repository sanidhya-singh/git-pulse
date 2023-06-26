from dagster import ScheduleDefinition
from gitpulse.jobs import get_github_data


# this schedule will execute the job to pull GitHub pull request data at 3AM every day
pull_request_schedule = ScheduleDefinition(job=get_github_data, cron_schedule="0 3 * * *")