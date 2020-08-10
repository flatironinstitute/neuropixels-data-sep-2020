#!/usr/bin/env python

import hither as hi
import kachery as ka
import kachery_p2p as kp
from .cortexlab_utils import cortexlab_create_recording_object
from .create_subrecording_object import create_subrecording_object

def prepare_cortexlab_datasets():
    X1 = cortexlab_create_recording_object.run(
        bin_uri='sha1://1b8592f0240603ae1019379cb47bad6475503aaf/tmp.dat?manifest=d05ca5b6e60e0fa8f2ff6f2f2ed822ff37da49c9',
        bin_size=87170751360, # Later kachery-p2p will allow us to get this information from bin_uri
        channel_map_npy_uri='sha1://b4de65964a758201db09f1e00d70ce40bca3a87e/channel_map.npy',
        channel_positions_npy_uri='sha1://434c1bca7fd857bc5a1c9215bd890025d082fe8d/channel_positions.py',
        raw_num_channels=385,
        samplerate=30000
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
    X1 = X1.get_result()
    X2 = X2.get_result()
    X3 = X3.get_result()

    le_recordings = []
    le_recordings.append(dict(
        recordingId='cortexlab-single-phase-3',
        recordingLabel='cortexlab-single-phase-3 (full)',
        recordingPath=ka.store_object(X1, basename='cortexlab-single-phase-3.json'),
        recordingObject=X1
    ))
    le_recordings.append(dict(
        recordingId='cortexlab-single-phase-3-ch0-7.10sec',
        recordingLabel='cortexlab-single-phase-3 (ch 0-7, 10 sec)',
        recordingPath=ka.store_object(X2, basename='cortexlab-single-phase-3-ch0-7-10sec.json'),
        recordingObject=X2
    ))
    le_recordings.append(dict(
        recordingId='cortexlab-single-phase-3.10sec',
        recordingLabel='cortexlab-single-phase-3 (10 sec)',
        recordingPath=ka.store_object(X2, basename='cortexlab-single-phase-3-10sec.json'),
        recordingObject=X2
    ))
    return le_recordings