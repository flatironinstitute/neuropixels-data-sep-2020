#!/usr/bin/env python

import hither as hi
import kachery_p2p as kp
import json
import os
from pathlib import Path
import sys
from neuropixels_data_sep_2020 import prepare_cortexlab_datasets, prepare_allen_datasets, get_recordings_file_path

known_recordings_file = get_recordings_file_path()
aws_url = 'http://ephys1.laboratorybox.org'
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

lines = []

lines.append('')
lines.append(f'[View in browser (labbox-ephys)]({aws_url}/default?feed={x.get_uri()})')

lines.append('')
lines.append('| Recording ID | Web link | Description |')
lines.append('|------ | ---- | ----------- |')
for le_recording in le_recordings:
    recid = le_recording['recordingId']
    description = le_recording.get('description', '')
    le_url = f'{aws_url}/default/recording/{recid}?feed={x.get_uri()}'
    lines.append(f'| {recid} | [view]({le_url}) | {description} |')
lines.append('')

lines.append('')
lines.append('| Sorting | Web link | Description |')
lines.append('|------ | ---- | ----------- |')
for le_sorting in le_sortings:
    sortid = le_sorting['sortingId']
    description = le_sorting.get('description', '')
    le_url = f'{aws_url}/default/sorting/{sortid}?feed={x.get_uri()}'
    lines.append(f'| {sortid} | [view]({le_url}) | {description} |')
lines.append('')

txt = '\n'.join(lines)
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print(txt)
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

