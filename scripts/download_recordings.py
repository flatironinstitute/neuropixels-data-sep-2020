#!/usr/bin/env python

# Thank you @alexmorley

import os
from pathlib import Path
import numpy as np
import neuropixels_data_sep_2020 as nd
import spikeextractors as se

# specify the ids of the recordings you want to download
recording_ids = [
    'cortexlab-single-phase-3-ch0-7.10sec'
]

output_dir = Path(os.environ.get('RECORDINGS_OUTPUT_DIR', 'recordings/'))
os.makedirs(output_dir, exist_ok=True)
for i, recording_id in enumerate(recording_ids):
    r_id = recording_id
    filename = f'{r_id.replace(" ", "_")}.dat'
    print(f'Creating ({i+1} of {len(recording_ids)}): {output_dir / filename}')
    recording = nd.load_recording(recording_id, download=True)
    np.savetxt(
            output_dir / f"{r_id}.channel_locations.csv",
            recording.get_channel_locations(),
            delimiter=",", fmt="%d"
    )
    np.savetxt(
            output_dir / f"{r_id}.channel_ids.csv",
            recording.get_channel_ids(),
            delimiter=",", fmt="%d"
    )
    np.savetxt(
            output_dir / f"{r_id}.num_channels.csv",
            [recording.get_num_channels()],
            delimiter=",", fmt="%d"
    )
    se.BinDatRecordingExtractor.write_recording(
        recording,
        output_dir / filename,
        dtype='int16'
    )
    print(f'########### DONE {output_dir / filename} ###########')