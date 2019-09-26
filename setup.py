import setuptools
import scrap_revuedepresse

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scrap_revuedepresse",
    version=scrap_revuedepresse.__version__,
    author="dbeley",
    author_email="dbeley@protonmail.com",
    description="Scrap newspaper covers from a variety of sources",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dbeley/scrap_revuedepresse",
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "scrap_revuedepresse=scrap_revuedepresse.__main__:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=[
        "beautifulsoup4",
        "urllib3",
        "requests",
        "lxml",
        "pandas",
        "selenium",
        "opencv-python",
    ],
)
