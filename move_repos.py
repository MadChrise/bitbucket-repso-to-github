import requests
import subprocess
import sys

# Bitbucket-Data
BITBUCKET_WORKSPACE = "YOUR_BITBUCKET_WORKSPACE_HERE"
BITBUCKET_USERNAME = "YOUR_BITBUCKET_USERNAME_HERE"
BITBUCKET_APP_PASSWORD = "YOUR_APP_PASSWORD_HERE"

# Github-Data
GITHUB_WORKSPACE = "YOUR_GITHUB_WORKSPACE_HERE"
GITHUB_TOKEN = "YOUR_GITHUB_PAT_TOKEN_HERE"
CREATE_AS_PRIVATE_REPO = True

# API-Urls
BITBUCKET_API_URL = "https://api.bitbucket.org/2.0/repositories/"
GITHUB_API_URL = f"https://api.github.com/orgs/{GITHUB_WORKSPACE}/repos"
# Log-File
LOG_FILE = ".\\info.txt"

# Writes the error-message in txt-file
def log(message):
    with open(LOG_FILE, "a") as log:
        log.write(message + "\n")

# Read repositories from Bitbucket
def get_repositories():
    repos = []
    repo_details = {}
    # Bitbucket URL for reading repos
    url = BITBUCKET_API_URL + BITBUCKET_WORKSPACE
    while url:
        response = requests.get(url, auth=(BITBUCKET_USERNAME, BITBUCKET_APP_PASSWORD))
        if response.status_code == 200:
            data = response.json()
            for repo in data['values']:
                full_name = repo['full_name']
                repos.append(full_name)
                # Save the clone URL for HTTPS (usually the first clone link)
                clone_links = repo.get('links', {}).get('clone', [])
                https_url = None
                for link in clone_links:
                    if link.get('name') == 'https':
                        https_url = link.get('href')
                        break
                repo_details[full_name] = https_url
            url = data.get('next')  # Bitbucket paginates results
        else:
            print(f"Error: {response.status_code}, {response.text}")
            log(f"Error: {response.status_code}, {response.text}")
            return None, None
    return repos, repo_details

# Clones the repository as bare repo from bitbucket
def clone_bare_repo(clone_url):
    try:
        subprocess.check_call(["git", "clone", "--bare", clone_url])
        print("Bare clone completed successfully.")
    except subprocess.CalledProcessError as e:
        print("Error during bare clone:", e)
        sys.exit(1)

# Creates a new Github repository
def create_github_repo(repo_name):
    # Name of the repo + wether it is private or public
    payload = {"name": repo_name, "private": CREATE_AS_PRIVATE_REPO}
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}

    # API request to create the rpo
    response = requests.post(GITHUB_API_URL, json=payload, headers=headers)

    if response.status_code == 201:
        print(f"GitHub repository '{repo_name}' created successfully.")
        return f"https://{GITHUB_TOKEN}@github.com/{GITHUB_WORKSPACE}/{repo_name}.git"
    else:
        print(f"Error creating GitHub repository: {response.text}")
        log(f"Error creating GitHub repository: {response.text}")
        sys.exit(1)

# Pushes a previously cloned repository to Github
def push_to_github(repo_name, github_url):
    try:
        # Push to github (with mirror-option so that all Branches etc. are pushed as well)
        subprocess.check_call(["git", "-C", f"{repo_name}.git", "push", "--mirror", github_url])
        print("Repository pushed to GitHub successfully.")
    except subprocess.CalledProcessError as e:
        print("Error pushing to GitHub:", e)
        log("Error pushing to GitHub:", e)
        sys.exit(1)

if __name__ == "__main__":
    # Read all repositories from Bitbucket
    repos, repo_details = get_repositories()
    if repos is None or not repos:
        print("No repositories found or authentication failed.")
        sys.exit(1)

    # Iterate over all repositories
    for idx, repo in enumerate(repos, start=1):
        # Url of the repository that should be cloned
        url_to_clone =repo_details.get(repo)
        # Name of the repository
        repo_name = repo.split('/')[-1]
        # Clone the repository
        clone_bare_repo(url_to_clone)

        # Create a new GitHub repository
        print(f"Creating GitHub repository: {repo_name}...")
        github_url = create_github_repo(repo_name)

        # Push the cloned repository to github
        print(f"Pushing {repo_name} to GitHub...")
        push_to_github(repo_name, github_url)