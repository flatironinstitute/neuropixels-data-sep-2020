#!/usr/bin/env python

import hither as hi
import kachery_p2p as kp
import json
import os
from pathlib import Path
import sys
from neuropixels_data_sep_2020 import prepare_cortexlab_datasets, prepare_allen_datasets, get_recordings_file_path

known_recordings_file = get_recordings_file_path()
aws_url = 'http://a9b927286911d4338ab905d0eabba09d-949726054.us-east-2.elb.amazonaws.com:8081/default'
compute_resource_uri = 'feed://82a4286f85b50866c290fe5650bbe52c507362aee420ba0185b3d9c7fa638da9?name=ccmlin008.flatironinstitute.org'

jc = hi.JobCache(use_tempdir=True)
#jc = None


with hi.RemoteJobHandler(uri=compute_resource_uri) as jh:
    with hi.Config(job_handler=jh, container=True, job_cache=jc):
        le_recordings1, le_sortings1 = prepare_cortexlab_datasets()
        le_recordings2 = prepare_allen_datasets()

le_recordings = le_recordings1 + le_recordings2
le_sortings = le_sortings1

try:
    f = kp.create_feed()
    recordings = f.get_subfeed(dict(documentId='default', key='recordings'))
    for le_recording in le_recordings:
        recordings.append_message(dict(
            action=dict(
                type='ADD_RECORDING',
                recording=le_recording
            )
        ))
    for le_sorting in le_sortings:
        recordings.append_message(dict(
            action=dict(
                type='ADD_SORTING',
                sorting=le_sorting
            )
        ))
    x = f.create_snapshot([dict(documentId='default', key='recordings')])
    print(x.get_uri())
finally:
    f.delete()

with open(known_recordings_file, 'w') as fp:
    json.dump(dict(
        recordings=le_recordings,
        sortings=le_sortings
    ), fp)

print('')
print(f'[View in browser (labbox-ephys)]({aws_url}?feed={x.get_uri()})')

print('')
print('| Recording  | Description |')
print('|------ | ----------- |')
for le_recording in le_recordings:
    print(f'| {le_recording["recordingLabel"]} | Placeholder for {le_recording["recordingId"]} |')
print('')

print('')
print('| Sorting  | Description |')
print('|------ | ----------- |')
for le_sorting in le_sortings:
    print(f'| {le_sorting["sortingLabel"]} | Placeholder for {le_sorting["sortingId"]} |')
print('')

