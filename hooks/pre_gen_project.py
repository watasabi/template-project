import sys
import cookiecutter.prompt
import subprocess

descriptions = {
    "default_branch":"Name of the default-branch:"
}

if "{{ cookiecutter.use_git }}" == "yes":
    MAX_ATTEMPTS = 5
    branch_name = cookiecutter.prompt.read_user_variable("default_branch","main", descriptions)
    
    for attempt in range(MAX_ATTEMPTS):
        try:  
            subprocess.check_call(['git', 'check-ref-format', '--branch', branch_name])
            break
        except subprocess.CalledProcessError as e:
            if attempt == MAX_ATTEMPTS - 1:
                print(f"Max attempts reached. Invalid branch name '{branch_name}'. Git initialization will fail. Exiting.")
            else:
                print(f"Please try again.")
                branch_name = cookiecutter.prompt.read_user_variable("default_branch", "main", descriptions) 
else:
    """{{ cookiecutter.update(
        {
            "default_branch": "",
        }
    )}}"""

sys.exit(0)