# Citing the datasets

The six corpora in this repository are redistributed copies of published benchmarks. Work that
uses them should cite the original dataset paper, not this repository. The entries below are the
ones used in the accompanying survey, in APA 7 style, with BibTeX at the end.

| Folder | Dataset | Citation | DOI or URL |
|---|---|---|---|
| `Datas/Banking` | BankING77 | Casanueva et al. (2020) | [10.18653/v1/2020.nlp4convai-1.5](https://doi.org/10.18653/v1/2020.nlp4convai-1.5) |
| `Datas/CLINC` | CLINC150 | Larson et al. (2019) | [10.18653/v1/D19-1131](https://doi.org/10.18653/v1/D19-1131) |
| `Datas/MCID` | MCID | Arora et al. (2020) | [OpenReview](https://openreview.net/forum?id=vP-CQG-ap-R) |
| `Datas/MTOP` | MTOP | Li et al. (2021) | [10.18653/v1/2021.eacl-main.257](https://doi.org/10.18653/v1/2021.eacl-main.257) |
| `Datas/SNIPS` | SNIPS | Coucke et al. (2018) | [10.48550/arXiv.1805.10190](https://doi.org/10.48550/arXiv.1805.10190) |
| `Datas/Stackoverflow` | StackOverflow | Xu et al. (2015) | [10.3115/v1/w15-1509](https://doi.org/10.3115/v1/w15-1509) |

## Full references

Arora, A., Shrivastava, A., Mohit, M., Lecanda, L. S. M., & Aly, A. (2020). *Cross-lingual
transfer learning for intent detection of COVID-19 utterances* [Preprint]. OpenReview.
https://openreview.net/forum?id=vP-CQG-ap-R

Casanueva, I., Temčinas, T., Gerz, D., Henderson, M., & Vulić, I. (2020). Efficient intent
detection with dual sentence encoders. In *Proceedings of the 2nd Workshop on Natural Language
Processing for Conversational AI* (pp. 38–45). Association for Computational Linguistics.
https://doi.org/10.18653/v1/2020.nlp4convai-1.5

Coucke, A., Saade, A., Ball, A., Bluche, T., Caulier, A., Leroy, D., Doumouro, C., Gisselbrecht,
T., Caltagirone, F., Lavril, T., Primet, M., & Dureau, J. (2018). *Snips voice platform: An
embedded spoken language understanding system for private-by-design voice interfaces*
(arXiv:1805.10190). arXiv. https://doi.org/10.48550/arXiv.1805.10190

Larson, S., Mahendran, A., Peper, J. J., Clarke, C., Lee, A., Hill, P., Kummerfeld, J. K., Leach,
K., Laurenzano, M. A., Tang, L., & Mars, J. (2019). An evaluation dataset for intent
classification and out-of-scope prediction. In *Proceedings of the 2019 Conference on Empirical
Methods in Natural Language Processing and the 9th International Joint Conference on Natural
Language Processing* (pp. 1311–1316). Association for Computational Linguistics.
https://doi.org/10.18653/v1/D19-1131

Li, H., Arora, A., Chen, S., Gupta, A., Gupta, S., & Mehdad, Y. (2021). MTOP: A comprehensive
multilingual task-oriented semantic parsing benchmark. In *Proceedings of the 16th Conference of
the European Chapter of the Association for Computational Linguistics: Main Volume*
(pp. 2950–2962). Association for Computational Linguistics.
https://doi.org/10.18653/v1/2021.eacl-main.257

Xu, J., Wang, P., Tian, G., Xu, B., Zhao, J., Wang, F., & Hao, H. (2015). Short text clustering
via convolutional neural networks. In *Proceedings of the 1st Workshop on Vector Space Modeling
for Natural Language Processing* (pp. 62–69). Association for Computational Linguistics.
https://doi.org/10.3115/v1/w15-1509

## BibTeX

```bibtex
@inproceedings{Casanueva2020Banking,
  author    = {Casanueva, I. and Tem{\v{c}}inas, T. and Gerz, D. and Henderson, M. and Vuli{\'c}, I.},
  title     = {Efficient intent detection with dual sentence encoders},
  booktitle = {Proceedings of the 2nd Workshop on Natural Language Processing for Conversational {AI}},
  year      = {2020},
  doi       = {10.18653/v1/2020.nlp4convai-1.5},
  pages     = {38--45}
}

@inproceedings{Larson2019CLINC,
  author    = {Larson, S. and Mahendran, A. and Peper, J. J. and Clarke, C. and Lee, A. and Hill, P.
               and Kummerfeld, J. K. and Leach, K. and Laurenzano, M. A. and Tang, L. and Mars, J.},
  title     = {An evaluation dataset for intent classification and out-of-scope prediction},
  booktitle = {Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing
               and the 9th International Joint Conference on Natural Language Processing},
  year      = {2019},
  doi       = {10.18653/v1/D19-1131},
  pages     = {1311--1316}
}

@misc{Arora2020MCID,
  author       = {Arora, A. and Shrivastava, A. and Mohit, M. and Lecanda, L. S. M. and Aly, A.},
  title        = {Cross-lingual transfer learning for intent detection of {COVID-19} utterances},
  howpublished = {OpenReview preprint},
  year         = {2020},
  url          = {https://openreview.net/forum?id=vP-CQG-ap-R}
}

@inproceedings{Li2021MTOP,
  author    = {Li, H. and Arora, A. and Chen, S. and Gupta, A. and Gupta, S. and Mehdad, Y.},
  title     = {{MTOP}: A comprehensive multilingual task-oriented semantic parsing benchmark},
  booktitle = {Proceedings of the 16th Conference of the European Chapter of the Association
               for Computational Linguistics: Main Volume},
  year      = {2021},
  doi       = {10.18653/v1/2021.eacl-main.257},
  pages     = {2950--2962}
}

@misc{Coucke2018Snips,
  author       = {Coucke, A. and Saade, A. and Ball, A. and Bluche, T. and Caulier, A. and Leroy, D.
                  and Doumouro, C. and Gisselbrecht, T. and Caltagirone, F. and Lavril, T.
                  and Primet, M. and Dureau, J.},
  title        = {Snips voice platform: An embedded spoken language understanding system for
                  private-by-design voice interfaces},
  howpublished = {arXiv preprint arXiv:1805.10190},
  year         = {2018},
  doi          = {10.48550/arXiv.1805.10190}
}

@inproceedings{Xu2015StackOverflow,
  author    = {Xu, J. and Wang, P. and Tian, G. and Xu, B. and Zhao, J. and Wang, F. and Hao, H.},
  title     = {Short text clustering via convolutional neural networks},
  booktitle = {Proceedings of the 1st Workshop on Vector Space Modeling for Natural Language Processing},
  year      = {2015},
  doi       = {10.3115/v1/w15-1509},
  pages     = {62--69}
}
```
