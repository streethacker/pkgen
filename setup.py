from setuptools import setup, find_packages


requires = []

setup(
    name='pkgen',
    version='0.1',
    description='Primary Key Generator Implemented In Python',
    author='YUCHI',
    author_email='wei.chensh@ele.me',
    packages=find_packages(),
    url='https://github.com/streethacker/pkgen',
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
)
