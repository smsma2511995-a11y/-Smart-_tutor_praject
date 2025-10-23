# setup.py
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="smarttutor-pro",
    version="1.0.0",
    description="النظام التعليمي الذكي المتكامل متعدد اللغات",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="SmartTutor Team",
    author_email="contact@smarttutor.com",
    packages=find_packages(),
    python_requires=">=3.8, <4",
    install_requires=[
        "torch>=2.0.0",
        "transformers>=4.30.0",
        "sentence-transformers>=2.2.0",
        "numpy>=1.24.0",
        "scikit-learn>=1.3.0",
        "pymupdf>=1.22.0",
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "kivy>=2.3.0",
        "kivymd>=1.1.1",
        "pathlib",
        "regex>=2023.10.0"
    ],
    extras_require={
        "dev": ["pytest", "pytest-cov", "black", "flake8"],
    },
    entry_points={
        "console_scripts": [
            "smarttutor=run:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Education :: Computer Aided Instruction (CAI)",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="education, ai, tutor, multilingual, arabic",
    project_urls={
        "Source": "https://github.com/your-username/smarttutor-pro",
        "Bug Reports": "https://github.com/your-username/smarttutor-pro/issues",
    },
)
