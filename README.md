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

Recommended usage with PyPy for maximum speed

TODO: Proper documentation for the library
TODO: Examples folder

### Example for cracking substitution cipher using ngram analysis

```
from lantern.modules import simplesubstitution
from lantern.score_functions import ngram

ciphertext = """Tmlk fqp oaiazpa, qda kluai oabafuar kazo tkfuaopzi zbbizfj. Ziqdltcd Rfbhakp' blkqajmlozox Qdljzp Bzoixia oasaooar ql fq rfpmzozcfkcix zp qdzq "Mfm klkpakpa," da kauaoqdaiapp oazbqar ql azbd soapd fkpqzijakq vfqd "olzop ls iztcdqao."Izqao, Caloca Eaokzor Pdzv mozfpar qda kluai, zp "Zii ls lka mfaba zkr blkpfpqakqix qotqdsti." Rtofkc qda paofzi mteifbzqflk, Rfbhakp vzp miazpar vfqd mteifb oapmlkpa ql Coazq Awmabqzqflkp zkr fqp pziap; vdak qda milq sfopq slojar fk dfp jfkr, da bziiar fq "z uaox sfka, kav zkr colqapnta fraz."""""

print(simplesubstitution.crack(ciphertext, [ngram.quadgram])[0])
```

## Development

### Testing

TODO: Why does this actually work? It should.
Use `py.test` to run tests using your current working environment

Use `tox -r` to build a new environment for each python version and run all unit tests

### Future plans

- [ ] Adaptive scoring to speed up decryption.
- [ ] Identification process for ciphertext.
- [ ] Multithreading.
- [ ] Support for more Classical Ciphers.
- [ ] Support for Modern Cryptographic Ciphers.

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`.
3. Commit your changes: `git commit -am 'Add some feature'`.
4. Push to the branch: `git push origin my-new-feature`.
5. Submit a pull request.
