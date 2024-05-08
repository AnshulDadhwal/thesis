import requests

def is_repo_forked(user, repo):
    # Constructing the API URL
    url = f"https://api.github.com/repos/{user}/{repo}"
    
    try:
        # Making the API request
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        
        # Checking if the repository is a fork
        if data.get('fork', False):
            original_repo = data['source']['full_name'] if 'source' in data else 'No source found'
            print(f"The repository {user}/{repo} is a fork.")
            print(f"Original repository: {original_repo}")
        else:
            print(f"The repository {user}/{repo} is not a fork.")
    
    except requests.RequestException as e:
        print(f"Failed to retrieve repository information: {e}")

# Example usage:
is_repo_forked('oracle', 'macaron')
