
import os

from setuptools import setup, find_packages

with open('aws_sat_api/__init__.py') as f:
    for line in f:
        if line.find("__version__") >= 0:
            version = line.split("=")[1].strip()
            version = version.strip('"')
            version = version.strip("'")
            continue


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


# Runtime requirements.
inst_reqs = ["boto3"]

extra_reqs = {
    'test': ['mock', 'pytest', 'pytest-cov', 'codecov']}

setup(name='aws_sat_api',
      version=version,
      description=u"""""",
      long_description="""""",
      python_requires='>=3',
      classifiers=[
          'Intended Audience :: Information Technology',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 3.6',
          'Topic :: Scientific/Engineering :: GIS'],
      keywords='',
      author=u"Vincent Sarago",
      author_email='contact@remotepixel.ca',
      url='https://github.com/remotepixel/aws-sat-api-py',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=inst_reqs,
      extras_require=extra_reqs)
