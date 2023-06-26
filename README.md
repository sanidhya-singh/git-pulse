# Git Pulse
Using a containerised solution, this project can help you pull GitHub metadata for your organisation.
Git Pulse can unlock better insights for your organisation by identifying pain points and unlocking better visibility into blockages.

Using Git Pulse, you can view metrics such as 
- mean time to merge
- average additions/deletions per PR
- average time to approve per reviewer
and lots more


## Running with Docker 
To run the environment on your machine the repo is setup to use Docker. Simply clone the repo to your machine and execute the command below 

```
docker-compose up -d --build
```

This will spin up containers that you will need to start working with this repository. If successful, it should look something like this on your Docker Desktop dashboard

![Screenshot 2023-05-01 at 22 51 20](https://user-images.githubusercontent.com/10533379/235496568-f949770b-b786-4065-aa31-6f0b482d26be.png)

The deployment makes use of different containers running
- Dagit UI
- Dagster Daemon
- Dagster gRPC
- PostgreSQL backend
- MongoDB

Please navigate to [http://localhost:3000/](http://localhost:3000/) on your favorite browser to see the Dagit UI. The above `docker compose` command also mounted the local GitHub repo to the Docker container, you are now free to make code changes and contribute to the repo. :) 


### Repository Names to Track
Edit the CSV in `src/gitpulse/data` to incldue the repositories you wish to track with GitPulse. Please ensure your GitHub token has the required privileges to be able to access the repos you wish to track.