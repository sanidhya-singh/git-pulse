from dagster import job
from gitpulse.ops import (
    get_repositories, get_open_pull_requests,
    get_closed_pull_requests
)


@job(metadata={"owner": "Sanidhya Singh"})
def get_github_data():
    """
    This Job extracts data from GitHub repos and writes it to MongoDB
    """
    repos = get_repositories()
    get_open_pull_requests(repos)
    get_closed_pull_requests(repos)