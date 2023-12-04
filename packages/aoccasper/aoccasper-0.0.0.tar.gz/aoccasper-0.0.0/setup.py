import os
from pathlib import Path
from shutil import rmtree, copytree, ignore_patterns

from setuptools import setup, find_packages
os.environ["PWD"] = os.getcwd()

# This should be changed.
pkg_name = "aoccasper"
new_version = "0.0.0"  # The starting version.

should_remove_copy = False
try:  # To copy the base level into setup folder to treat this as its own package.
    src_path = Path(os.environ["PWD"], f"../../{pkg_name}")
    dst_path = Path(f"./{pkg_name}")

    copytree(src_path, dst_path, ignore=ignore_patterns("setup"))
    should_remove_copy = True
except FileNotFoundError:
    print("Could not copy tree")

try:
    import requests
    from packaging import version

    CONTENT_TYPES = [
        "application/vnd.pypi.simple.v1+json",
        "application/vnd.pypi.simple.v1+html;q=0.2",
        "text/html;q=0.01",  # For legacy compatibility
    ]
    ACCEPT = ", ".join(CONTENT_TYPES)
    # result = requests.get(f"https://test.pypi.org/simple/{pkg_name}/", headers={"Accept": ACCEPT})
    result = requests.get(f"https://pypi.org/simple/{pkg_name}/", headers={"Accept": ACCEPT})
    if result:
        max_version = max(map(version.parse, result.json()["versions"]))
        new_version = f"{max_version.major}.{max_version.minor}.{max_version.micro + 1}"
except Exception as e:  # Can't think of why this should fail.
    raise e


try:
    setup(
        name=pkg_name,
        version=new_version,
        packages=find_packages(),
        author="Casper Chris Adriaan Bekkers",
        author_email="casperbekkers@hotmail.com",
        long_description=open("README.md", "r").read(),
        #include_package_data=True,
        install_requires=[
        ]
    )
except Exception as e:
    raise e
finally:
    #  Still remove even is setup breaks.
    if should_remove_copy:
        rmtree(dst_path)
