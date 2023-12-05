from setuptools import setup, find_packages

setup(
    name="polychromy",
    version="0.0.2",
    packages=find_packages(),
    package_data={"polychromy": ["data/colors.json"]},
    install_requires=["textlinebreaker >= 0.1.0 "],  # Add any dependencies here
    entry_points={
        "console_scripts": [
            "polychromy = polychromy.polychromy:color_show"  # Command to call the package
        ],
    },
    # other setup configurations...
)
