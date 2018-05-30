import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='observable-collections',
    version='0.1.2',
    description='Rx based collections that supports change notification',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Shiyam S',
    author_email='austin.shyam@gmail.com',
    license='MIT',
    download_url='https://github.com/shyam-s00/ObservableCollections',

    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha"
    ),
    install_requires=['rx']
)
