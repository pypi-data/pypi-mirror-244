# CDO Local UUID Utility

[![Continuous Integration](https://github.com/Cyber-Domain-Ontology/CDO-Utility-Local-UUID/actions/workflows/cicd.yml/badge.svg)](https://github.com/Cyber-Domain-Ontology/CDO-Utility-Local-UUID/actions/workflows/cicd.yml)

This project provides a specialized UUID-generating function that can, on user request, cause a program to generate deterministic UUIDs.  Its main purpose is to assist with generating version-controllable example data using consistent identifiers.  This package intentionally includes mechanisms to make it difficult to activate this non-random mode without awareness of the caller.


## Disclaimer

Participation by NIST in the creation of the documentation of mentioned software is not intended to imply a recommendation or endorsement by the National Institute of Standards and Technology, nor is it intended to imply that any specific software is necessarily the best available for the purpose.


## Installation

This repository can be installed from PyPI or from source.


### Installing from PyPI

```bash
pip install cdo-local-uuid
```

### Installing from source

Users who wish to install pre-release versions and/or make improvements to the code base should install in this manner.

1. Clone this repository.
2. (Optional) Create and activate a virtual environment.
3. Run `pip install $x`, where `$x` is the path to the cloned repository.

Local installation is demonstrated in the `.venv.done.log` target of the `tests/` directory's [`Makefile`](tests/Makefile).


## Usage

[This module](cdo_local_uuid/__init__.py) provides a wrapper UUID generator, `local_uuid()`.  It is intended to replace the Python call sequence `str(uuid.uuid4())`.  In the default behavior, the two idioms behave the same:

```python
>>> from uuid import uuid4
>>> from cdo_local_uuid import local_uuid
>>> str(uuid4())
'168ec24a-4920-43f5-85ad-9c6088b0cad8'
>>> local_uuid()
'bd203d75-f3eb-40fe-a266-b447beadbd54'
```

However, for some code-demonstration purposes, deterministic UUIDs might be desired, e.g. so a demonstration file including generated UUIDs can be regenerated and only change when the code changes, reducing version-control noise.

To see how to configure UUID generation, see the `_demo_uuid` function in [this module](cdo_local_uuid/__init__.py).


## Development status

This repository follows [CASE community guidance on describing development status](https://caseontology.org/resources/software.html#development_status), by adherence to noted support requirements.

The status of this repository is:

4 - Beta


## Versioning

This project follows [SEMVER 2.0.0](https://semver.org/) where versions are declared.


## Dependencies

This repository's primary module was originally part of the [`case-utils`](https://github.com/casework/CASE-Utilities-Python) package.  It was separated to provide a package with no runtime dependencies outside of the Python standard library.


## Make targets

Some `make` targets are defined for this repository:
* `check` - Run unit tests.
* `clean` - Remove test build files, but not downloaded files.


## Licensing

This repository is licensed under the Apache 2.0 License. See [LICENSE](LICENSE).

Portions of this repository contributed by NIST are governed by the [NIST Software Licensing Statement](THIRD_PARTY_LICENSES.md#nist-software-licensing-statement).
