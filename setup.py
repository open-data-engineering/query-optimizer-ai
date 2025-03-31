from setuptools import setup, find_packages

setup(
    name="query-optimizer-ai",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={
        "commons": ["py.typed"],
    },
    install_requires=[
        "faker",
        "pydantic",
        "pydantic[email]",
        "numpy",
        "pandas",
        "pytest",
        "pytest-cov",
        "pytest-mock",
    ],
)