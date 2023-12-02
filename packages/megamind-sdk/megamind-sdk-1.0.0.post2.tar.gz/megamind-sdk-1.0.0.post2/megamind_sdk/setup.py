from setuptools import setup

packages = [
    "megamind_sdk",
    "megamind_sdk.utils",
    "megamind_sdk.api",
]

package_data = {"": ["*"]}

setup_kwargs = {
    "name": 'megamind-sdk',
    "version": '1.0.0-2',
    "description": 'MegaMind will provide you with some utils',
    "author": "MegaMind",
    "packages": packages,
    "package_data": package_data,
    "python_requires": ">=3.6,<4.0",
}

setup(**setup_kwargs)
