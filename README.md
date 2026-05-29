# Basic Neural Machine Translation

## Overview

This project implements a basic NMT system for Burmese grapheme-to-phoneme (G2P) translation using an established toolkit such as Marian NMT, along with custom preprocessing scripts for data normalization.

The workflow covers the full NMT pipeline from data normalization, training, and evaluation. Multiple experiments are documented with varying settings. BLEU scores and translation outputs are systematically logged and summarized for comparative analysis.

## Error-Free NMT Workflow

- Use Ubuntu-native Perl v5.38
- Install Marian NMT and dependencies (nvcc, gcc-11, nvidia-smi)
- Optionally configure paths in 
    - seq2seq.myph.sh
    - transformer.myph.sh

## Experiments

### Sequence-to-Sequence Model
1. **Seq2Seq run1** ([nmt_seq2seq_v1](notebooks/nmt_seq2seq_v1.ipynb) => models/model.seq2seq.myph/baseline/): default settings
2. **Seq2Seq run2** ([nmt_seq2seq_v2](notebooks/nmt_seq2seq_v2.ipynb) => models/model.seq2seq.myph/change1/): changes placeholder
3. **Seq2Seq run3** ([nmt_seq2seq_v3](notebooks/nmt_seq2seq_v3.ipynb) => models/model.seq2seq.myph/change2/): changes placeholder

### Transformer Model
1. **Transformer run1** ([nmt_transformer_v1](notebooks/nmt_transformer_v1.ipynb) => models/model.transformer.myph/baseline/): default settings
2. **Transformer run2** ([nmt_transformer_v2](notebooks/nmt_transformer_v2.ipynb) => models/model.transformer.myph/change1/): changes placeholder
3. **Transformer run3** ([nmt_transformer_v3](notebooks/nmt_transformer_v3.ipynb) => models/model.transformer.myph/change2/): changes placeholders

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
├── data/
│   ├── g2p-par/                    # originally Sayar's
│   ├── cleaned/                    # preprocessed data (version 1)
│   ├── vocab/
│   └── logs/
│
├── syl-normalizer/         # originally Sayar's # modified to merge with previous token for athat (်) cases
├── seq2seq.myph.sh         # originally Sayar's # modified paths
└── transformer.myph.sh     # originally Sayar's # modified paths

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
