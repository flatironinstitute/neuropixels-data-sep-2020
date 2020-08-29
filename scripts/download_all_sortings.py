#!/usr/bin/env python

import os
from pathlib import Path
import numpy as np
import neuropixels_data_sep_2020 as nd
import spikeextractors as se

# specify the ids of the recordings you want to download
sorting_ids = [
    'cortexlab-single-phase-3:curated',
    'cortexlab-single-phase-3:curated_good',
    'allen_mouse419112_probeE:curated',
    'allen_mouse415148_probeE:curated'
]

for i, sorting_id in enumerate(sorting_ids):
    print(f'########### LOADING {sorting_id} ###########')
    sorting = nd.load_sorting(sorting_id)
    print(f'Num. units: len(sorting.get_unit_ids)')
