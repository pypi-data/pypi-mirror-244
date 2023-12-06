from setuptools import setup, find_packages

setup(
    name='newbookapi',
    version='0.1.0',
    author='Manzar nouman',
    author_email='manzarnouman@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests',  # Add other dependencies as needed
    ],
    description='A Python client for the Newbook API.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://www.travelresorts.com/',  # Replace with your repository URL
    classifiers=[
        # Classifiers help users find your project
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    project_urls={
        'Source': 'https://github.com/TridentMarketing/newbook-api/tree/packagify'
    },
    python_requires='>=3.6',
)