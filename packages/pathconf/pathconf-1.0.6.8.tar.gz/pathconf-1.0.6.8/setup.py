from setuptools import setup, find_packages
# Read the contents of your README file
with open('README.md') as f:
    long_description = f.read()


def read_version():
    version = {}
    with open("version.py") as fp:
        # Executes the code within version.py,
        # but within the 'version' dictionary's scope.
        exec(fp.read(), version)
    return version['__version__']


setup(
    name='pathconf',
    version=read_version(),  # Use the version from version.py
    packages=find_packages(),
    description='Uses os.walk to find and catalogue a given file. Built to call some scripts from inside others on different machines since onedrive kept giving itself a random path and was a pain to manage',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Sam Kirby',
    author_email='sam.kirby@gagamuller.com',
    install_requires=[
        # Any dependencies you have, e.g., 'requests', 'numpy', etc.
    ],
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.org/classifiers/
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.1',
)