from dagster import job
from gitpulse.ops import (
    get_repositories, get_pull_requests
)


@job(metadata={"owner": "Sanidhya Singh"})
def get_github_data():
    """
    This Job extracts data from GitHub repos
    """
    get_pull_requests(
        get_repositories()
    )