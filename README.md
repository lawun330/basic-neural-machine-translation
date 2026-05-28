# Basic Neural Machine Translation

## Overview

This project implements a basic SMT system for Burmese grapheme-to-phoneme (G2P) translation using established SMT toolkits such as Moses, GIZA++, and MGIZA, along with custom preprocessing scripts for data normalization and preparation.

The workflow covers the full SMT pipeline from data normalization and SGM file generation to training, decoding, and evaluation. Multiple experiments are documented with varying settings. BLEU scores and translation outputs are systematically logged and summarized for comparative analysis.

## Error-Free PBSMT Workflow

- Use Ubuntu-native Perl v5.38
- Install Marian and dependencies (nvcc, gcc-11, nvidia-smi)
- Optionally configure paths in 
    - seq2seq.phmy.sh
- 

## Experiments


Summary: [presentation slides](presentation_slides.pdf)

Results:
| ![](img/1.png) | ![](img/2.png) |
|------------------------|-------------------------|

## Dataset

- [Sayar's G2P dataset](https://github.com/ye-kyaw-thu/AIE-F/tree/main/slide-code/class-13and14/data)

## File Structure
```
/
...
├── img/
├── notebooks/
├── models/
├── summary/
│
│
├── data/
│   ├── g2p-par/                    # originally Sayar's
│   ├── cleaned/                    # preprocessed data (version 1)
│   └── logs/
│
├── syl-normalizer/     # originally Sayar's # modified to merge with previous token for athat (်) cases
└── seq2seq.myph.sh     # originally Sayar's # modified paths
```

## References

- [In-Class Tutorial](https://github.com/ye-kyaw-thu/AIE-F/tree/main/slide-code/class-22/NMT-notebooks)
- ```
  @InProceedings{mariannmt,
      title     = {Marian: Fast Neural Machine Translation in {C++}},
      author    = {Junczys-Dowmunt, Marcin and Grundkiewicz, Roman and
                  Dwojak, Tomasz and Hoang, Hieu and Heafield, Kenneth and
                  Neckermann, Tom and Seide, Frank and Germann, Ulrich and
                  Fikri Aji, Alham and Bogoychev, Nikolay and
                  Martins, Andr\'{e} F. T. and Birch, Alexandra},
      booktitle = {Proceedings of ACL 2018, System Demonstrations},
      pages     = {116--121},
      publisher = {Association for Computational Linguistics},
      year      = {2018},
      month     = {July},
      address   = {Melbourne, Australia},
      url       = {http://www.aclweb.org/anthology/P18-4020}
  }
  ```

## Note

This project was done for educational purposes as an assignment for the AI Engineering Fundamentals class taught by [*Sayar Ye Kyaw Thu*](https://github.com/ye-kyaw-thu).
