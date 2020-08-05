#!/usr/bin/env python

from typing import List, Any
import json

from .extractors import LabboxEphysRecordingExtractor
import hither as hi
import kachery_p2p as kp

recording_fname: str = "known_recordings.json"

def get_valid_recordings(fname: str) -> List[Any]:
    with open(fname, 'r') as fp:
        recordings: List[Any] = json.load(fp)
        return recordings

def load_recording(rec_id: str) -> Any:
    valid_recordings: List[Any] = get_valid_recordings(recording_fname)
    for entry in valid_recordings:
        if rec_id == entry['recordingId'] or rec_id == entry['recordingLabel']:
            obj = kp.load_file(entry['recordingObject'])
            recording = LabboxEphysRecordingExtractor(obj, download=False)
            return recording
    raise Exception(f"Requested recording with identifier {rec_id} is not recognized.")


# Through hither, this function will actually be run on the remote compute resource.
# By unsetting the job cache in the config we ensure the function actually runs. This
# ensures that the file actually gets downloaded from the peer network on the rcr.
# Any container used must use the same $KACHERY_STORAGE_DIR as the surrounding environment.
@hi.function('upload_file_to_compute_resource', '0.1.0')
@hi.container('docker://magland/labbox-ephys-processing:latest')
def upload_file_to_compute_resource(file_sha1: str) -> None:
    with hi.Config(job_cache=None):
        kp.load_file(file_sha1)

