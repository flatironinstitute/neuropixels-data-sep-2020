import os
import sys
import json
from pathlib import Path

from slugify import slugify

sys.path.append('.')
import neuropixels_data_sep_2020 as nd
import spikeextractors as se

with open('./known_recordings.json') as f:
    known_recordings = json.load(f)

recording_ids = [r['recordingId'] for r in known_recordings['recordings']]

output_dir = Path(os.environ.get('RECORDINGS_OUTPUT_DIR', 'recordings/'))
os.makedirs(output_dir, exist_ok=True)
for i, recording_id in enumerate(recording_ids):
    filename = f'{slugify(recording_id)}.dat'
    print(f'Creating ({i+1} of {len(recording_ids)}): {output_dir / filename}')
    recording = nd.load_recording(recording_id)
    se.BinDatRecordingExtractor.write_recording(recording, output_dir / filename)
    print(f'########### DONE {output_dir / filename} ###########')
