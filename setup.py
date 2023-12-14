from setuptools import find_packages  # type: ignore
from setuptools import setup  # type: ignore

if __name__ == "__main__":
    name = "text2music"
    version = "1.0.0"
    python_requires = ">=3.10,<3.11"
    description = "A simple text to music app using Python"
    packages = find_packages(include=["text2music", "text2music.*"])
    install_requires = [
        "diffusers",
        "torch",
        "gradio",
        "transformers",
        "scipy",
    ]
    extras_require = {
        "development": ["isort", "mypy", "black", "Flake8-pyproject", "pytest", "pytest-cov"]
    }

    setup(
        name=name,
        version=version,
        description=description,
        python_requires=python_requires,
        packages=packages,
        install_requires=install_requires,
        extras_require=extras_require,
        entry_points={},  # Define here any scripts you want to run from the command line
    )
