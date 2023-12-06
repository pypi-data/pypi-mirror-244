from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

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
    package_data={'amplabs': ['assets/*']},
    version='0.0.6',
    description='One of the AmpLabs production to create high end plots for your data',
    author='Amplabs',
    install_requires=['dash'],
    readme = "README.md",
    long_description=long_description,
    long_description_content_type="text/markdown",
)