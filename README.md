# Intent Discovery Survey — Dataset and Analysis Package

Six task-oriented dialogue benchmark datasets (94,200 utterances, 387 intent categories),
together with the analysis scripts and per-dataset outputs behind the dataset characterization in
the accompanying survey *A Survey on Intent Discovery in Open-World Task-Oriented Dialogue*. The
corpora are redistributed as obtained from their original releases, which remain authoritative;
the scripts run against them offline once the dependencies are installed.

## Layout

```text
Datas/
├── Banking/          BankING77
├── CLINC/            CLINC150
├── MCID/             COVID-19 multilingual intent queries (en, es, fr, de, spanglish)
├── MTOP/             MTOP intent detection, English split
├── SNIPS/            SNIPS NLU benchmark
└── Stackoverflow/    StackOverflow short-text titles
Analysis/
├── Intents_distribution.py   class distribution, Gini impurity, imbalance ratio, figure
├── utterance.py              utterance length statistics
├── utterance_en.py           length plus syntactic statistics, English (spaCy)
└── utterance_cn.py           length plus syntactic statistics, Chinese (LTP)
utils/
└── merge.py                  merges batched loader output into one corpus file
```

Inside a dataset folder the corpus sits in `data/`, or in `rawText/` and `covid_release/` where the
source distributes plain text; `intents/` holds the intent list when it is distributed separately.
The `*.py` loader and the `README.md` are those shipped with that distribution, and the loader
header records the download address. `eval/` holds the outputs described below.

## Datasets and sources

| Folder | Corpus | Obtained from | Upstream work |
|---|---|---|---|
| `Banking` | `data/` Parquet, `intents/` Parquet | Hugging Face `DeepPavlov/banking77` | Casanueva et al. (2020), PolyAI |
| `CLINC` | `data/` Parquet, `intents/` Parquet | Hugging Face `DeepPavlov/clinc150` | Larson et al. (2019) |
| `MCID` | `covid_release/` TSV | `fb.me/covid_mcid_dataset` | Meta COVID-19 intent dataset |
| `MTOP` | `data/` Parquet | Hugging Face `mteb/mtop_intent` | Li et al. (2021) |
| `SNIPS` | `data/` TSV | `OpenGPTX/illuminer` | Coucke et al. (2018) |
| `Stackoverflow` | `rawText/` TXT and word vectors | `jacoxu/StackOverflow` | Xu et al. (2015) |

Citations for the dataset papers are collected in [`DATASETS.md`](DATASETS.md), in APA 7 and
BibTeX. Cite the original dataset papers rather than this repository.

The Parquet folders follow the Hugging Face `datasets` layout:

```python
from datasets import load_dataset

ds = load_dataset("parquet", data_files="Datas/Banking/data/*.parquet")
```

`SNIPS/data/train.tsv` and the files under `MCID/covid_release/` are tab-separated, one utterance
and one label per line; `Stackoverflow/rawText/` holds titles, labels and word vectors as text.

## Per-dataset outputs

Each `Datas/<Dataset>/eval/` folder holds the four results the survey reports:

| File | Contents |
|---|---|
| `<dataset>_analysis_results.json` | Sample count, class distribution, class proportions, Gini impurity, imbalance ratio. |
| `<dataset>_class_distribution.png` | Intent frequencies, sorted, as plotted in the survey. |
| `<dataset>_utterance_base.json` | Maximum, minimum and mean utterance length in characters. |
| `<dataset>_utterance_multi.json` | Length statistics plus sentence-length, part-of-speech and dependency distributions. |

The intermediate files are not stored: step 1 writes the per-split batches and step 2 consolidates
them into `<dataset>_merge_output.json`, the file the analysis scripts read. Both are listed in
`.gitignore` and can be rebuilt from the corpora at any time, so running the pipeline leaves the
working tree clean.

`_utterance_base` needs only the standard library; `_utterance_multi` needs a syntactic tagger
(spaCy for English, LTP for Chinese) and is provided for reference rather than as a
dependency-free reproduction target.

## Running the analysis

Steps 1–2 rebuild the consolidated corpus from the release; steps 3–4 produce the statistics and
the figure.

```bash
# 1. Loader: writes batched JSON into that dataset's eval/ folder.
#    Run it from inside the dataset folder, e.g. Datas/Banking/banking.py

# 2. Merge the batches into a single corpus file.
python utils/merge.py

# 3. Class distribution, Gini impurity, imbalance ratio and figure.
python Analysis/Intents_distribution.py

# 4. Utterance length, and optionally syntactic statistics.
python Analysis/utterance.py        # standard library only
python Analysis/utterance_en.py     # English: requires spacy and en_core_web_trf
python Analysis/utterance_cn.py     # Chinese: requires LTP
```

Each script handles one dataset at a time, selected by the `data_sets` variable (e.g.
`data_sets = "Banking"`) in the `__main__` block at the bottom of the file, which also lists the
input and output paths. Paths resolve against the repository root, so the scripts run from
anywhere. The dependencies, all installed from their own distributions, are `pandas` and `pyarrow`
for the Parquet files, `matplotlib` for the figure, `spacy` with `en_core_web_trf` for English
syntax, and `LTP` with a Chinese model for Chinese syntax.

## Notes on the released code

The scripts are those used to produce the outputs here, with two mechanical changes that alter no
computation: absolute development paths are resolved relative to the repository root, and the call
at the end of `utils/merge.py` is guarded by `if __name__ == '__main__':` so the module can be
imported without executing a merge.

## Scope

- **Copies, not new annotation.** No dialogues were collected here, and nothing in this repository
  should be cited as a new resource.
- **Licensing follows each original release.** Consult the upstream links above; `SNIPS/README.md`
  declares MIT, while the other datasets carry the terms of their own release.
- **No model weights.** The LTP model and the spaCy pipelines are installed from their own
  distributions and are not redistributed here.

## Citation

If you use these files, cite the accompanying survey together with the dataset papers collected in
[`DATASETS.md`](DATASETS.md).
