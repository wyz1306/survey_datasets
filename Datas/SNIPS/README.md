---
license: mit
dataset_info:
  features:
  - name: audio
    dtype: audio
  - name: ID
    dtype: int64
  - name: text
    dtype: string
  - name: worker
    dtype: string
  - name: distance
    dtype: string
  - name: source
    dtype: string
  splits:
  - name: train
    num_bytes: 557016057.31
    num_examples: 5886
  download_size: 574672982
  dataset_size: 557016057.31
language:
- en
task_categories:
- automatic-speech-recognition
size_categories:
- 1K<n<10K
---
# Dataset Card for SNIPS SLU v1.0

### Dataset Summary

This dataset contains SNIPS SLU Speech Recognition Dataset, available [here](https://github.com/sonos/spoken-language-understanding-research-datasets).

It contains recordings of commands for smart home appliances in English, with info about demographics of the speaker.
