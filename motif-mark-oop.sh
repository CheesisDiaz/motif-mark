#!/bin/bash

fasta="Figure_1.fasta"
# fasta="/Users/cheesis/bioinfo/Bi625/Assignments/OOP_Motif_Mark/motif-mark/test.fa"
motifs="Fig_1_motifs.txt"

./motif-mark-oop.py \
    -f $fasta \
    -m $motifs \