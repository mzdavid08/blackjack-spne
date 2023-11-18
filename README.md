# Blackjack SPNE
CSCI455 Game Theory group repository created by Nathan Ard and David Meraz.

## Getting Started

### Install
- Use Python 3.10
- Run `git clone https://github.com/mzdavid08/blackjack-spne.git` to pull the repo

### Use
- To run the tree generator, run `python3 blackjack_tree.py [starting value] [stop number] [output file name]`
- To run the SPNE calculation, run `python3 spne_calculation.py [output file name]`

### Tips
- All parameters are optional for both programs
- The stop number for the tree generator must be less than or equal to twenty-one
- There exists a pre-computed SPNE map in the form of a pickle file under `output` which has been included due to its small file size and the time complexity of the SPNE calculator
- As the generated trees have large file sizes, we have not included them in this repository