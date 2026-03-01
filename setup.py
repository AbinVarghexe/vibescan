from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vibescan",
    version="0.1.0",
    description="A pre-publish security analysis tool to detect AI hallucinated dependencies and slopsquatting.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="VibeScan Contributors",
    author_email="",
    url="https://github.com/yourusername/vibescan",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "colorama>=0.4.4",
        "packaging>=21.3"
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-mock>=3.10.0",
            "responses>=0.20.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "vibescan=vibescan.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "Topic :: Software Development :: Quality Assurance",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.7",
    keywords="security ai slopsquatting hallucination dependencies npm pypi",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/vibescan/issues",
        "Source": "https://github.com/yourusername/vibescan",
    },
)