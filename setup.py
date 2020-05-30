from setuptools import setup

setup(
    name='services_manager',
    version='0.1',
    description='application for manage services running on server',
    author='Alexander Vasiliev',
    author_email='asushofman@gmail.com',
    license='MIT',
    packages=['services_manager', 'logs', 'sqlite', 'templates'],
    zip_safe=False,
)
