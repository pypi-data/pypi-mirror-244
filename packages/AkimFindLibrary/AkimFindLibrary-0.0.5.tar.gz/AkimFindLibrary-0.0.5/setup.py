from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='AkimFindLibrary',
  version='0.0.5',
  author='Akim_b',
  author_email='akim.petbu@gmail.com',
  description='This is the simplest module for EGE Number 24.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/Akello1',
  packages=['AkimFindLibrary'],
  install_requires=['requests>=2.24.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='file',
  project_urls={
    'GitHub': 'https://github.com/Akello1'
  },
  python_requires='>=3.6'
)