from setuptools import setup, find_packages

setup(
    name='firewall_project',
    version='0.1',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'python-dotenv', 
        'scapy',
        'requests',
        'altgraph==0.17.2',
        'future==0.18.2',
        'macholib==1.15.2',
        'six==1.15.0',
        'wheel==0.44.0',
    ],
    entry_points={
        'console_scripts': [
            'firewall=firewall:main',
        ],
    },
    description='Firewall Project',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Sofia Soto',
    author_email='sofia.soto@utp.edu.co',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)