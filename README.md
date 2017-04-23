# lantern

TODO: Logo

TODO: Jenkins auto builds

TODO: Coveralls

lantern is a cryptanalysis library to assist in the identification and cracking of ciphertext.

| Supported Python Implementations |
| ---------------------------------|
| Python 2.7                       |
| Python 3.5                       |
| PyPy                             |

## Installation
```
git clone git@github.com:CameronLonsdale/lantern.git
pip install -e ./lantern
```

## Usage

lanterns's usage is for it's modules to be imported into custom scripts written by the user. The modules aim to be generalised cryptoanalysis functions which the user can extend / modify / combine with other changes to solve particular problems.

Recommended usage with PyPy for maximum speed.

TODO: Proper documentation for the library

[Example programs](examples)

## Development

### Testing

TODO: Why doesnt this actually work? It should.

Use `py.test` to run tests using your current working environment

Use `tox -r` to build a new environment for each python version and run all unit tests

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`.
3. Commit your changes: `git commit -am 'Add some feature'`.
4. Push to the branch: `git push origin my-new-feature`.
5. Submit a pull request.
