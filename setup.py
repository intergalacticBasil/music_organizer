from setuptools import setup, find_packages

setup(
    name="music_organizer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "watchdog>=2.1.9",
        "beets>=1.6.0",
    ],
    entry_points={
        "console_scripts": [
            "music-organizer=music_organizer.__main__:main",
        ],
    },
    python_requires=">=3.6",
)