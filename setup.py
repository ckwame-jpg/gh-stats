from setuptools import find_packages, setup

setup(
    name="gh-stats",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0",
        "rich>=13.0",
        "httpx>=0.28",
    ],
    entry_points={
        "console_scripts": [
            "gh-stats=gh_stats.cli:cli",
        ],
    },
    python_requires=">=3.9",
)
