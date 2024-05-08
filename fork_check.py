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
        
        # Extracting owner information
        owner_info = data.get('owner', {})
        print("Owner Information:")
        print(f"Login: {owner_info.get('login', 'Not available')}")
        print(f"ID: {owner_info.get('id', 'Not available')}")
        print(f"Type: {owner_info.get('type', 'Not available')}")
        print(f"URL: {owner_info.get('html_url', 'Not available')}")

        # Check if the repository is archived
        is_archived = data.get('archived', False)
        print(f"Archived: {'Yes' if is_archived else 'No'}")

        # Assuming a 'deprecated' tag in topics for deprecation status (as an example)
        topics = data.get('topics', [])
        is_deprecated = 'deprecated' in topics
        print(f"Deprecated: {'Yes' if is_deprecated else 'No'}")

    except requests.RequestException as e:
        print(f"Failed to retrieve repository information: {e}")

# Taking user input for the repository owner and the repository name
user_input = input("Enter the GitHub username of the repository owner: ")
repo_input = input("Enter the repository name: ")

# Example usage:
is_repo_forked(user_input, repo_input)
