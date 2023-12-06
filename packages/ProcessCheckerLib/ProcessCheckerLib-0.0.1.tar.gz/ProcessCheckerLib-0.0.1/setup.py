from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='ProcessCheckerLib',
  version='0.0.1',
  author='brambleaka',
  author_email='sambuka11jail@outlook.com',
  description='This is lib for ProcessesCheckerBot.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='',
  packages=find_packages(),
  install_requires=['requests','flask','schedule','psutil','dotenv'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='files speedfiles ',
  project_urls={},
  python_requires='>=3.8'
)
