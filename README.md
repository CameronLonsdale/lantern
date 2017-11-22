# lantern

[![Documentation Status](https://readthedocs.org/projects/lantern-crypto/badge/?version=latest)](http://lantern-crypto.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.org/CameronLonsdale/lantern.svg?branch=master)](https://travis-ci.org/CameronLonsdale/lantern)
[![Coverage Status](https://coveralls.io/repos/github/CameronLonsdale/lantern/badge.svg?branch=master)](https://coveralls.io/github/CameronLonsdale/lantern?branch=master)

**lantern** is a cryptanalysis library to assist with the identification and breaking of classical ciphers. The library provides general purpose analysis tools, as well as premade modules to break well known ciphers.

```python
from lantern.modules import caesar
from lantern import fitness

ciphertext = "iodj{EuxwhIrufhLvEhvwIrufh}"

decryptions = caesar.crack(ciphertext, fitness.english.quadgrams)
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

Python 3.4 or newer required.

lantern has no external dependencies outside of the standard library.

## Usage

As a library, lanterns functionality can be used in REPL or pre-written scripts. 
The library aims to be highly modular and generalised, providing the user with the ability to extend / modify / combine functions
with others to solve particular problems.

[Example programs](examples)

## Development

### Testing

Setup a virtual environment.

```
virtualenv -p python3.5 venv
source ./venv/bin/activate
```

Install development requirements.

`pip install -Ur dev_requirements.txt`

Use `py.test` to run tests using your current working environment.

Use `tox -r` to build a new environment for each python version and run all tests.

### Documentation

Document is built using [sphinx](http://www.sphinx-doc.org) and [napoleon-sphinx](https://sphinxcontrib-napoleon.readthedocs.io).

Install documentation requirements.

`pip install -Ur docs/requirements.txt`

Build the HTML, output in `build/html`.

`make html`
