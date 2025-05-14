from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='firewall_project',
    version='0.1',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'python-dotenv', 
        'scapy',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'firewall=firewall:main',
        ],
    },
    description='Firewall Project',
    long_description=long_description,
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
