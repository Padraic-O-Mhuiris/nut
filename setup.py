from setuptools import setup

setup(
    name="nut",
    version="0.1",
    packages=["nut"],
    package_dir={"nut": "src"},
    install_requires=[
        # List your dependencies here
        # e.g., 'requests>=2.25.1',
    ],
    entry_points={
        "console_scripts": [
            # If you want to create a command-line command to run main.py
            "project-name = main:main_function",
        ],
    },
)
