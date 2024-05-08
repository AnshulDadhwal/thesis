import requests

def get_package_info(system, package_name):
    # URL encode the package name to handle special characters including slash
    encoded_package_name = requests.utils.quote(package_name, safe='')

    # Construct the URL for the API request to get package details
    package_url = f"https://api.deps.dev/v3/systems/{system}/packages/{encoded_package_name}"

    try:
        # Make the API call for package details
        package_response = requests.get(package_url)
        package_response.raise_for_status()  # Raise an exception for HTTP errors
        package_data = package_response.json()
        
        if 'packageKey' in package_data:
            print(f"Package details for {package_name}:")
            print("Package System:", package_data['packageKey']['system'])
            print("Package Name:", package_data['packageKey']['name'])
            
            # Iterate through each version to get dependencies
            if 'versions' in package_data:
                print("Versions and Direct Dependencies:")
                for version in package_data['versions']:
                    version_number = version['versionKey']['version']
                    print(f"  Version: {version_number}, Published At: {version['publishedAt']}, Is Default: {version['isDefault']}")

                    # Construct the URL for the API request to get dependencies
                    dependencies_url = f"https://api.deps.dev/v3/systems/{system}/packages/{encoded_package_name}/versions/{version_number}:dependencies"
                    dependencies_response = requests.get(dependencies_url)
                    dependencies_response.raise_for_status()
                    dependencies_data = dependencies_response.json()

                    # Display the dependencies with relation DIRECT
                    if 'nodes' in dependencies_data:
                        print("    Direct Dependencies:")
                        direct_deps = [node for node in dependencies_data['nodes'] if node['relation'] == 'DIRECT']
                        if direct_deps:
                            for node in direct_deps:
                                name = node['versionKey']['name']
                                version = node['versionKey']['version']
                                print(f"      Name: {name}, Version: {version}")
                        else:
                            print("      No direct dependencies found.")
                    else:
                        print("    No dependencies found.")

            else:
                print("No version information available.")
        else:
            print("Package information not found.")

    except requests.RequestException as e:
        print(f"An error occurred while fetching package information: {e}")

# Collect user input for system and package name
user_system = input("Enter the package system (e.g., npm, pypi): ")
user_package_name = input("Enter the package name (e.g., lodash, @tensorflow/tfjs): ")

# Call the function with user input
get_package_info(user_system, user_package_name)
