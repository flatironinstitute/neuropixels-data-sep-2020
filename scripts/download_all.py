import os
import sys
import json
from pathlib import Path

from slugify import slugify
import numpy as np

sys.path.append('.')
import neuropixels_data_sep_2020 as nd
import spikeextractors as se

with open('./known_recordings.json') as f:
    known_recordings = json.load(f)

recording_ids = [r['recordingId'] for r in known_recordings['recordings'] if r['recordingId'].endswith('10sec')]

output_dir = Path(os.environ.get('RECORDINGS_OUTPUT_DIR', 'recordings/'))
os.makedirs(output_dir, exist_ok=True)
for i, recording_id in enumerate(recording_ids):
    r_id = slugify(recording_id)
    filename = f'{r_id}.dat'
    print(f'Creating ({i+1} of {len(recording_ids)}): {output_dir / filename}')
    recording = nd.load_recording(recording_id)
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
