from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()


setup(
    name="ffxivcalc",  # Required
    version="0.8.613",  # Required
    package_dir={"": "src"},  # Optional,
    packages=find_packages(where="src"),  # Required
    python_requires=">=3.10, <4",
    install_requires=[  "contourpy>=1.0.5",
                        "cycler>=0.11.0",
                        "fonttools>=4.37.2",
                        "kiwisolver>=1.4.4",
                        "matplotlib>=3.6.0",
                        "numpy>=1.23.3",
                        "packaging>=21.3",
                        "Pillow>=9.2.0",
                        "pyparsing>=3.0.9",
                        "python-dateutil>=2.8.2",
                        "six>=1.16.0",
                        "coreapi>=2.3.3"],  # Optional
)