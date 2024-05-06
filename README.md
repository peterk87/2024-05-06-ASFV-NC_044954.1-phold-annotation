# 2024-05-06 ASFV Malawi NC_044954.1 Phold annotation

## Installation and Setup

Installed [phold](https://github.com/gbouras13/phold) with PyTorch and CUDA for running on a GPU and [pharokka](https://github.com/gbouras13/pharokka) into new Conda env:

```bash
mamba create -n phold -y phold "pytorch=*=cuda*" pharokka 
```

Installed `phold` databases:

```
$ phold install
2024-05-06 12:17:24.299 | INFO     | phold:install:1097 - Downloading the Phold database into the default directory /home/pkruczkiewicz/miniconda3/envs/phold/lib/python3.10/site-packages/phold/database
2024-05-06 12:17:24.299 | INFO     | phold:install:1104 - Checking that the Rostlab/ProstT5_fp16 ProstT5 model is available in /home/pkruczkiewicz/miniconda3/envs/phold/lib/python3.10/site-packages/phold/database
2024-05-06 12:17:24.299 | INFO     | phold.features.predict_3Di:get_T5_model:121 - Using device: cpu
2024-05-06 12:17:24.299 | INFO     | phold.features.predict_3Di:get_T5_model:127 - Loading T5 from: /home/pkruczkiewicz/miniconda3/envs/phold/lib/python3.10/site-packages/phold/database/Rostlab/ProstT5_fp16
2024-05-06 12:17:24.299 | INFO     | phold.features.predict_3Di:get_T5_model:128 - If /home/pkruczkiewicz/miniconda3/envs/phold/lib/python3.10/site-packages/phold/database/Rostlab/ProstT5_fp16 is not found, it will be downloaded
/home/pkruczkiewicz/miniconda3/envs/phold/lib/python3.10/site-packages/huggingface_hub/file_download.py:1132: FutureWarning: `resume_download` is deprecated and will be removed in version 1.0.0. Downloads always resume when possible. If you want to force a new download, use `force_download=True`.
  warnings.warn(
config.json: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 733/733 [00:00<00:00, 7.41MB/s]
pytorch_model.bin: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 5.64G/5.64G [02:28<00:00, 38.1MB/s]
/home/pkruczkiewicz/miniconda3/envs/phold/lib/python3.10/site-packages/torch/_utils.py:831: UserWarning: TypedStorage is deprecated. It will be removed in the future and UntypedStorage will be the only storage class. This should only matter to you if you are using storages directly.  To access UntypedStorage directly, use tensor.untyped_storage() instead of tensor.storage()
  return self.fget.__get__(instance, owner)()
tokenizer_config.json: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2.40k/2.40k [00:00<00:00, 28.5MB/s]
spiece.model: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 238k/238k [00:00<00:00, 1.24MB/s]
added_tokens.json: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 283/283 [00:00<00:00, 2.98MB/s]
special_tokens_map.json: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2.20k/2.20k [00:00<00:00, 25.8MB/s]
You are using the default legacy behaviour of the <class 'transformers.models.t5.tokenization_t5.T5Tokenizer'>. This is expected, and simply means that the `legacy` (previous) behavior will be used so nothing changes for you. If you want to use the new behaviour, set `legacy=False`. This should only be set if you understand what it means, and thoroughly read the reason why this was added as explained in https://github.com/huggingface/transformers/pull/24565
Special tokens have been added in the vocabulary, make sure the associated word embeddings are fine-tuned or trained.
2024-05-06 12:19:56.667 | INFO     | phold.features.predict_3Di:get_T5_model:138 - Rostlab/ProstT5_fp16 loaded
2024-05-06 12:19:56.836 | INFO     | phold:install:1116 - ProstT5 model downloaded.
2024-05-06 12:19:56.836 | INFO     | phold.databases.db:install_database:80 - Checking Phold database installation in /home/pkruczkiewicz/miniconda3/envs/phold/lib/python3.10/site-packages/phold/database.
2024-05-06 12:19:56.836 | WARNING  | phold.databases.db:check_db_installation:209 - Phold Database file /home/pkruczkiewicz/miniconda3/envs/phold/lib/python3.10/site-packages/phold/database/all_phold_prostt5 is missing
2024-05-06 12:19:56.836 | INFO     | phold.databases.db:install_database:85 - Some Phold databases files are missing
2024-05-06 12:19:56.837 | INFO     | phold.databases.db:install_database:86 - Downloading the Phold database
2024-05-06 12:19:56.837 | INFO     | phold.databases.db:install_database:91 - Downloading Phold database from https://zenodo.org/records/10675285/files/phold_structure_foldseek_db.tar.gz
|████████████████████████████████████████| 1.64G/1.64G [100%] in 1:40.0 (16.44M/s)
2024-05-06 12:21:39.614 | INFO     | phold.databases.db:install_database:101 - Phold database file download OK: 353a1a6763e1261c5c44e1e2da9d8736
2024-05-06 12:21:39.615 | INFO     | phold.databases.db:install_database:107 - Extracting Phold database tarball: file=/home/pkruczkiewicz/miniconda3/envs/phold/lib/python3.10/site-packages/phold/database/phold_structure_foldseek_db.tar.gz, output=/home/pkruczkiewicz/miniconda3/envs/phold/lib/python3.10/site-packages/phold/database
```

Installed `pharokka` databases:

```
$ install_databases.py -o pharokka-db
2024-05-06 14:17:52.155 | INFO     | databases:instantiate_install:111 - Checking Pharokka database installation in pharokka-db.
2024-05-06 14:17:52.155 | INFO     | databases:check_db_installation:213 - PHROGs Databases are missing.
2024-05-06 14:17:52.155 | INFO     | databases:check_db_installation:220 - VFDB Databases are missing.
2024-05-06 14:17:52.155 | INFO     | databases:check_db_installation:227 - CARD Databases are missing.
2024-05-06 14:17:52.155 | INFO     | databases:check_db_installation:233 - PHROGs Annotation File is missing.
2024-05-06 14:17:52.155 | INFO     | databases:check_db_installation:239 - INPHARED Mash Annotation File is missing.
2024-05-06 14:17:52.155 | INFO     | databases:check_db_installation:245 - INPHARED Mash Sketch File is missing.
2024-05-06 14:17:52.155 | INFO     | databases:instantiate_install:116 - Some Databases are missing.
2024-05-06 14:17:52.155 | INFO     | databases:instantiate_install:121 - Downloading Pharokka Databases from https://zenodo.org/record/8276347/files/pharokka_v1.4.0_databases.tar.gz.
|████████████████████████████████████████| 571.7M/571.7M [100%] in 1:43.4 (5.53M/s)
2024-05-06 14:19:37.130 | INFO     | databases:instantiate_install:132 - Database file download OK: c21144209b993c06fae2dac906d73b96
2024-05-06 14:19:37.130 | INFO     | databases:instantiate_install:138 - Extracting DB tarball: file=pharokka-db/pharokka_v1.4.0_databases.tar.gz, output=pharokka-db
```

## Phold analysis

Ran `pharokka`:

```
pharokka.py -i NC_044954.1.fasta -o pharokka-NC_044954.1 -d pharokka-db/ -t 16 --fast
```

Ran `phold` with `pharokka` generated GBK file:

```bash
phold run -i pharokka-NC_044954.1/pharokka.gbk -o phold-NC_044954.1 -t 16
```

Converted `phold` GBK to GFF3 with `py-gbk-to-gff.ipynb` Jupyter Notebook.

## Phold annotation summary

```
Description	Count	Contig
CDS	246	NC_044954.1
connector	0	NC_044954.1
DNA, RNA and nucleotide metabolism	30	NC_044954.1
head and packaging	3	NC_044954.1
integration and excision	0	NC_044954.1
lysis	0	NC_044954.1
moron, auxiliary metabolic gene and host takeover	4	NC_044954.1
other	8	NC_044954.1
tail	5	NC_044954.1
transcription regulation	0	NC_044954.1
unknown function	196	NC_044954.1
VFDB_Virulence_Factors	0	NC_044954.1
CARD_AMR	1	NC_044954.1
ACR_anti_crispr	0	NC_044954.1
Defensefinder	2	NC_044954.1
```