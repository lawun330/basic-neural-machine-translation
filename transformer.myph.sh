#!/bin/bash

## Written by Ye Kyaw Thu, Affiliated Professor, CADT, Cambodia
## for NMT Experiments between Burmese and Ethnic Languages
## used Marian NMT Framework for transformer training
## Last updated: 23 May 2022

model_folder="../models/model.transformer.myph"; # -- MODIFIED --
mkdir ${model_folder};
data_path="../data/cleaned"; # -- MODIFIED --
vocab_path="../data/vocab"; # -- MODIFIED --
src="my"; tgt="ph"; # -- MODIFIED --

marian \
  --type transformer \
  --train-sets ${data_path}/train.${src} ${data_path}/train.${tgt} \
  --max-length 200 \
  --valid-sets ${data_path}/dev.${src} ${data_path}/dev.${tgt} \
  --vocabs ${vocab_path}/vocab.${src}.yml ${vocab_path}/vocab.${tgt}.yml \
  --maxi-batch 100 \
  --valid-translation-output ${model_folder}/valid.output --quiet-translation \
  --beam-size 6 --normalize 0.6 \
  --transformer-heads 8 \
  --transformer-postprocess-emb d \
  --transformer-postprocess dan \
  --transformer-dropout 0.3 --label-smoothing 0.1 \
  --learn-rate 0.0003 --lr-warmup 0 --lr-decay-inv-sqrt 16000 --lr-report \
  --clip-norm 5 \
  --exponential-smoothing \
  --model ${model_folder}/model.npz \
  --enc-depth 2 \
  --dec-depth 2 \
  --tied-embeddings \
  --mini-batch-fit -w 1000 \
  --valid-mini-batch 64 \
  --valid-metrics cross-entropy perplexity bleu\
  --valid-freq 5000 --save-freq 5000 --disp-freq 500 \
  --early-stopping 10 \
  --log ${model_folder}/train.log --valid-log ${model_folder}/valid.log \
  --devices 0 --sync-sgd --seed 1111 \
  --dump-config > ${model_folder}/config.yml \

time marian -c ${model_folder}/config.yml 2>&1 | tee ${model_folder}/transformer.${src}-${tgt}.log
