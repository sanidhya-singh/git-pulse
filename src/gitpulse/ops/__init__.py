from dagster import op
import os
from github import Github
from github import Auth
from pymongo import MongoClient
from pymongo import InsertOne
import pandas as pd


@op 
def init_base_data(context) -> bool:
    """
    This Op reads `base_data.csv` containing the repo names to be initialised
    """
    # connect to MongoDB collection
    mongo_client = MongoClient(os.environ["MONGO_CONNECTION_STRING"])
    mongo_database = mongo_client["GitPulse"]
    mongo_collection = mongo_database["repos"]

    # truncate collection and write
    mongo_collection.delete_many({})

    # read data and insert into MongoDB collection
    base_data = pd.read_csv('gitpulse/data/base_data.csv')
    for index, row in base_data.iterrows():
        mongo_collection.insert_one({
            "repo_owner": row['repo_owner'],
            "repo_name": row['repo_name']
        })

    # close MongoDB connection
    mongo_client.close()

    return True



@op
def get_repositories(context) -> list:
    """
    This Op returns a list of dictionaries with the repository owner and name as keys
    """
    # connect to MongoDB collection
    mongo_client = MongoClient(os.environ["MONGO_CONNECTION_STRING"])
    mongo_database = mongo_client["GitPulse"]
    mongo_collection = mongo_database["repos"]
    repos = list(mongo_collection.find())
    
    # close MongoDB connection
    mongo_client.close()

    return repos


@op(out={})
def get_open_pull_requests(context, repos: list):
    """
    This Op extracts open pull requests in a given repository and writes 
    their metadata to MongoDB collection `open_pull_requests`
    """
    # using an access token
    auth = Auth.Token(os.environ['GITHUB_TOKEN'])

    # Public Web Github
    g = Github(auth=auth)

    # list to store InsertOne objects for bulk write
    inserts = []

    # loop over the repositories
    for repo in repos:
        # Replace 'owner' and 'repo' with the repository details
        repo = g.get_repo(f'{repo["repo_owner"]}/{repo["repo_name"]}')

        # Get the list of pull requests
        pulls = repo.get_pulls()

        # Iterate over the pull requests and create insert payload
        for pull in pulls:
            inserts.append(
                InsertOne(
                    {
                        "additions": pull.additions,
                        "deletions": pull.deletions,
                        "state": pull.state,
                        "html_url": pull.html_url,
                        "assignee": pull.assignee.login if pull.assignee else None,
                        "assignees": [assignee.login for assignee in pull.assignees],
                        "changed_files": pull.changed_files,
                        "created_at": pull.created_at,
                        "updated_at": pull.updated_at,
                        "mergeable": pull.mergeable,
                        "number": pull.number,
                        "requested_reviewers": [reviewer.login for reviewer in pull.requested_reviewers],
                        "state": pull.state,
                        "title": pull.title,
                        "user": pull.user.login
                    }
                )
            )

    # connect to MongoDB collection
    mongo_client = MongoClient(os.environ["MONGO_CONNECTION_STRING"])
    mongo_database = mongo_client["GitPulse"]
    mongo_collection = mongo_database["open_pull_requests"]

    # truncate collection and write
    mongo_collection.delete_many({})
    mongo_collection.bulk_write(inserts)

    # close MongoDB connection
    mongo_client.close()
    

@op(out={})
def get_closed_pull_requests(context, repos: list):
    """
    This Op extracts closed pull requests in a given repository and writes 
    their metadata to MongoDB collection `closed_pull_requests`
    """
    # using an access token
    auth = Auth.Token(os.environ['GITHUB_TOKEN'])

    # Public Web Github
    g = Github(auth=auth)

    # list to store InsertOne objects for bulk write
    inserts = []

    # loop over the repositories
    for repo in repos:
        # Replace 'owner' and 'repo' with the repository details
        repo = g.get_repo(f'{repo["repo_owner"]}/{repo["repo_name"]}')

        # Get the list of pull requests
        pulls = repo.get_pulls(state='closed')

        # Iterate over the pull requests and create insert payload
        for pull in pulls:
            inserts.append(
                InsertOne(
                    {
                        "additions": pull.additions,
                        "deletions": pull.deletions,
                        "state": pull.state,
                        "html_url": pull.html_url,
                        "assignee": pull.assignee.login if pull.assignee else None,
                        "assignees": [assignee.login for assignee in pull.assignees],
                        "changed_files": pull.changed_files,
                        "created_at": pull.created_at,
                        "updated_at": pull.updated_at,
                        "mergeable": pull.mergeable,
                        "number": pull.number,
                        "requested_reviewers": [reviewer.login for reviewer in pull.requested_reviewers],
                        "state": pull.state,
                        "title": pull.title,
                        "user": pull.user.login
                    }
                )
            )

    # connect to MongoDB collection
    mongo_client = MongoClient(os.environ["MONGO_CONNECTION_STRING"])
    mongo_database = mongo_client["GitPulse"]
    mongo_collection = mongo_database["closed_pull_requests"]

    # truncate collection and write
    mongo_collection.delete_many({})
    mongo_collection.bulk_write(inserts)

    # close MongoDB connection
    mongo_client.close()