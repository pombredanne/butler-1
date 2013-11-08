# -*- coding: UTF-8 -*-
from distutils.command.install import INSTALL_SCHEMES
from distutils.core import setup
from setuptools import find_packages
import os
import re
import time


_version = "0.1.%sdev0" % int(time.time())
_packages = find_packages('butler', exclude=["*.tests", "*.tests.*", "tests.*", "tests"])


# make sure that data files go into the right place
# see http://groups.google.com/group/comp.lang.python/browse_thread/thread/35ec7b2fed36eaec/2105ee4d9e8042cb
for scheme in INSTALL_SCHEMES.values(): 
    scheme['data'] = scheme['purelib']


# find any static content such as HTML files or CSS
_INCLUDE = re.compile("^.*\.(html|less|css|js|png|gif|jpg|mo|eot|svg|ttf|woff|otf|json|conf|txt|ico)$")
_root_directory='butler'


def get_package_data():
    package_data = {}
    for pkg in os.listdir(_root_directory):
        pkg_path = os.path.join(_root_directory, pkg)
        if os.path.isdir(pkg_path):
            package_data[pkg] = create_paths(pkg_path)
    return package_data


def create_paths(root_dir):
    paths = []
    is_package = os.path.exists(os.path.join(root_dir, '__init__.py'))
    children = os.listdir(root_dir)
    for child in children:
        childpath = os.path.join(root_dir, child)
        if os.path.isfile(childpath) and not is_package and _INCLUDE.match(child):
            paths.append(child)
        if os.path.isdir(childpath):
            paths += [os.path.join( child, path ) for path in create_paths( os.path.join(root_dir, child) ) ]
    return paths


_reqs_dir = os.path.join(os.path.dirname(__file__), 'requirements')


def _strip_comments(line):
    return line.split('#', 1)[0].strip()


def _get_reqs(req):
    with open(os.path.join( _reqs_dir, req ) ) as f:
        requires = f.readlines()
        requires = map(_strip_comments, requires)
        requires = filter( lambda x:x.strip()!='', requires )
        return requires

_install_requires = _get_reqs('common.txt')
_extras_require = {
    'psql': _get_reqs('psql.txt'),
}

_data_files = [('', ['requirements/%s' % reqs_file for reqs_file in os.listdir(_reqs_dir)])]


setup(
    name='butler',
    version=_version,
       
    packages=_packages,
    package_dir={'': 'butler'},
    package_data=get_package_data(),
       
    install_requires=_install_requires,
    extras_require=_extras_require,

    data_files=_data_files,

    author='Akvo.org',
    author_email='code@akvo.org',
    url='https://github.com/akvo/akvo-butler',

    license='Affero GPL',
)
