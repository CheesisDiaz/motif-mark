## OOP Motif Mark ##

### Goals ###

Create a python object-oriented code to visualize motifs on sequences. 

### Requirements ###

To run this code you require two files

    - Motif file. This needs to contain all possible motif types, 
    if a nucleotide can be either "t" or "c" will be represented with a "y". 
    For example if a motif type is tcgt or tcgc can be represented as *ycgy*.

    - Sequence file. The sequence must be on a fasta file. 
    The exon of the sequence must be indicated in capital letters.

#### Packages ####

    -  Pycairo

#### Modules ####

    - re
    - cairo
    - argparse
    - random

#### How to run the program ####

As mentioned previously, the code requires two files which must be inputed as parameters. 

```
./motif-mark-oop.py -f <sequence_file> -m <motif_file>
```

### Output ###

The output of this program will result in a png file that will contain a diagram per sequence that will include the introns, exons and motif type (coloured by type).
