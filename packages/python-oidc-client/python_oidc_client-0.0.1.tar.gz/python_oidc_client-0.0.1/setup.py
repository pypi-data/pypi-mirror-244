from setuptools import setup, find_packages

setup(
    name='python_oidc_client',
    version='0.0.1',  # Update this version as per your package development
    author='IDPartner',
    author_email='engineering-external@idpartner.com',
    description='A Python client for interacting with OpenID Connect providers.',
    long_description="""The IDPartner gem offers a Python client for OpenID Connect providers, streamlining
                        authorization, token acquisition, and user information retrieval. It supports various
                        authentication methods and handles endpoint discovery via well-known configuration. The
                        package simplifies JWT generation, signing, and verifying, making OpenID Connect integration
                        straightforward and secure.""",
    url='https://github.com/idpartner-app/python_oidc_client',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'authlib',
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
