#!/usr/bin/env python

import json
import os
from pathlib import Path
from typing import List, Any
import kachery_p2p as kp

from .extractors import LabboxEphysRecordingExtractor, LabboxEphysSortingExtractor
from .known_recordings_uri import KNOWN_RECORDINGS_URI

module_name = 'neuropixels-data-sep-2020'

def load_known_recordings_dict():
    try:
        x = kp.load_object(KNOWN_RECORDINGS_URI)
    except:
        raise Exception('Problem loading recordings dict. Perhaps you are not running the kachery-p2p daemon?')
    return x

def get_valid_recordings() -> List[Any]:
    x = load_known_recordings_dict()
    return x['recordings']

def get_valid_sortings() -> List[Any]:
    x = load_known_recordings_dict()
    return x['sortings']

def load_recording(rec_id: str, download=False) -> Any:
    valid_recordings: List[Any] = get_valid_recordings()
    for entry in valid_recordings:
        rec_json = f"{rec_id}.json"
        if (rec_id == entry['recordingId'] or rec_id == entry['recordingLabel']
            or rec_json == entry['recordingId'] or rec_json == entry['recordingLabel']):
            uri = entry['recordingPath']
            recording = LabboxEphysRecordingExtractor(uri, download=download)
            return recording
    raise Exception(f"Requested recording with identifier '{rec_id}' is not recognized.")

def load_sorting(sorting_id: str) -> Any:
    valid_sortings: List[Any] = get_valid_sortings()
    for entry in valid_sortings:
        sorting_json = f"{sorting_id}.json"
        if (sorting_id == entry['sortingId'] or sorting_id == entry['sortingLabel']
            or sorting_json == entry['sortingId'] or sorting_json == entry['sortingLabel']):
            uri = entry['sortingPath']
            sorting = LabboxEphysSortingExtractor(uri)
            return sorting
    raise Exception(f"Requested sorting with identifier '{sorting_id}' is not recognized.")
