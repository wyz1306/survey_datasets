# Intent Discovery Survey — Dataset Package

Six task-oriented dialogue benchmark datasets, arranged so that the dataset characterization
reported in the accompanying survey *A Survey on Intent Discovery in Open-World Task-Oriented
Dialogue* can be recomputed from a single directory tree.

The six datasets together cover 94,200 utterances and 387 intent categories. They are
redistributed here as obtained; the original releases remain authoritative.

## Layout

```text
Datas/
├── Banking/          BankING77
├── CLINC/            CLINC150
├── MCID/             COVID-19 multilingual intent queries (en, es, fr, de, spanglish)
├── MTOP/             MTOP intent detection, English split
├── SNIPS/            SNIPS NLU benchmark
└── Stackoverflow/    StackOverflow short-text titles
```

Each folder keeps the layout of the distribution it was obtained from. The corpus sits in
`data/`, or in `rawText/` and `covid_release/` where the source distributes plain text. An
`intents/` folder holds the intent list when the source provides one separately. The `*.py`
loader and the `README.md` are the ones shipped with that distribution, and the loader header
comment records where it was downloaded from.

## Datasets and sources

| Folder | Corpus | Obtained from | Upstream work |
|---|---|---|---|
| `Banking` | `data/` Parquet, `intents/` Parquet | Hugging Face `DeepPavlov/banking77` | Casanueva et al. (2020), PolyAI |
| `CLINC` | `data/` Parquet, `intents/` Parquet | Hugging Face `DeepPavlov/clinc150` | Larson et al. (2019) |
| `MCID` | `covid_release/` TSV | `fb.me/covid_mcid_dataset` | Meta COVID-19 intent dataset |
| `MTOP` | `data/` Parquet | Hugging Face `mteb/mtop_intent` | Li et al. (2021) |
| `SNIPS` | `data/` TSV | `OpenGPTX/illuminer` | Coucke et al. (2018) |
| `Stackoverflow` | `rawText/` TXT and word vectors | `jacoxu/StackOverflow` | Xu et al. (2015) |

## Loading

The Parquet folders follow the Hugging Face `datasets` layout and can be read without network
access:

```python
from datasets import load_dataset

ds = load_dataset("parquet", data_files="Datas/Banking/data/*.parquet")
```

`SNIPS/data/train.tsv` and the files under `MCID/covid_release/` are tab-separated, one
utterance and one label per line. `Stackoverflow/rawText/` holds titles, labels, and
pre-trained word vectors as plain text.

## Scope

- **Copies, not new annotation.** No dialogues were collected by the authors of the survey,
  and nothing in this repository should be cited as a new resource.
- **Licensing follows each original release.** Consult the upstream links above. The SNIPS
  dataset card in `SNIPS/README.md` declares MIT; the remaining datasets carry the terms of
  their own release.
- **No model weights.** The Chinese LTP model and the spaCy pipelines used by the analysis
  scripts are installed from their own distributions and are not redistributed here.
- **Not included.** Per-dataset analysis outputs and class-distribution figures derived from
  these files are not part of this repository.

## Citation

If you use these files, please cite the accompanying survey together with the original
dataset papers listed above.
