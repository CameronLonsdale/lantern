# lantern

[![Documentation Status](https://readthedocs.org/projects/lantern-crypto/badge/?version=latest)](http://lantern-crypto.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.org/CameronLonsdale/lantern.svg?branch=master)](https://travis-ci.org/CameronLonsdale/lantern)
[![Coverage Status](https://coveralls.io/repos/github/CameronLonsdale/lantern/badge.svg?branch=master)](https://coveralls.io/github/CameronLonsdale/lantern?branch=master)

**lantern** is a cryptanalysis library to assist with the identification and breaking of classical ciphers. The library provides general purpose analysis tools, as well as premade modules to break well known ciphers.

```python
from lantern.modules import shift
from lantern import fitness

ciphertext = "iodj{EuxwhIrufhLvEhvwIrufh}"

decryptions = shift.crack(ciphertext, fitness.english.quadgrams)
print(decryptions[0])
```

In short, lantern can be used to:

+ **Identify** ciphers from ciphertext
+ **Automatically crack** well known ciphers
+ **Analyze** ciphertext to assist in the breaking of custom crypto systems

## Installation

```
pip3 install -U lantern
```

## Documentation

Full documentation available at [lantern-crypto.readthedocs.io](https://lantern-crypto.readthedocs.io)

## Requirements

Python 3.7 required.

lantern has no external dependencies outside of the standard library.

## Usage

As a library, lanterns functionality can be used in REPL or pre-written scripts. 
The library aims to be highly modular and generalised, providing the user with the ability to extend / modify / combine functions
with others to solve particular problems.

[Example programs](examples)

## Development

### Testing

1. Setup a virtual environment.

```
virtualenv -p python3.7 venv
source ./venv/bin/activate
```

2. Install development requirements.

```
pip3 install -Ur dev_requirements.txt
```

3. Use `py.test` to run tests using your current working environment.

4. Use `tox` to build a new environment for each python version and run all tests.

### Documentation

Document is built using [sphinx](http://www.sphinx-doc.org) and [napoleon-sphinx](https://sphinxcontrib-napoleon.readthedocs.io).

1. Install documentation requirements.

```
pip3 install -Ur docs/requirements.txt
```

2. Build the HTML from inside `/docs`, output in `build/html`.

```
make html
```
