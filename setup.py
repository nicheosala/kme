from setuptools import setup, find_packages

setup(
    name='kme',
    version='1.0.0',
    packages=find_packages(),
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
    entry_points={
        'console_scripts': ['qkd=kme.__main__:main']
    },
    package_data={'': ['api/openapi.yaml']}
)
