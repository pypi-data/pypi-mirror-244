import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gogclient",
    version="0.1.0",
    author="Patrick Menschel",
    author_email="menschel.p@posteo.de",
    description="A client for requests to GOG.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/menschel/gogclient",
    packages=setuptools.find_packages(exclude=["tests", ]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.7",
    keywords="gogrepo requests",
    install_requires=["requests", "lxml", "tqdm", "tomli"],
    scripts=["bin/gogrepo", "bin/gogdiscounts"],
    data_files=[('~/', ['data/gogrepo.toml'])]
)
