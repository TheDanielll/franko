from setuptools import setup, find_packages

def get_version():
    with open("Franko/__init__.py", "r") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"\'')
    raise RuntimeError("Unable to find version string.")

setup(
    name="Franko",
    version=get_version(),
    packages=find_packages(),
    package_data={
        'Franko': ['decline.bundle.js'],
    },
    install_requires=["setuptools>=61.0", "wheel", "pydantic"],
    extras_require={
        'dev_deps ': [
            'pytest'
        ]
    },
    license="MIT",
    license_files=("LICENSE",),
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Text Processing :: Linguistic',
    ],

    include_package_data=True,
    description="Project for declension of Ukrainian names",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Danila Aleksandrov",
    author_email="danila.alexandrov24@gmail.com",
    python_requires='>=3.10',
)