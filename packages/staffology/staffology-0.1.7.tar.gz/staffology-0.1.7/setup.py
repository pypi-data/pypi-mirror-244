from setuptools import find_packages, setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='staffology',
    version='0.1.7',
    packages=find_packages(),
    url='https://github.com/ihorizonUK/staffology',
    description="Staffology openapi client with authentication patch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='isik-kaplan',
    author_email='isik@ihorizon.co.uk',
    python_requires=">=3.7",
    install_requires=['httpx', "attrs"],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 5 - Production/Stable',
    ],
)
