# cckrypto

cckrypto is a cryptanalysis framework to assist in the automated identification and breaking of ciphertexts.

## Goal

One click identify and decrypt a piece of ciphertext

## Future plans

- [ ] Adaptive scoring to speed up decryption.
- [ ] Identification process for ciphertext.
- [ ] Multithreading.
- [ ] Support for more Classical Ciphers.
- [ ] Support for Modern Cryptographic Ciphers.

## Installation
```
git clone git@github.com:CameronLonsdale/cckrypto.git
pip install -e ./cckrypto
```

## Usage

cckrypto's usage is for it's modules to be imported into custom scripts written by the user. The modules aim to be generalised cryptoanalysis functions which the user can extend / modify / combine with other changes to solve particular problems.

### Example for cracking substitution cipher using ngram analysis

```
from cckrypto.modules import simplesubstitution
from cckrypto.score_functions import ngram

ciphertext = """Tmlk fqp oaiazpa, qda kluai oabafuar kazo tkfuaopzi zbbizfj. Ziqdltcd Rfbhakp' blkqajmlozox Qdljzp Bzoixia oasaooar ql fq rfpmzozcfkcix zp qdzq "Mfm klkpakpa," da kauaoqdaiapp oazbqar ql azbd soapd fkpqzijakq vfqd "olzop ls iztcdqao."Izqao, Caloca Eaokzor Pdzv mozfpar qda kluai, zp "Zii ls lka mfaba zkr blkpfpqakqix qotqdsti." Rtofkc qda paofzi mteifbzqflk, Rfbhakp vzp miazpar vfqd mteifb oapmlkpa ql Coazq Awmabqzqflkp zkr fqp pziap; vdak qda milq sfopq slojar fk dfp jfkr, da bziiar fq "z uaox sfka, kav zkr colqapnta fraz."""""

print(simplesubstitution.crack(ciphertext, [ngram.quadgram])[0])
```

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`.
3. Commit your changes: `git commit -am 'Add some feature'`.
4. Push to the branch: `git push origin my-new-feature`.
5. Submit a pull request.
