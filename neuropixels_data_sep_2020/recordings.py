#!/usr/bin/env python

import json
import os
from pathlib import Path
from typing import List, Any

from .extractors import LabboxEphysRecordingExtractor
import hither as hi
import kachery_p2p as kp

module_name = 'neuropixels-data-sep-2020'

def get_recordings_file_path(*, readonly: bool = False) -> str:
    module_name = 'neuropixels-data-sep-2020'
    p = Path(os.getcwd())

    if (not module_name in str(p)):
        raise Exception("prepare_datasets.py is being executed from an unsupported directory.")
    basepath = p
    for x in p.parents:
        if module_name in str(x):
            basepath = x

    known_recordings_file = f"{basepath}/known_recordings.json"
    file_exists = Path(known_recordings_file).exists()
    namestr = f"Known-recordings file {known_recordings_file}"
    if (not file_exists and readonly):
        raise Exception(f"{namestr} does not exist and can't be opened for reading.")
    if (file_exists and not readonly):
        raise Exception(f"""
    {namestr} already exists; aborting.
    If you intended to overwrite it, please delete it first.""")

    return known_recordings_file


def get_valid_recordings(fname: str) -> List[Any]:
    with open(fname, 'r') as fp:
        recordings: List[Any] = json.load(fp)
        return recordings

def load_recording(rec_id: str) -> Any:
    valid_recordings: List[Any] = get_valid_recordings(get_recordings_file_path(readonly=True))
    for entry in valid_recordings:
        rec_json = f"{rec_id}.json"
        if (rec_id == entry['recordingId'] or rec_id == entry['recordingLabel']
            or rec_json == entry['recordingId'] or rec_json == entry['recordingLabel']):
            uri = entry['recordingPath']
            recording = LabboxEphysRecordingExtractor(uri, download=False)
            return recording
    raise Exception(f"Requested recording with identifier '{rec_id}' is not recognized.")


# Through hither, this function will actually be run on the remote compute resource.
# By unsetting the job cache in the config we ensure the function actually runs. This
# ensures that the file actually gets downloaded from the peer network on the rcr.
# Any container used must use the same $KACHERY_STORAGE_DIR as the surrounding environment.
@hi.function('upload_file_to_compute_resource', '0.1.0')
@hi.container('docker://magland/labbox-ephys-processing:latest')
def upload_file_to_compute_resource(file_sha1: str) -> None:
    with hi.Config(job_cache=None):
        return kp.load_file(file_sha1)
