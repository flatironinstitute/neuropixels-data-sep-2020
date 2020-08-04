#!/usr/bin/env python

import hither as hi
import kachery as ka
import kachery_p2p as kp
from .cortexlab_utils import cortexlab_create_recording_object
from .create_subrecording_object import create_subrecording_object

def prepare_cortexlab_datasets():
    X1 = cortexlab_create_recording_object.run(
        dirname='sha1dir://d40edb4e52ad5abef2c1689f7b04164fbf65271b.cortexlab-single-phase-3',
        bin_fname='Hopkins_20160722_g0_t0.imec.ap_CAR.bin',
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