import os
import subprocess
import sys


def run_command(command):
    """Run a shell command and handle errors."""
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Command '{command}' failed with error: {e}")
        sys.exit(1)


def has_changes():
    """Check if there are changes in the working directory."""
    result = subprocess.run(
        "git status --porcelain", capture_output=True, text=True, shell=True
    )
    return bool(result.stdout.strip())


def remote_exists(remote_name="origin"):
    """Check if a remote with the given name already exists."""
    result = subprocess.run("git remote", capture_output=True, text=True, shell=True)
    return remote_name in result.stdout.splitlines()


def main():
    # Default project path is the current working directory
    default_path = os.getcwd()
    print(f"The default path is: {default_path}")

    # Get project path from the user
    project_path = input(
        "Enter the path to your project (Press Enter to use the current path): "
    ).strip()
    if not project_path:
        project_path = default_path

    # Get the GitHub repository URL from the user
    remote_url = input("Enter the GitHub repository URL: ").strip()
    if not remote_url:
        print("Error: No repository URL provided.")
        sys.exit(1)

    # Get the branch name from the user
    branch_name = input(
        "Enter the branch name to push (Press Enter for 'main'): "
    ).strip()
    if not branch_name:
        branch_name = "main"

    # Check if the project path exists
    if not os.path.exists(project_path):
        print("Error: The specified path does not exist.")
        sys.exit(1)

    # Change to the project directory
    os.chdir(project_path)

    # Initialize Git repository if not already initialized
    if not os.path.exists(os.path.join(project_path, ".git")):
        print("Initializing Git repository...")
        run_command("git init")

    # Ensure the branch is named correctly
    print(f"Switching to branch '{branch_name}'...")
    run_command(f"git branch -M {branch_name}")

    # Add remote origin if not already added
    if not remote_exists():
        print("Adding remote origin...")
        run_command(f"git remote add origin {remote_url}")
    else:
        print("Remote 'origin' already exists. Skipping this step.")

    # Stage all changes (including untracked files)
    print("Adding files to staging area...")
    run_command("git add .")

    # Check for changes before committing
    if has_changes():
        commit_message = input(
            "Enter commit message (Press Enter for default): "
        ).strip()
        if not commit_message:
            commit_message = "Update project"
        print("Making commit...")
        run_command(f'git commit -m "{commit_message}"')
    else:
        print("No changes to commit. Skipping commit step.")

    # Push changes to the specified branch
    print(f"Pushing changes to branch '{branch_name}'...")
    try:
        run_command(f"git push -u origin {branch_name}")
        print("Push successful!")
    except SystemExit:
        print(
            f"Push to branch '{branch_name}' failed. Please check for conflicts or other issues."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
