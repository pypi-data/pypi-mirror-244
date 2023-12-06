from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='calculate-1-0',
    version='0.1',
    license='MIT License',
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords='calculate-for-students-1-0',
    description=u'Library not official',
    packages=['calculate'],
    install_requires=['openai'],)