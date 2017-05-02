********************************
lantern: automated cryptanalysis
********************************

**lantern** is a cryptanalysis library to assist with the identification and breaking of classical ciphers. The library provides general purpose analysis tools, aswell as premade modules to break well known classic ciphers. ::

    from lantern.modules import caesar
    from lantern.score_functions import english_scorer

    ciphertext = """iodj{EuxwhIrufhLvEhvwIrufh}"""

    decryptions = caesar.crack(ciphertext, [english_scorer.quadgrams()])
    best_decryption = decryptions[0]
    print(best_decryption.plaintext)

In short, lantern can be used to:

* **Identify** ciphers from ciphertext
* **Auotomatically crack** well known ciphers
* **Analyze** ciphertext to assist in the breaking of custom crypto systems

Install
=======
.. code-block:: bash

    git clone git@github.com:CameronLonsdale/lantern.git
    pip install -e ./lantern

Guide
=====
Coming Soon


API Reference
=============
.. toctree::
   :maxdepth: 2

   lantern.modules
   lantern.analysis
   lantern.score_functions
   lantern.structures
   lantern
