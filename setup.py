import setuptools
import scrap_revuedepresse

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name="scrap_revuedepresse",
        version=scrap_revuedepresse.__version__,
        author="dbeley",
        author_email="dbeley@protonmail.com",
        description="Scrap the content of the revuedepreses website",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/dbeley/scrap_revuedepresse",
        packages=setuptools.find_packages(),
        include_package_data=True,
        entry_points={
            "console_scripts": [
                "scrap_revuedepresse=scrap_revuedepresse.__main__:main"
                #"scrap_revuedepresse_simple=scrap_revuedepresse.scrap_revuedepresse_simple:main"
                ]
            },
        classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: POSIX :: Linux"
            ],
        install_requires=[
            'bs4',
            'urllib3',
            'requests',
            'lxml',
            ]
        )
