import requests

def get_package_info(system, package_name):
    # URL encode the package name to handle special characters including slash
    encoded_package_name = requests.utils.quote(package_name, safe='')

    # Construct the URL for the API request
    url = f"https://api.deps.dev/v3/systems/{system}/packages/{encoded_package_name}"

    try:
        # Make the API call
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON data returned by the API
        package_data = response.json()
        
        # Display the key 'packageKey'
        if 'packageKey' in package_data:
            print(f"Package details for {package_name}:")
            print("Package System:", package_data['packageKey']['system'])
            print("Package Name:", package_data['packageKey']['name'])
            
            # Display version details
            if 'versions' in package_data:
                print("Versions:")
                for version in package_data['versions']:
                    print(f"  Version: {version['versionKey']['version']}, Published At: {version['publishedAt']}, Is Default: {version['isDefault']}")
            else:
                print("No version information available.")
        else:
            print("Package information not found.")

    except requests.RequestException as e:
        print(f"An error occurred while fetching package information: {e}")

# Example usage of the function
get_package_info('npm', '@colors/colors')
