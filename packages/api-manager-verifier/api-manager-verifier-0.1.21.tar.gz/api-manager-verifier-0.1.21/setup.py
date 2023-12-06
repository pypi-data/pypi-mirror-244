import re
import setuptools

with open("README.txt", "r") as fh:
    long_description = fh.read()


def __get_version():
    with open("data_verifier/__init__.py") as file:
        return re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', file.read(), re.MULTILINE).group(1)


def __get_requirements():
    with open("requirements.txt") as file:
        return file.readlines()


setuptools.setup(
    name="api-manager-verifier",
    version=__get_version(),
    description='Project to manage the course registration of the dtu student',
    author='Ashish Kumar',
    long_description=long_description,
    url='https://github.com/Ashish2000L',
    packages=setuptools.find_packages(),
    install_requires=__get_requirements(),
    classifiers=[
        # https://pypi.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'License :: Free for non-commercial use',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Session',
        'Topic :: Software Development :: Libraries',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Content Management System',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
    ]
)
