from setuptools import setup
def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(name='TestMyFirstProjectLibrary',
      long_description=readme(),
      version='0.0.2',
      description='Gaussian and Binomial distributions',
      packages=['TestMyFirstProjectLibrary'],
      author_email='akim.petbu@gmail.com',
      zip_safe=False)
