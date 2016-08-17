import os
from setuptools import setup, find_packages


version = "0.0"

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django-pages",
    version = version,
    description = "",
    long_description = read("README.rst"),
    classifiers = [],
    keywords = "",
    author = "Bryan Chow",
    author_email = "",
    url = "https://github.com/bryanchow/django-pages",
    download_url = "https://github.com/bryanchow/django-pages/tarball/master",
    license = "WTFPL",
    packages = find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'django',
    ],
)
