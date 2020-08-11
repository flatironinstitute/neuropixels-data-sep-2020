#!/usr/bin/env python

import hither as hi
import kachery as ka
import kachery_p2p as kp
from .cortexlab_utils import cortexlab_create_recording_object
from .create_subrecording_object import create_subrecording_object
from .create_subrecording_object import create_subrecording_object

def prepare_allen_datasets():
    bin_uri = 'sha1://39ae3fcccd3803170dd97fc9a8799e7169214419/continuous.dat?manifest=31942d7d97ff3a46fa1dbca72d8dc048bd65d5ce'
    channel_info_uri = 'sha1://349d7f018f4f09da5c230a9d46e07c2aeffbc1e2/channel_info.csv'
    channel_positions = _load_channel_positions_from_csv(channel_info_uri)
    X1 = dict(
        recording_format='bin1',
        data=dict(
            raw=bin_uri,
            raw_num_channels=384,
            num_frames=105000000, # infer from file size and guess of samplerate
            samplerate=30000, # guess
            channel_ids=list(range(0, 384)), # for now
            # The following are placeholders... we need the actual geom file.
            channel_map=dict(zip([str(c) for c in range(0, 384)], [c for c in range(0, 384)])),
            channel_positions=channel_positions
        )
    )
    X2 = create_subrecording_object.run(
        recording_object=X1,
        channels=[0, 1, 2, 3, 4, 5, 6, 7],
        start_frame=0,
        end_frame=30000 * 10
    )
    X3 = create_subrecording_object.run(
        recording_object=X1,
        channels=None,
        start_frame=0,
        end_frame=30000 * 10
    )
    hi.wait()
    X2 = X2.get_result()
    X3 = X3.get_result()

    # labbox-ephys format for recordings
    le_recordings = []
    le_recordings.append(dict(
        recordingId='allen_mouse419112_probeE',
        recordingLabel='allen_mouse419112_probeE (full)',
        recordingPath=ka.store_object(X1, basename='allen_mouse419112_probeE.json'),
        recordingObject=X1
    ))
    le_recordings.append(dict(
        recordingId='allen_mouse419112_probeE-ch0-7.10sec',
        recordingLabel='allen_mouse419112_probeE (ch 0-7, 10 sec)',
        recordingPath=ka.store_object(X2, basename='allen_mouse419112_probeE-ch0-7-10sec.json'),
        recordingObject=X2
    ))
    le_recordings.append(dict(
        recordingId='allen_mouse419112_probeE-10sec',
        recordingLabel='allen_mouse419112_probeE (10 sec)',
        recordingPath=ka.store_object(X3, basename='allen_mouse419112_probeE-10sec.json'),
        recordingObject=X3
    ))

    return le_recordings

def _load_channel_positions_from_csv(uri):
    csvtxt = kp.load_text(uri)
    lines = csvtxt.split('\n')
    lines = lines[1:] # skip header
    lines = [line for line in lines if line] # skip empty lines
    channel_positions = {}
    for line in lines:
        vals = line.split(',')
        ii = int(vals[0])
        x = float(vals[1])
        y = float(vals[2])
        channel_positions[str(ii)] = [x, y]
    return channel_positions

if __name__ == '__main__':
    main()


# - curated_unit_times.npy: sha1://57029ae68643881f5d4015397be87ba0d4815b52/curated_unit_times.npy
#     - curated_unit_IDs.npy: sha1://61762d8f0bdac57db64ceec1636e0009af0f02ef/curated_unit_IDs.npy?manifest=371f609a04189947e45ea8f29e60b0fd2edb1a69
#     - curated_unit_channels.npy: sha1://8b3a98b9d45c1c62eb4402245800e278873bd8e5/curated_unit_channels.npy
#     - continuous.dat: 