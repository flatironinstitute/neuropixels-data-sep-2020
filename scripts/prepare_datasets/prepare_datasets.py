#!/usr/bin/env python

import hither as hi
import kachery_p2p as kp
import json
import datetime
import os
from pathlib import Path
import sys
from neuropixels_data_sep_2020 import prepare_cortexlab_datasets, prepare_allen_datasets

aws_url = 'http://ephys1.laboratorybox.org'
compute_resource_uri = 'feed://96b4879d17c55fdd414b1f03e52d9c54c16467488ff42adabedb3c9386ee5397?name=ccmlin008-ephys1-3'

jc = hi.JobCache(use_tempdir=True)
#jc = None


with hi.RemoteJobHandler(uri=compute_resource_uri) as jh:
    with hi.Config(job_handler=jh, container=True, job_cache=jc):
        le_recordings1, le_sortings1 = prepare_cortexlab_datasets()
        le_recordings2, le_sortings2 = prepare_allen_datasets()

le_recordings = le_recordings1 + le_recordings2
le_sortings = le_sortings1 + le_sortings2

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

known_recordings_dict = dict(
    recordings=le_recordings,
    sortings=le_sortings
)
known_recordings_uri = kp.store_object(known_recordings_dict, basename='known_recordings.json')

lines = []

lines.append('| Recording ID | Web link | Description |')
lines.append('|------ | ---- | ----------- |')
for le_recording in le_recordings:
    recid = le_recording['recordingId']
    description = le_recording.get('description', '')
    le_url = f'{aws_url}/default/recording/{recid}?feed={x.get_uri()}'
    lines.append(f'| {recid} | [view]({le_url}) | {description} |')
lines.append('')

lines.append('')
lines.append('| Sorting ID | Web link | Description |')
lines.append('|------ | ---- | ----------- |')
for le_sorting in le_sortings:
    sortid = le_sorting['sortingId']
    description = le_sorting.get('description', '')
    le_url = f'{aws_url}/default/sorting/{sortid}?feed={x.get_uri()}'
    lines.append(f'| {sortid} | [view]({le_url}) | {description} |')
lines.append('')

lines.append('')
lines.append(f'[Browse all recordings]({aws_url}/default?feed={x.get_uri()})')

txt = '\n'.join(lines)
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print(txt)
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

try:
    with open('README.md') as f:
        readme_txt = f.read()
    ind1 = readme_txt.find('<!-- BEGIN DATA TABLE -->')
    ind2 = readme_txt.find('<!-- END DATA TABLE -->')
    assert (ind1 >=0) and (ind2 >= 0)
    readme_txt = ''.join([
        readme_txt[:ind1],
        '<!-- BEGIN DATA TABLE -->\n',
        f'\n<!--- Auto-generated at {datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}-->\n',
        '\n'.join(lines),
        '\n',
        readme_txt[ind2:]
    ])
    with open('README.md', 'w') as f:
        f.write(readme_txt)
except:
    raise Exception('Unable to auto-update README.md. Run this script from the base directory of the repo.')

known_recordings_uri_py_fname = 'neuropixels_data_sep_2020/known_recordings_uri.py'
if not os.path.exists(known_recordings_uri_py_fname):
    raise Exception('Unable to auto-update known_recordings_uri.py. Run this script from the base directory of the repo.')
with open(known_recordings_uri_py_fname, 'w') as f:
    f.write(f'KNOWN_RECORDINGS_URI = {known_recordings_uri}')


