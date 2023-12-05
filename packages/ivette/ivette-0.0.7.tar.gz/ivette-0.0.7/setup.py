from setuptools import setup

# Read deps
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='ivette',
    version='0.0.7',
    description='Python client for Ivette Computational chemistry and Bioinformatics project',
    author='Eduardo Bogado',
    py_modules=['ivette', 'ivette.fileIO_module', 'ivette.IO_module', 'ivette.load_module',
                'ivette.run_module', 'ivette.supabase_module'],  # Include 'ivette.py' as a module
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'ivette=ivette:main',
        ],
    },
)
