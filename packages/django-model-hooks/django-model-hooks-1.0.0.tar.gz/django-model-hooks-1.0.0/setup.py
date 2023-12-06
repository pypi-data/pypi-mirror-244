from setuptools import setup, find_namespace_packages
from model_hooks.version import Version


setup(name='django-model-hooks',
     version=Version('1.0.0').number,
     description='Model hooks for Django',
     long_description=open('README.md').read().strip(),
     long_description_content_type="text/markdown",
     author='Bram Boogaard',
     author_email='bram@luggo.nl',
     url='https://gitlab.com/luggagecare/django-model-hooks',
     packages=find_namespace_packages(include=['model_hooks', 'model_hooks.migrations']),
     include_package_data=True,
     install_requires=[
         'pytest',
         'pytest-cov',
         'pytest-django',
         'django~=4.2.7'
     ],
     license='MIT License',
     zip_safe=False,
     keywords='Django Model hooks',
     classifiers=['Development Status :: 3 - Alpha'])
