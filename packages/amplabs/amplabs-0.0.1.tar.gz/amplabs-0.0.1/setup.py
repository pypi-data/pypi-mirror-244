from setuptools import find_packages, setup


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
    version='0.0.1',
    description='One of the AmpLabs production to create high end plots for your data',
    author='Amplabs',
    install_requires=['dash'],
)