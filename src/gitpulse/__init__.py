from dagster import Definitions
from gitpulse.jobs import mvp_job


GitPulse = Definitions(
    jobs = [mvp_job]
)