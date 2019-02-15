import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    include_package_data=True,
    package_data={'linestar': ['static/date_ids.json']},
    name="linestar-scrape",
    version="1.0.9",
    author="Brendan Hart",
    author_email="brendanahart@gmail.com",
    description="A package to scrape linestarapp.com daily fantasy sports ownership data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WolverineSportsAnalytics/linestar-scrape",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)