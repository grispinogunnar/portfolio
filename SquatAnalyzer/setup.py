from setuptools import setup, find_packages

setup(
    name="barbell-tracker",
    version="1.0",
    description="A Python-based tool for barbell tracking and squat analysis.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Gunnar Grispino",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "PyQt5",
        "opencv-python",
        "mediapipe",
        "numpy",
    ],
    entry_points={
        "console_scripts": [
            "barbell-tracker=app:main",  # Command-line entry point
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
