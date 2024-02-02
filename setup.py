from setuptools import setup, find_packages
import os


with open(os.path.join(os.path.dirname(__file__), "epyt_flow/VERSION"),
          "r", encoding="utf-8") as f_version:
    version = f_version.read().strip()

def readme():
    with open("README.md", "r", encoding="utf-8") as f_readme:
        return f_readme.read()


setup(name='epyt-flow',
      version=version,
      description='EPyT-Flow -- EPANET Python Toolkit - Flow',
      long_description=readme(),
      keywords='epanet, water, networks, hydraulics, quality, simulations',
      url='https://github.com/WaterFutures/EPyT-Flow',
      author='André Artelt',
      author_email='aartelt@techfak.uni-bielefeld.de',
      license='MIT',
      python_requires='>=3.9',
      packages=find_packages(),
      include_package_data=True,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Science/Research',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.9'
          ],
      zip_safe=False)
