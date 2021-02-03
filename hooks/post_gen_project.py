from pathlib import Path


### Utility functions

def exit_program_early():

    print('Exiting')

    exit(1)

def gather_user_input(prompt,input_prompt='?'):

    response = None

    while response is None:

        print(prompt)

        response = input(input_prompt).strip()

        if not response:
            
            print('Please provide a valid response or type \'exit\' and hit the Enter key to exit the program.')

            response = None

        elif response.lower() == 'exit':

            exit_program_early()

    return response

def gather_user_confirmation(prompt):

    response = gather_user_input(prompt,input_prompt='[Y/N] > ').upper()[0]

    return response[0] =='Y'


### Ensure the python script was copied into the directory.
def confirm_script_copied():

    input('Copy your python script into the generated directory named {{cookiecutter.name}} and hit the "Enter" key to continue.')

    return Path('.').joinpath(f'{{cookie_cutter.script_name}}.py').exists()

while not confirm_script_copied():

    print('''
A script named {{cookie_cutter.script_name}}.py could not be found
in the directory named {{cookiecutter.name}}.

A script named {{cookie_cutter.script_name}}.py MUST be found in the 
directory {{cookiecutter.name}} for this process to continue.''')

    if not gather_user_confirmation('Try again?'): exit_program_early()

    print('Ok, let\'s try this again.')

# ======================================================================

### Git work

import re
import subprocess

def run_command(cmd,do_execute=True):

    if do_execute:

        try:

            subprocess.run(cmd,check=True)

        except:

            return False

    else:

        print(' '.join(cmd))

    return True

def gather_tag():

    tag = None

    while tag is None:

        tag = gather_user_input('What tag should be used? (Must be in format v#.#.# E.g. v1.0.0)')

        tag = tag if re.match(r'v\d\.\d\.\d') else None

        if not tag: print('Make sure your tag is in the format v#.#.# (E.g. v1.0.0)')

    return tag

'''
    run git init
    Ask user if they want to push their new repo
        ask user for git repo url
        ask user if they want to tag repo
            ensure tag is in correct format
        build command
'''

if gather_user_confirmation('Push results to Github?'):

    do_execute_git_commands = run_command(['git','--version'])

    if not do_execute_git_commands:

        print('''
Oh no! It looks like git isn't installed and/or available from the command line on your system.

The process will continue, but instead of executing the git commands they will be printed out.

Copy and save them. Once you have git properly set up on your system, open a command prompt
in your project's directory and run the commands.

The things to check are:

    1. Git is installed on your system (https://github.com/git-guides/install-git)
    2. Git is available on the command line. You'll know if you can open a command prompt, run 'git --version' and get a response similar to 'git version 2.17.1'''')

    git_initialized = run_command(['git','init','-b','main'],do_execute_git_commands)

    if not git_initialized: # What are the chances this would happen?

        print('It looks like there was an issue creating the git repo.')

        exit_program_early()

    if gather_user_confirmation('Push results to a remote GitHub repository?'):

        if gather_user_confirmation('Tag the results?'):

            tag = gather_tag()

        else:

            tag = None

        remote_url = gather_user_input('What\'s the remote url?')

        if gather_user_confirmation('Do you want to specify your commit message? Default will be "INITIAL COMMIT"'):

            commit_message = gather_user_input('What commit message would you like to use?')

        else:

            commit_message = 'INITIAL COMMIT'

        commit_message = f'"{commit_message}"' # Is this necessary?

        run_command(['git','add','-A'],do_execute_git_commands)

        run_command(['git','commit','-m',commit_message],do_execute_git_commands)

        if tag:

            tag_message = f'"Version {tag[1:]}"'

            run_command(['git','tag','-a',tag,'-m',tag_message],do_execute_git_commands)

            run_command(['git','push','--follow-tags'],do_execute_git_commands)

        else:

            run_command(['git','push'],do_execute_git_commands)



