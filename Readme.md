# Bitbucket to Github Migration

Our Git-Repositories were located at Bitbucket. For a few reasons we wanted to migrate to Github. As there is no simple "Take all the repositories there and copy it to Github" i wrote a simple script that downloads all Repos from Bitbucket and pushes it to Github.

All branches and tags are migrated.

**Caution**: This script was suitable for us but maybe needs to be adjusted for your specific needs. But overall i think it is a good starting point.

# Prerequisites

- The script doesn't check if a repository with the name exists in the Workspace. If a repository with the same name already exists in GitHub, the script will fail unless manually deleted beforehand.
- The script only migrates the repositories. No issues, pull requests, wiki pages, or other metadata are transferred.
- You need to have git installed and git should know your Origins

You need a Bitbucket app password and a Github "PAT" (Personal Access Token).

You need to have Python3 installed.

## Bitbucket App Password

At the time of writing this, you can create your Bitbucket app password the following way:

- Open Bitbucket in your browser
- Go to "Settings -> Personal Bitbucket settings"
- Go to "App passwords"
- Click on "Create app password"
- Choose Permissions (Repositories Read should be sufficient)

## Github PAT Token

- Click on your profile picture on the right top of the screen
- Go to "Settings
- Go to "Developer Settings" (last item)
- Go to "Personal access tokens -> Tokens (classic)"
- Click on "Generate new token"
- Check "repo" and click on "Generate token"

# Running the script

Install the `requests`-Library for Python (`pip install requests`).

Download the script and configure your settings:

- BITBUCKET_WORKSPACE: The name of your Bitbucket Workspace where the repos are located
- BITBUCKET_USERNAME: Username of your Bitbucket-Account. **Caution**: This is not the E-Mail Address you log in with, instead it is the "real" username. You can find it in your Personal settings.
- BITBUCKET_APP_PASSWORD: The previously generated app password
- GITHUB_WORKSPACE: Your Github-Workspace where the repos should be pushed to
- GITHUB_TOKEN: Your previously generated PAT-Token
- CREATE_AS_PRIVATE_REPO: Defines if the repository that is created in Github is private or public

Now simply run the script:

```python
python3 move_repos.py
```