from setuptools import setup

setup(
    name = 'mplanetypes',
    version = 0.1,
    description = "A few utility type-checking functions that I use a lot.",
    long_description = "A few utility type-checking functions that I use a lot.",
    long_description_content_type = "text/plain",
    author = "Michael P. Lane",
    author_email = "mlanetheta@gmail.com",
    url = "https://github.com/automorphis/mplanetypes",
    package_dir = {"": "lib"},
    packages = [
        "mplanetypes"
    ],
    install_requires = [
        'numpy',
    ],
    classifiers = [
        "Programming Language :: Python",
    ],
    zip_safe = False
)