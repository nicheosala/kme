from setuptools import setup

setup(
    name='kme',
    version='1.0.0',
    packages=['KME', 'KME.models', 'KME.controllers'],
    url='',
    license='',
    author='Nicolò Sala',
    author_email='nicolo4.sala@mail.polimi.it',
    description='Key Management Entity',
    python_requires='>=3.10',
    install_requires=[
        "connexion~=2.9.0",
        "jsons~=1.6.0",
        "setuptools~=58.5.3"
    ],
    tests_require=[],  # TODO
    entry_points={
        'console_scripts': ['qkd=KME.__main__:main']
    },
    package_data={'': ['../api/openapi.yaml']}
)
