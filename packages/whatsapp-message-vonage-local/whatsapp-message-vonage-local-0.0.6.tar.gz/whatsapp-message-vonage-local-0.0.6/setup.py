"imports"
import setuptools
# Each Python project should have pyproject.toml or setup.py
# used by python -m build
# ```python -m build``` needs pyproject.toml or setup.py
# The need for setup.py is changing as of poetry 1.1.0 (including current pre-release)
# as we have moved away from needing to generate a setup.py file to enable editable installs -
# We might able to delete this file in the near future
setuptools.setup(
    name='whatsapp-message-vonage-local',
    version='0.0.6',  # https://pypi.org/project/<project-name>/
    author="Circles",
    author_email="info@circles.life",
    description="PyPI Package for Circles <project-name> Local/Remote Python",
    long_description="This is a package for sharing common XXX function used in different repositories",
    long_description_content_type="text/markdown",
    url="https://github.com/circles-zone/whatsapp-message-vonage-local-python-package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
         "License :: Other/Proprietary License",
         "Operating System :: OS Independent",
    ],
    # TODO: Update which packages to include with this package
    install_requires=[
        'logzio-python-handler>= 4.1.0',
        'phonenumbers>=8.13.25'
    ],
)
