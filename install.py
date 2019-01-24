#!/usr/bin/env python3

import os
import subprocess
import pathlib


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
    command = 'python3 -m venv {venv_name}'.format(venv_name=venv_name).split()
    subprocess.run(command)


def install_venv(venv_name, path):
    os.chdir(path)
    subprocess.run(
        'source {venv_name}/bin/activate; pip install --upgrade pip setuptools wheel'.format(
            venv_name=venv_name
        ),
        shell=True,
        executable='/bin/bash',
    )
    subprocess.run(
        'source {venv_name}/bin/activate; pip install -r {requirements_path}/requirements.txt'.format(
            venv_name=venv_name,
            requirements_path='/{base}/venvs/data-science'.format(base='test'),
        ),
        shell=True,
        executable='/bin/bash',
    )
    subprocess.run(
        'source {venv_name}/bin/activate; pip freeze'.format(venv_name=venv_name),
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


def main():
    # venvs_dir_path = make_venv_base_dir('test')
    # venvs_dir_path = make_venv_base_dir('~/test')
    venvs_dir_path = make_venv_base_dir('/data/test')
    create_venv('data-science', venvs_dir_path)
    install_venv('data-science', venvs_dir_path)


if __name__ == '__main__':
    main()
