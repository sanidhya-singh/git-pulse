from dagster import job
from gitpulse.ops import (
    get_repositories, get_open_pull_requests,
    get_closed_pull_requests, init_base_data
)


@job(metadata={"owner": "Sanidhya Singh"})
def get_github_data():
    """
    This Job extracts data from GitHub repos and writes it to MongoDB
    """
    repos = get_repositories()
    get_open_pull_requests(repos)
    get_closed_pull_requests(repos)



@job(metadata={"owner": "Sanidhya Singh"})
def init():
    """
    This Job initialises the `GitPulse.repos` collection with the data from the CSV `gitpulse/data/base_data.csv`
    """
    init_base_data()