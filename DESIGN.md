# General
I'm considering adding an early exit feature such that a decryption process can exit when it is confident it has found the correct plaintext. A way to implement this would be to have a scoring function set a flag when its sure that you can exit, or a similar. Implementing this would involve some architectural changes, so I havent done this yet, still thinking about it.

# Simple Substitution
- Investigate better starting positions(from freq analysis) instead of just random?
- Simulated annealing
