from dagster import Definitions
from gitpulse.jobs import get_github_data
from gitpulse.schedules import pull_request_schedule


GitPulse = Definitions(
    jobs = [get_github_data],
    schedules = [pull_request_schedule]
)