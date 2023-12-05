from io import open

from setuptools import find_packages, setup

setup(
    name="CEScore",
    version="0.0.1",
    author="Al Motasem Bellah Al Ajlouni",
    author_email="eng.motasem@ymail.com",
    description="Set of an automatic metrics to evaluate the  simplicity, meaning preservation, and grammaticality of a simplified text by comparing it with the original complex text as a reference.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    keywords=["metric", "simplicity", "meaning preservation", "grammaticality" , "text simplification", "split and rephrase"],
    license="MIT",
    url="https://github.com/motasemajlouni/CEScore",
    #packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    packages=find_packages(),
    install_requires=["nltk","numpy","pandas","requests"],
    entry_points={"console_scripts" : ['CEScore=CEScore.__main__:main']},
    include_package_data=True,
    python_requires=">=3.6",
    tests_require=["pytest"],
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
