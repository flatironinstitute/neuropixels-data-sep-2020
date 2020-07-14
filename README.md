**Note**: This repo is under construction

# neuropixels-data-sep-2020
Example neuropixels datasets for purposes of developing spike sorting algorithms

## Overview

Explain that you can interact with the below datasets in a variety of ways:

* Within the browser (labbox-ephys)
* On your own computer (must run kachery-p2p daemon)

Provide link to instructions for loading these datasets into SpikeInterface recording objects.

## CortexLab: Single Phase 3 dataset

Source data: http://data.cortexlab.net/singlePhase3/

Soudce data kachery URI: `sha1dir://d40edb4e52ad5abef2c1689f7b04164fbf65271b.cortexlab-single-phase-3`

Recording objects generated by [this script](./scripts/prepare_datasets/prepare_cortexlab_datasets.py)

| Name  | Recording object |
|------ | ---------------- |
| Full recording | sha1://8d9a0bbc2c67820866faccecf52650bd420ea8fb/cortexlab-single-phase-3.json  |
| Ch. 0-7, 10sec | sha1://4dbb81fa5ad52368077b62654d0e0624c889a24f/cortexlab-single-phase-3.ch0-7.10sec.json  |

