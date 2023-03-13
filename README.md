# polaris_utils

<!-- TODO: Add badges -->
<!-- [![PyPI version](https://badge.fury.io/py/mdlearn.svg)](https://badge.fury.io/py/mdlearn) -->
<!-- [![Documentation Status](https://readthedocs.org/projects/mdlearn/badge/?version=latest)](https://mdlearn.readthedocs.io/en/latest/?badge=latest) -->

Polaris submission utilities 

For more details and specific examples of how to use polaris_utils, please see our [documentation](https://readthedocs.org/).

## Table of Contents
- [polaris_utils](#polarisutils)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
    - [Install latest version with PyPI](#install-latest-version-with-pypi)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [Acknowledgments](#acknowledgments)
  - [License](#license)

## Installation

### Install latest version

```
git clone https://github.com/ramanathanlab/polaris_utils.git
pip3 install -r requirements/requirements.txt
pip3 install .
``` 

### Installing in `develop` mode
*Recomended to use conda virtual environment*
```
conda create -n [env_name] python=3.9
pip3 install --upgrade pip setuptools wheel
pip3 install -r requirements/dev.txt
pip3 install -r requirements/requirements.txt
pip3 install -e .
```

## Usage

To run an arbitrary command through polaris using this package use the following command:

```
python -m polaris_utils.submit -a [ACCONT] -q [QUEU_NAME] -t [TIME] -n [NNODES] -j [JOBNAME] --extras "[PRERUN_COMMANDS]" --command "[COMMAND]"
```
_Note: the `--extras` and `--command` arguments must be escaped with strings_ 

An example is shown here: 

```
python -m polaris_utils.submit -a [ACCOUNT] -q debug -t 1:00:00 -n 2 -j polaris_utils_ex --extras "module load conda/2022-09-08; conda activate my_env" --command "python -m genslm_develop.train --config /lus/eagle/projects/CVD-Mol-AI/github/genslm-develop/configs/polaris-multi.yaml"
```
_Note: this example is not a valid command, but is meant to show the structure of the command_

## Contributing

Please report **bugs**, **enhancement requests**, or **questions** through the [Issue Tracker](https://github.com/KPHippe/polaris_utils/issues).

If you are looking to contribute, please see [`CONTRIBUTING.md`](https://github.com/KPHippe/polaris_utils/blob/main/CONTRIBUTING.md).


## Acknowledgments

TODO

## License

<!-- polaris_utils has a TODO license, as seen in the [LICENSE](https://github.com/ramanathanlab/mdlearn/blob/main/LICENSE) file. -->
