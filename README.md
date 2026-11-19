# Intent Discovery Survey — Dataset and Analysis Package

Six task-oriented dialogue benchmark datasets, together with the analysis scripts and the
per-dataset outputs behind the dataset characterization reported in the accompanying survey
*A Survey on Intent Discovery in Open-World Task-Oriented Dialogue*.

Everything needed to recompute the statistics in that section sits in this directory tree; the
scripts are run against the corpora included here and require no network access once the
dependencies are installed.

The six datasets together cover 94,200 utterances and 387 intent categories, as reported in the
survey. They are redistributed as obtained from their original releases, which remain
authoritative.

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

Within each dataset folder, the corpus sits in `data/`, or in `rawText/` and `covid_release/`
where the source distributes plain text. An `intents/` folder holds the intent list when the
source provides one separately. The `*.py` loader and the `README.md` are the ones shipped with
that distribution, and the loader header comment records where it was downloaded from. The
`eval/` folder holds the outputs produced for that dataset, described below.

## Datasets and sources

| Folder | Corpus | Obtained from | Upstream work |
|---|---|---|---|
| `Banking` | `data/` Parquet, `intents/` Parquet | Hugging Face `DeepPavlov/banking77` | Casanueva et al. (2020), PolyAI |
| `CLINC` | `data/` Parquet, `intents/` Parquet | Hugging Face `DeepPavlov/clinc150` | Larson et al. (2019) |
| `MCID` | `covid_release/` TSV | `fb.me/covid_mcid_dataset` | Meta COVID-19 intent dataset |
| `MTOP` | `data/` Parquet | Hugging Face `mteb/mtop_intent` | Li et al. (2021) |
| `SNIPS` | `data/` TSV | `OpenGPTX/illuminer` | Coucke et al. (2018) |
| `Stackoverflow` | `rawText/` TXT and word vectors | `jacoxu/StackOverflow` | Xu et al. (2015) |

Citations for each dataset paper are collected in [`DATASETS.md`](DATASETS.md), in both APA 7 and
BibTeX. Cite the original dataset papers rather than this repository.

## Per-dataset outputs

Each `Datas/<Dataset>/eval/` folder contains four files, the results that the survey reports:

| File | Contents |
|---|---|
| `<dataset>_analysis_results.json` | Sample count, class distribution, class proportions, Gini impurity, imbalance ratio. |
| `<dataset>_class_distribution.png` | Intent frequencies, sorted, as plotted in the survey. |
| `<dataset>_utterance_base.json` | Maximum, minimum and mean utterance length in characters. |
| `<dataset>_utterance_multi.json` | Length statistics plus sentence-length, part-of-speech and dependency distributions. |

`_utterance_base` requires only the standard library; `_utterance_multi` requires a syntactic
tagger (spaCy for English, LTP for Chinese) and is provided for reference rather than as a
dependency-free reproduction target.

The intermediate files are not part of the repository. Step 1 writes the per-split batches and
step 2 consolidates them into `<dataset>_merge_output.json`, the file the analysis scripts read.
Both are listed in `.gitignore`: they are large and can be rebuilt from the corpora at any time.

## Running the analysis

The pipeline has four steps. The first two build the consolidated corpus from the release; the
last two produce the statistics and the figure.

```bash
# 1. Loader: reads the release and writes batched JSON into that dataset's eval/ folder.
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

Each script processes one dataset at a time. The dataset is selected by the `data_sets` variable
(e.g. `data_sets = "Banking"`) in the `__main__` block at the bottom of the file; the same block
lists the corresponding input and output paths. Paths resolve against the repository root, so the
scripts can be run from anywhere.

Dependencies, all installed from their own distributions:

- `pandas`, `pyarrow` — Parquet corpus files
- `matplotlib` — the class-distribution figure
- `spacy` with `en_core_web_trf` — English syntactic statistics
- `LTP` with a Chinese model — Chinese syntactic statistics

## Loading the corpora

The Parquet folders follow the Hugging Face `datasets` layout and can be read without network
access:

```python
from datasets import load_dataset

ds = load_dataset("parquet", data_files="Datas/Banking/data/*.parquet")
```

`SNIPS/data/train.tsv` and the files under `MCID/covid_release/` are tab-separated, one
utterance and one label per line. `Stackoverflow/rawText/` holds titles, labels, and pre-trained
word vectors as plain text.

## Notes on the released code

The scripts are the ones used to produce the outputs in this repository. Two mechanical changes
were made before release, neither of which alters any computation:

- Paths that were absolute in the development environment are now resolved relative to the
  repository root, so the code runs from a fresh clone.
- The call at the end of `utils/merge.py` is guarded by `if __name__ == '__main__':`, so the
  module can be imported without executing a merge.

Per-split batches and the consolidated corpus file are regenerated by steps 1 and 2 rather than
stored, and their paths are listed in `.gitignore`, so running the pipeline leaves the working
tree clean. What the repository keeps is the input corpora, the scripts, and the final results.

## Scope

- **Copies, not new annotation.** No dialogues were collected by the authors of the survey, and
  nothing in this repository should be cited as a new resource.
- **Licensing follows each original release.** Consult the upstream links above. The SNIPS
  dataset card in `SNIPS/README.md` declares MIT; the remaining datasets carry the terms of
  their own release.
- **No model weights.** The Chinese LTP model and the spaCy pipelines used by the analysis
  scripts are installed from their own distributions and are not redistributed here.

## Citation

If you use these files, please cite the accompanying survey together with the original dataset
papers collected in [`DATASETS.md`](DATASETS.md).
