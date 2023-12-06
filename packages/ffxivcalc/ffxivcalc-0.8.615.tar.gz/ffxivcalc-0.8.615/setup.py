from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()


setup(
    name="ffxivcalc",  # Required
    version="0.8.615",  # Required
    package_dir={"": "src"},  # Optional,
    packages=find_packages(where="src"),  # Required
    python_requires=">=3.10",
    install_requires=[  "contourpy",
                        "cycler",
                        "fonttools",
                        "kiwisolver",
                        "matplotlib",
                        "numpy",
                        "packaging",
                        "Pillow",
                        "pyparsing",
                        "python-dateutil",
                        "six",
                        "coreapi"],  # Optional
)