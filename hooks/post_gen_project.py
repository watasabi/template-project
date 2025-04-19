import os
import subprocess

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


# Set up git repository
def init_git():
    try:
        subprocess.check_call(
            ["git", "init", "-b", "{{ cookiecutter.default_branch }}"],
            cwd=PROJECT_DIRECTORY,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        subprocess.check_call(
            ["git", "config", "--global", "--add", "safe.directory", PROJECT_DIRECTORY],
            cwd=PROJECT_DIRECTORY,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        subprocess.check_call(
            ["git", "add", "."],
            cwd=PROJECT_DIRECTORY,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        subprocess.check_call(
            ["git", "commit", "-m", "Initial commit from cookicutter."],
            cwd=PROJECT_DIRECTORY,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        print("Git repository initialized successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error initializing git repository: {e}")


def copy_env():
    try:
        subprocess.check_call(
            ["mv", "src/config/.env.example", "src/config/.env"],
            cwd=PROJECT_DIRECTORY,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(".env file created sucessfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error creating .env file: {e}")


def create_gitingore():
    try:
        subprocess.check_call(
            "echo '#Exclude everything except the gitignore\n*\n!.gitignore' > data/.gitignore",
            cwd=PROJECT_DIRECTORY,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error creating .gitignore file in data folder: {e}")


if __name__ == "__main__":
    create_gitingore()
    if "{{ cookiecutter.use_git }}" == "Yes":
        init_git()

    # copy_env()
