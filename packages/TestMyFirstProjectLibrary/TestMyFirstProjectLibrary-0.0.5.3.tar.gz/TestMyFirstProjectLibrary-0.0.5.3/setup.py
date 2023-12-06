from setuptools import setup
def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(name='TestMyFirstProjectLibrary',

      version='0.0.5.3',
      description='None',

      packages=['TestMyFirstProjectLibrary'],
      author_email='akim.petbu@gmail.com')
