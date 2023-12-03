import os.path
import sys

from setuptools import setup, find_namespace_packages

# Don't import joshydev_ml module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "joshydev_ml"))

version_file = os.path.join(os.path.dirname(__file__), "version.txt")
with open(version_file) as file_handler:
    __version__ = file_handler.read().strip()

setup(
    name="joshydev_ml",
    version=__version__,
    description="Gym And StableBaselines3",
    author="JoshyDev",
    packages=find_namespace_packages(include=["joshydev_ml*"]),
    zip_safe=False,
    install_requires=[
        "numpy>=1.18.0",
        "cloudpickle>=1.2.0",
        "importlib_metadata>=4.8.1; python_version < '3.8'",
    ],
    package_data={
        "joshydev_ml": [
            "version.txt",
            "gym/envs/mujoco/assets/*.xml",
            "gym/envs/classic_control/assets/*.png",
            "gym/envs/robotics/assets/LICENSE.md",
            "gym/envs/robotics/assets/fetch/*.xml",
            "gym/envs/robotics/assets/hand/*.xml",
            "gym/envs/robotics/assets/stls/fetch/*.stl",
            "gym/envs/robotics/assets/stls/hand/*.stl",
            "gym/envs/robotics/assets/textures/*.png",
        ]
    },
    tests_require=["pytest", "mock"],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
