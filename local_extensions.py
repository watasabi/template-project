import subprocess
from cookiecutter.prompt import read_user_choice, read_user_variable, read_user_yes_no
from jinja2.ext import Extension


ADDITIONAL_PROMPTS = {
    "default_branch": "[Extra] Name for the default branch",
    "full_name":  "  [1/3] Your name",
    "email": "  [2/3] Your email",
    "use_git": "  [3/3] Would you like to initialize a git repository?",

    "save_mail":"[Extra] No email or a different one was found in git config, do you want to save this email to it?",
    "save_name":"[Extra] No name or a different one was found in git config, do you want to save this name to it?"
}


class AdditionalPrompts(Extension):
    def __init__(self, environment):
        """Jinja2 Extension Constructor."""
        super().__init__(environment)

        def branch_name(var_name, default=None):
            MAX_ATTEMPTS = 5
            branch_name = prompt_user(var_name, default)
            for attempt in range(MAX_ATTEMPTS):
                try:
                    subprocess.check_call(
                        ["git", "check-ref-format", "--branch", branch_name],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                    return branch_name
                except subprocess.CalledProcessError:
                    if attempt == MAX_ATTEMPTS - 1:
                        print(
                            f"Max attempts reached. Invalid branch name '{branch_name}'. Will use 'main' as default branch. Exiting."
                        )
                        return "main"
                    else:
                        print("Please try again.")
                        branch_name = prompt_user(var_name, default)

        def get_user_name() -> str:
            try:
                output = subprocess.check_output(
                    ["git", "config", "user.name"], stderr=subprocess.DEVNULL
                )
                return output.decode().strip()
            except subprocess.CalledProcessError:
                return "Name"

        def get_user_email() -> str:
            try:
                output = subprocess.check_output(
                    ["git", "config", "user.email"], stderr=subprocess.DEVNULL
                )
                return output.decode().strip()
            except subprocess.CalledProcessError:
                return "Email"

        def prompt_user(var_name, default=None):
            return read_user_variable(var_name, default, prompts=ADDITIONAL_PROMPTS)

        def prompt_user_choices(var_name, choices):
            return read_user_choice(
                var_name, options=choices, prompts=ADDITIONAL_PROMPTS
            )

        def prompt_user_yes_no(var_name, default=True):
            return read_user_yes_no(var_name, default, prompts=ADDITIONAL_PROMPTS)

        def ask_to_save(info, type):
            if type == "email":
                to_save = prompt_user_yes_no("save_mail")
                if to_save:
                    try:
                        subprocess.check_call(['git', 'config', '--global',  '--add', 'user.email', info], 
                                              stdout=subprocess.DEVNULL,
                                              stderr=subprocess.DEVNULL)
                    except subprocess.CalledProcessError as e:
                        print(f"Error saving name: {e}")
                    
            elif type == "name":
                to_save = prompt_user_yes_no("save_name")
                try:
                    subprocess.check_call(['git', 'config', '--global',  '--add', 'user.name', info],
                                           stdout=subprocess.DEVNULL,
                                           stderr=subprocess.DEVNULL)
                except subprocess.CalledProcessError as e:
                    print(f"Error saving name: {e}")
            else:
                print(f"Not a valid type {type}.")
        

        # Make these functions available to the Jinja2 context
        environment.globals.update(
            prompt_user=prompt_user,
            prompt_user_choices=prompt_user_choices,
            prompt_user_yes_no=prompt_user_yes_no,
            branch_name=branch_name,
            get_user_name=get_user_name,
            get_user_email=get_user_email,
            ask_to_save=ask_to_save,
        )
