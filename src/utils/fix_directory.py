import yaml
import os

def update_working_directory_in_yaml():
    """
    Reads the prefect.yaml file in the root directory, searches for the directory
    in the pull configuration, and updates it with the current working directory
    if it's different. If it's already the current directory, just prints a message.
    """
    file_path = "prefect.yaml"  # Assumes the file is in the root directory

    try:
        # Load the YAML file
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)

        # Get the current working directory
        current_directory = os.getcwd()
        print(f"Current working directory: {current_directory}")

        # Search for the directory inside the 'pull' configuration
        pull_steps = data.get('pull', [])
        updated = False
        for step in pull_steps:
            if 'prefect.deployments.steps.set_working_directory' in step:
                directory = step['prefect.deployments.steps.set_working_directory'].get('directory')
                if directory == current_directory:
                    print(f"The directory in the YAML file is already set to the current directory: {current_directory}")
                    return  # Exit without making changes
                else:
                    # Update the directory with the current working directory
                    step['prefect.deployments.steps.set_working_directory']['directory'] = current_directory
                    updated = True
                    print(f"Updated directory to: {current_directory}")

        if updated:
            # Write the updated data back to the YAML file
            with open(file_path, 'w') as f:
                yaml.dump(data, f, default_flow_style=False)
            print(f"File '{file_path}' updated successfully.")
        else:
            print("No matching 'pull' configuration found in the YAML file.")

    except FileNotFoundError:
        print(f"Error: '{file_path}' not found in the current directory.")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    update_working_directory_in_yaml()
