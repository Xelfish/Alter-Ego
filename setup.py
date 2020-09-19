from setuptools import find_packages, setup

setup(
    name="alterego",
    version="1.0",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "pillow",
        "opencv-python",
        "rembg",
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib"
    ],
)