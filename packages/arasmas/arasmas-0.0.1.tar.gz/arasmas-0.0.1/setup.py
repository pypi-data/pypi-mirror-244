from setuptools import setup, find_packages

setup(
    name="arasmas",
    version="0.0.1",
    author="Knu",
    author_email="minu928@snu.ac.kr",
    url="https://github.com/MyKnu/Samsara",
    download_url="https://github.com/MyKnu/Samsara/",
    install_requies=["numpy>=1.22.4", "yaml>=6.0.1", "scipy>=1.10.4", "tqdm>=4.66", "ase>=3.19"],
    description="Frame workf of Generative Learning for MLFF",
    packages=find_packages(),
    keywords=["MLFF", "LAMMPS", "CP2K"],
    python_requires=">=3.7",
    package_data={"": ["*"]},
    # entry_points={
    #     # make the scripts available as command line scripts
    #     "console_scripts": [
    #         "arasmas-run = samsaralearn.cli.run:main",
    #     ]
    # },
    zip_safe=False,
)
