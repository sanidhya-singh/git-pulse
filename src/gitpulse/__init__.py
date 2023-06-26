from dagster import Definitions
from gitpulse.jobs import get_github_data, init
from gitpulse.schedules import pull_request_schedule


GitPulse = Definitions(
    jobs = [get_github_data, init],
    schedules = [pull_request_schedule]
)