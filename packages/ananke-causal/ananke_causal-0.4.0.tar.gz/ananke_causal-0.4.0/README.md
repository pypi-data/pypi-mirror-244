# Ananke

Visit the [website](https://ananke.readthedocs.io) to find out more.

[Ananke](https://en.wikipedia.org/wiki/Ananke), named for the Greek
primordial goddess of necessity and causality, is a python package for
causal inference using the language of graphical models

## Contributors

* Rohit Bhattacharya 
* Jaron Lee
* Razieh Nabi 
* Preethi Prakash
* Ranjani Srinivasan

Interested contributors should check out the [CONTRIBUTING.md](CONTRIBUTING.md) for further details.

## Installation

If graph visualization is not required then install via `pip`:

```
pip install ananke-causal
```

Alternatively, the package may be installed from gitlab by cloning and `cd` into the directory. Then, `poetry` (see https://python-poetry.org) can be used to install:

```
poetry install
```

### Install with graph visualization


If graphing support is required, it is necessary to install [graphviz](https://www.graphviz.org/download/).


#### Non M1 Mac instructions
Ubuntu:
```shell script
sudo apt install graphviz libgraphviz-dev pkg-config
```

Mac ([Homebrew](https://brew.sh/)):
```shell script
brew install graphviz
```

Fedora:
```shell script
sudo yum install graphviz
```

Once graphviz has been installed, then:

```shell script
pip install ananke-causal[viz] # if pip is preferred

poetry install --extras viz # if poetry is preferred
```

#### M1 Mac specific instructions

If on M1 see this [issue](https://github.com/pygraphviz/pygraphviz/issues/398). The fix is to run the following before installing:
```shell script
brew install graphviz
python -m pip install \
    --global-option=build_ext \
    --global-option="-I$(brew --prefix graphviz)/include/" \
    --global-option="-L$(brew --prefix graphviz)/lib/" \
    pygraphviz
```
