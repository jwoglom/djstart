#!/usr/bin/env python3
import argparse
import os, shutil
from subprocess import Popen

def get_venv_exe(exe):
    return os.path.abspath(os.path.join(get_venv_exe.PATH, 'bin', exe))


def create_venv(venv_path, python):
    if os.path.exists(venv_path):
        print("Virtualenv exists, continuing...")
    else:
        Popen(['virtualenv', '--python={}'.format(python), venv_path]).wait()

def pip_generate_requirements(outer_path, pip_reqs=[]):
    reqpath = os.path.join(outer_path, 'requirements.txt')
    with open(reqpath, 'w') as fo:
        fo.write('\n'.join(pip_reqs))
        fo.write('\n')
    fo.close()

def pip_install_requirements(outer_path):
    reqpath = os.path.join(outer_path, 'requirements.txt')
    Popen([get_venv_exe('pip'), 'install', '-r{}'.format(reqpath)]).wait()

def django_create_project(outer_path, name):
    if os.path.exists(os.path.join(outer_path, name, 'manage.py')):
        print("Project exists, continuing...")
    else:
        Popen([get_venv_exe('django-admin.py'), 'startproject', name], cwd=outer_path).wait()

def pip_move_requirements(outer_path, name):
    oldreqs = os.path.join(outer_path, 'requirements.txt')
    if os.path.exists(oldreqs):
        shutil.move(oldreqs, os.path.join(outer_path, name, 'requirements.txt'))

def create_repo(repo_path):
    if os.path.exists(os.path.join(repo_path, ".git")):
        print("Git repository exists, continuing...")
    else:
        Popen(['git', 'init', repo_path]).wait()

def django_create_default_app(repo_path, name, app_name='core'):
    managepy = os.path.join(repo_path, 'manage.py')
    apps = os.path.join(repo_path, name, 'apps')
    if not os.path.exists(apps):
        os.mkdir(apps)
    if os.path.exists(os.path.join(apps, app_name)):
        print("App", app_name, "already exists, continuing...")
    else:
        Popen([managepy, 'startapp', app_name], cwd=apps).wait()

def django_warp_project(repo_path, name):
    pass
    

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

    repo_path = os.path.join(outer_path, args.name)
    project_path = os.path.join(repo_path, args.name)

    venv_path = args.venv_path or '~/.virtualenvs'
    venv_path = os.path.join(os.path.expanduser(venv_path), args.name)
    get_venv_exe.PATH = venv_path
    DJANGO_VERSION = '1.10'

    python = shutil.which(args.python) or args.python

    print("outer_path:", outer_path)
    print("\tgit:", repo_path)
    print("\tdjango:", project_path)
    print("venv:", venv_path)
    print("\tpython:", python)

    if args.create_venv:
        create_venv(venv_path, python)

    pip_reqs = [
        'Django~={}'.format(DJANGO_VERSION),
    ]
    pip_generate_requirements(outer_path, pip_reqs)
    pip_install_requirements(outer_path)

    django_create_project(outer_path, args.name)

    pip_move_requirements(outer_path, args.name)

    create_repo(repo_path)

    django_create_default_app(repo_path, args.name)
    django_warp_project(repo_path, args.name)


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
