#!/usr/bin/env python3
import argparse
import os, shutil
from subprocess import Popen

def get_venv_exe(exe):
    return os.path.abspath(os.path.join(get_venv_exe.PATH, 'bin', exe))


def mkdir_repo(git_path):
    if not os.path.exists(git_path):
        print("Creating directory:", git_path)
        os.mkdir(git_path)

def create_repo(git_path):
    if os.path.exists(os.path.join(git_path, ".git")):
        print("Git repository exists, ignoring.")
    else:
        Popen(['git', 'init', git_path]).wait()

def create_venv(venv_path, python):
    if os.path.exists(venv_path):
        print("Virtualenv exists, ignoring.")
    else:
        Popen(['virtualenv', '--python={}'.format(python), venv_path]).wait()

def pip_generate_requirements(git_path, pip_reqs=[]):
    reqpath = os.path.join(git_path, 'requirements.txt')
    with open(reqpath, 'w') as fo:
        fo.write('\n'.join(pip_reqs))
        fo.write('\n')
    fo.close()

def pip_install_requirements(git_path):
    reqpath = os.path.join(git_path, 'requirements.txt')
    Popen([get_venv_exe('pip'), 'install', '-r{}'.format(reqpath)]).wait()

def django_create_project(git_path, name):
    Popen([get_venv_exe('django-admin.py'), 'startproject', name], cwd=git_path).wait()


def get_args():
    parser = argparse.ArgumentParser(description='Quick-start a Django project.')
    parser.add_argument('--create-repo',
                        action='store_true',
                        dest='create_repo',
                        help='create a git repo')
    parser.add_argument('--create-venv',
                        action='store_true',
                        dest='create_venv',
                        help='create a virtualenv')
    parser.add_argument('--venv-path',
                        type=str,
                        dest='venv_path',
                        help='outer path to virtualenv environment')
    parser.add_argument('--path',
                        type=str,
                        dest='path',
                        help='outer path (defaults to current directory)')
    parser.add_argument('--python',
                        type=str,
                        dest='python',
                        default='python3',
                        help='Name of or path to python executable')
    parser.add_argument('name',
                        metavar='NAME',
                        type=str,
                        help='Django project name')

    return parser.parse_args()

def main():
    args = get_args()

    outer_path = args.path or '.'
    outer_path = os.path.abspath(outer_path)

    git_path = os.path.join(outer_path, args.name)
    django_path = os.path.join(git_path, args.name)

    venv_path = args.venv_path or '~/.virtualenvs'
    venv_path = os.path.join(os.path.expanduser(venv_path), args.name)
    get_venv_exe.PATH = venv_path
    DJANGO_VERSION = '1.10'

    python = shutil.which(args.python) or args.python

    print("outer_path:", outer_path)
    print("\tgit:", git_path)
    print("\tdjango:", django_path)
    print("venv:", venv_path)
    print("\tpython:", python)

    mkdir_repo(git_path)

    if args.create_repo:
        create_repo(git_path)

    if args.create_venv:
        create_venv(venv_path, python)

    pip_reqs = [
        'Django~={}'.format(DJANGO_VERSION),
    ]
    pip_generate_requirements(git_path, pip_reqs)
    pip_install_requirements(git_path)

    django_create_project(git_path, args.name)

    #django_warp_project(django_path, args.name)


if __name__ == '__main__':
    main()

#repo/
#  project/
#    wsgi.py
#    settings.py
#    secret.py
#    apps/
#      app1/
#        models.py
#        views.py
#        urls.py
#    static/
#    templates/
