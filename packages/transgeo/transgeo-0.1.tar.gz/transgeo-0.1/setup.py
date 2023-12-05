from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='transgeo',
    version='0.1',
    description='Transformations géomètriques',
    long_description_content_type='text/markdown',
    long_description=long_description,
    url='https://x.com/david_cobac',
    author='David COBAC',
    author_email='david.cobac@gmail.com',
    keywords=['géométrie',
              'transformations'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    license='CC-BY-NC-SA',
    # packages=find_packages(),
    packages=find_packages()
)
