from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

''' For dev creation - '''
# setup(
#     name='amplabs-dev',
#     packages=find_packages(),
#     version='0.0.1',
#     description='Amplabs Library',
#     author='Amplabs',
#     install_requires=['dash'],
# )


''' For prod creation '''
setup(
    name='amplabs',
    packages=find_packages(),
    version='0.0.4',
    description='One of the AmpLabs production to create high end plots for your data',
    author='Amplabs',
    install_requires=['dash'],
    readme = "README.md",
    long_description=long_description,
    ong_description_content_type="text/markdown",
)