"""
Somn - 汇千古之智，向未知而生
"""

from setuptools import setup, find_packages
from pathlib import Path

# 读取 README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding='utf-8') if readme_path.exists() else ""

# 读取 requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    with open(requirements_path, 'r', encoding='utf-8') as f:
        requirements = [
            line.strip() 
            for line in f 
            if line.strip() and not line.startswith('#')
        ]

setup(
    name="smartoffice-ai",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="汇千古之智，向未知而生。能持续学习成长的超级智能体",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/smartoffice-ai",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-qt>=4.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ]
    },
    # entry_points removed — project uses src layout with smart_office_assistant.src
    # Install via: pip install -e smart_office_assistant/
    include_package_data=True,
    package_data={
        "": ["*.yaml", "*.json", "*.txt", "*.md"],
    },
)
