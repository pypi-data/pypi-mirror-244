from setuptools import setup, find_packages
setup(
   name='my_package_anirudh',
   version='0.3',
   packages=find_packages(),
   install_requires=[
      'click',
   ],
   entry_points='''
      [console_scripts]
      my_cli_app=my_cli_app:hello
      ''',
)