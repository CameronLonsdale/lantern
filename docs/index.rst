********************************
lantern: automated cryptanalysis
********************************

**lantern** is a cryptanalysis library to assist with the identification and breaking of classical ciphers. The library provides general purpose analysis tools, as well as premade modules to break well known ciphers. ::

    from lantern.modules import caesar
    from lantern import fitness

    ciphertext = "iodj{EuxwhIrufhLvEhvwIrufh}"

    decryptions = caesar.crack(ciphertext, fitness.english.quadgrams)
    print(decryptions[0])


In short, lantern can be used to:

+ **Identify** ciphers from ciphertext
+ **Automatically crack** well known ciphers
+ **Analyze** ciphertext to assist in the breaking of custom crypto systems

Install
=======

.. code-block:: bash

    pip3 install -U lantern

Guide
=====

Coming Soon

API Reference
=============

.. toctree::
   :maxdepth: 2

   lantern.score
   lantern.util
   lantern.modules
   lantern.analysis
   lantern.fitness
   lantern.structures
