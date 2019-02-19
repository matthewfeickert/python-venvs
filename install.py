#!/usr/bin/env python3

import os
import subprocess
import pathlib
import json


def install_poetry():
    """
    Install Poetry if it is not already installed
    """
    try:
        # TODO: Use a more POSIX method of which
        command = 'which poetry'.split()
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print('# Installing Poetry\n')
        print(
            '## curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python3'
        )
        # Need to split response across
        command_curl_poetry = 'curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py'.split()
        # curl_poetry = subprocess.run(command_curl_poetry, stdout=subprocess.PIPE)
        curl_poetry = subprocess.Popen(command_curl_poetry, stdout=subprocess.PIPE)
        # print(curl_poetry)

        # install_poetry = 'curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python3'.split()
        # print(install_poetry)
        # install_poetry = subprocess.run(
        install_poetry = subprocess.Popen(
            ['python3'], stdin=curl_poetry.stdout, stdout=subprocess.PIPE
        )
        # Allow curl_poetry to receive a SIGPIPE if process_wc exits.
        curl_poetry.stdout.close()
        install_poetry.communicate()

        HOME = os.environ['HOME']
        with open(f'{HOME}/.bashrc', 'a') as bashrc:
            bashrc.write(f'\n# Added for Poetry\nsource {HOME}/.poetry/env\n')
    return 0


def make_venv_base_dir(path):
    """
    Make the venv directory to keep things clean

    Args:
        path `str`: The path at which venvs should be made

    Returns:
        absolute_path: The absolute path to the venvs directory
    """
    absolute_path = os.path.join(
        pathlib.Path(os.path.expanduser(path)).absolute(), 'venvs'
    )
    os.makedirs(absolute_path, exist_ok=True)
    return absolute_path


def create_venv(venv_name, path):
    """
    Make a python3 venv at the path

    Args:
        venv_name `str`
        path `str`
    """
    os.chdir(path)
    command = f'python3 -m venv {venv_name}'.split()
    subprocess.run(command)


def install_venv(venv_name, path, __PYTHONVENVS_DIR):
    create_venv(venv_name, path)

    os.chdir(path)
    subprocess.run(
        f'source {venv_name}/bin/activate; pip install --upgrade pip setuptools wheel',
        shell=True,
        executable='/bin/bash',
    )
    HOME = os.environ['HOME']
    # requirements_path = os.environ['PYTHONVENVS_DIR'] + '/venvs/' + venv_name
    requirements_path = __PYTHONVENVS_DIR + '/venvs/' + venv_name
    # subprocess.run(
    #     f'source {HOME}/.bashrc; source {HOME}/.poetry/env; source {venv_name}/bin/activate; cd {requirements_path}; poetry install',
    #     shell=True,
    #     executable='/bin/bash',
    # )
    subprocess.run(
        f'source {venv_name}/bin/activate; cd {requirements_path}; poetry install',
        shell=True,
        executable='/bin/bash',
    )

    # command = 'source {venv_name}/bin/activate ; pip --version ; pip install --upgrade pip setuptools wheel ; pip freeze'.format(venv_name=venv_name).split()
    # print(command)
    # subprocess.run(command,
    #     executable='/bin/bash',
    # )
    # subprocess.call('./{venv_name}/bin/activate; pip --version'.format(venv_name=venv_name), shell=True, executable='/bin/bash')
    # command = './{venv_name}/bin/activate'.format(venv_name=venv_name).split()
    # print(command)
    # # command = 'touch test.txt'.split()
    # process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    # proc_stdout = process.communicate()[0].strip()
    # print(proc_stdout)


def set_project_path(path=None, config_name='config.json'):
    if path is None:
        path = os.getcwd()
    location = {'location': f'{path}'}
    with open(config_name, 'w') as location_json:
        json.dump(location, location_json)
    return 0


def main():
    if not os.path.isfile('config.json'):
        install_poetry()
        # subprocess.run(
        #     'bash {PWD}/set_location.sh'.format(PWD=os.getcwd()),
        #     shell=True,
        #     executable='/bin/bash',
        # )
        set_project_path()
        print('\n#Please run\n# source $HOME/.bashrc\n')
        exit(0)
    else:
        with open('config.json') as config:
            __PYTHONVENVS_DIR__ = json.load(config)['location']

    # FIXME: Temporary test path
    HOME = os.environ['HOME']
    venvs_dir_path = make_venv_base_dir(f'{HOME}/test')

    install_venv('data-science', venvs_dir_path, __PYTHONVENVS_DIR=__PYTHONVENVS_DIR__)


if __name__ == '__main__':
    main()
