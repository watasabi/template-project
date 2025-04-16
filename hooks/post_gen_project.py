import os 
import subprocess
import shutil

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)

# Set up git repository
def init_git():
    try:

        subprocess.check_call(['git', 'init', '-b', '{{ cookiecutter.default_branch }}'], cwd=PROJECT_DIRECTORY)

        subprocess.check_call(['git', 'config', '--global', '--add', 'safe.directory', PROJECT_DIRECTORY], cwd=PROJECT_DIRECTORY)

        subprocess.check_call(['git', 'add', '.'], cwd=PROJECT_DIRECTORY)

        subprocess.check_call(['git', 'commit', '-m', 'Initial commit from cookicutter.'], 
                             cwd=PROJECT_DIRECTORY)
            
        print("Git repository initialized successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error initializing git repository: {e}")

def copy_env():
    try:
        subprocess.check_call(['mv', 'src/config/.env.example', 'src/config/.env'], cwd=PROJECT_DIRECTORY)
        print(".env file created sucessfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error initializing creating .env file: {e}")

if __name__ == '__main__':
    if '{{ cookiecutter.use_git }}' != 'no':
        init_git()
    
    #copy_env()