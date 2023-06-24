from dagster import Definitions
from gitpulse.jobs import get_github_data


GitPulse = Definitions(
    jobs = [get_github_data]
)