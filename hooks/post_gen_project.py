import os
os.system('python --version')
from pathlib import Path
import traceback


try:

    DO_GIT_INIT = "{{ cookiecutter.do_init_git_repo }}"[0] == "Y"

    DO_PUSH_TO_GITHUB = (
        DO_GIT_INIT and "{{ cookiecutter.do_push_repo_to_github }}"[0] == "Y"
    )

    ### Utility functions

    def exit_program_early():

        print("Exiting")

        exit(1)

    def gather_user_input(prompt, input_prompt="?"):

        response = None

        while response is None:

            print(prompt)

            response = input(input_prompt).strip()

            if not response:

                print(
                    "Please provide a valid response or type 'exit' and hit the Enter key to exit the program."
                )

                response = None

            elif response.lower() == "exit":

                exit_program_early()

        return response

    def gather_user_confirmation(prompt):

        response = gather_user_input(prompt, input_prompt="[Y/N] > ").upper()[0]

        return response[0] == "Y"

    ### Ensure the python script was copied into the directory.
    def confirm_script_copied():

        input(
            'Copy your python script into the generated directory named {{cookiecutter.name}} and hit the "Enter" key to continue.'
        )

        return Path(".").joinpath("{{cookiecutter.script_name}}.py").exists()

    while not confirm_script_copied():

        print(
            """
A script named {{cookiecutter.script_name}}.py could not be found
in the directory named {{cookiecutter.name}}.

A script named {{cookiecutter.script_name}}.py MUST be found in the 
directory {{cookiecutter.name}} for this process to continue."""
        )

        if not gather_user_confirmation("Try again?"):
            exit_program_early()

        print("Ok, let's try this again.")

    # ======================================================================

    ### Requirements work

    req_path = Path('requirements.txt')

    if gather_user_confirmation('Would you like to add requirements to requirements.txt?'):

        reqs = gather_user_input('Ok, please provide a comma separated list of your requirements. (E.g. pandas, tqdm)')

        req_str = '\n'.join([
            req.strip()
            for req
            in reqs.split(",")
        ])

        with open(req_path,'w') as out_file:

            out_file.write(req_str)

    else:

        req_path.unlink()        

    # ======================================================================

    ### Git work

    import re
    import subprocess

    def run_command(cmd, do_execute=True):

        if do_execute:

            try:

                subprocess.run(cmd, check=True)

            except Exception as e:

                print(
                    """
Oh no! It looks like there was an issue running the command:

    {0}
    
The problem was:

    {1}

The process will continue, but instead of executing the git commands they will be printed out.

Copy and save them for later use after the errors have been resolved.
""".format(" ".join(cmd),str(e))
                )

                return False

        else:

            print(" ".join(cmd))

        return do_execute

    def run_multiple_commands(cmds, do_execute_git_commands):

        for cmd in cmds:

            do_execute_git_commands = run_command(cmd, do_execute_git_commands)

        return do_execute_git_commands

    def gather_tag():

        tag = None

        while tag is None:

            tag = gather_user_input(
                "What tag should be used? (Must be in format v#.#.# E.g. v1.0.0)"
            )

            tag = tag if re.match(r"v\d\.\d\.\d", tag) else None

            if not tag:
                print("Make sure your tag is in the format v#.#.# (E.g. v1.0.0)")

        return tag

    if DO_GIT_INIT:

        do_execute_git_commands = run_command(["git", "--version"])

        if not all(
            [
                run_command(["git", "init"], do_execute_git_commands),
                run_command(["git", "checkout", "-b", "main"], do_execute_git_commands),
            ]
        ):  # What are the chances this would happen?

            print("It looks like there was an issue creating the git repo.")

            exit_program_early()

        if DO_PUSH_TO_GITHUB:

            remote_url = gather_user_input("What's the remote url?")

            do_execute_git_commands = run_multiple_commands(
                [
                    ["git", "remote", "add", "origin", remote_url],
                    ["git","add","-A"],
                    ["git","commit","-m","INITIAL COMMIT"],
                    ["git", "push", "--set-upstream", "origin", "main"],
                ],
                do_execute_git_commands,
            )

            if gather_user_confirmation("Tag the results?"):

                tag = gather_tag()

            else:

                tag = None

            if tag:

                tag_message = '"Version {0}"'.format(tag[1:])

                do_execute_git_commands = run_multiple_commands(
                    [
                        ["git", "tag", "-a", tag, "-m", tag_message],
                        ["git", "push", "--follow-tags"],
                    ],
                    do_execute_git_commands,
                )

except Exception as e:

    traceback.print_exc()

    exit(6)
