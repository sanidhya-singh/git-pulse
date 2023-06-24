from dagster import op
import os
from github import Github
from github import Auth


@op
def get_repositories(context) -> list:
    """
    This Op returns a list of dictionaries with the repository owner and name as keys
    """
    return [
        {"repo_owner": "Stability-AI", "repo_name": "stablediffusion"},
        {"repo_owner": "Stability-AI", "repo_name": "StableLM"},
        {"repo_owner": "Stability-AI", "repo_name": "StableStudio"},
    ]


@op(out={})
def get_pull_requests(context, repos: list):
    """
    This Op returns the pull requests in a given repository
    """
    # using an access token
    auth = Auth.Token(os.environ['GITHUB_TOKEN'])

    # Public Web Github
    g = Github(auth=auth)

    # loop over the repositories
    for repo in repos:
        # Replace 'owner' and 'repo' with the repository details
        repo = g.get_repo('Stability-AI/stablediffusion')

        # Get the list of pull requests
        pulls = repo.get_pulls()

        # Iterate over the pull requests and print their titles and URLs
        for pull in pulls:
            context.log.info(f"Title: {pull.title}")
            context.log.info(f"URL: {pull.html_url}")