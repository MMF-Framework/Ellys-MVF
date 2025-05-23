# setup.py

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ellys-mvf",
    version="1.0.0",
    author="MMF-Framework",
    author_email="contact@mmf-framework.org",
    description="MMF Ellys Minimum Viable Framework - 전략 실행 프레임워크",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MMF-Framework/Ellys-MVF",
    project_urls={
        "Bug Tracker": "https://github.com/MMF-Framework/Ellys-MVF/issues",
        "Documentation": "https://github.com/MMF-Framework/Ellys-MVF/docs",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Scheduling",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "ellys-mvf=mvf.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "mvf": [
            "templates/**/*",
            "system/**/*",
        ],
    },
)