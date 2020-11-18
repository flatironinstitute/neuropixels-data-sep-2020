#!/usr/bin/env python

import hither as hi
import kachery_p2p as kp
import json
import datetime
import os
from pathlib import Path
import sys
from neuropixels_data_sep_2020 import prepare_cortexlab_datasets, prepare_cortexlab_drift_datasets, prepare_allen_datasets, prepare_svoboda_datasets, prepare_contributed_sortings
from neuropixels_data_sep_2020.uploader import upload_files_to_compute_resource
import labbox_ephys as le

aws_url = 'http://ephys1.laboratorybox.org'
compute_resource_uri = 'feed://1afa93d013bb6a5f68e87186c6bd43e11cefb9da2fddc8837c30a47c1a7bf72f?name=ephys1'

#jc = hi.JobCache(use_tempdir=True)
jc = None


with hi.RemoteJobHandler(compute_resource_uri=compute_resource_uri) as jh:
    with hi.Config(job_handler=jh, container=True, job_cache=jc):
        le_recordings1, le_sortings1 = prepare_cortexlab_datasets()
        le_recordings2 = prepare_cortexlab_drift_datasets()
        le_recordings3, le_sortings3 = prepare_allen_datasets()
        le_recordings4, le_sortings4, le_curation_actions4 = prepare_svoboda_datasets()
        hi.wait()

        le_recordings = le_recordings1 + le_recordings2 + le_recordings3 + le_recordings4
        le_sortings = le_sortings1 + le_sortings3 + le_sortings4
        le_curation_actions = le_curation_actions4

        le_recordings_by_id = {}
        for r in le_recordings:
            le_recordings_by_id[r['recordingId']] = r
        contributed_sortings = prepare_contributed_sortings(le_recordings_by_id)
        le_sortings = le_sortings + contributed_sortings

try:
    f = kp.create_feed()
    recordings = f.get_subfeed(dict(documentId='default', key='recordings'))
    sortings = f.get_subfeed(dict(documentId='default', key='sortings'))
    for le_recording in le_recordings:
        recordings.append_message(dict(
            action=dict(
                type='ADD_RECORDING',
                recording=le_recording
            )
        ))
    for le_sorting in le_sortings:
        sortings.append_message(dict(
            action=dict(
                type='ADD_SORTING',
                sorting=le_sorting
            )
        ))
    for action in le_curation_actions:
        sortings.append_message(dict(
            action=action
        ))
    x = f.create_snapshot([
        dict(documentId='default', key='recordings'),
        dict(documentId='default', key='sortings')
    ])
    print(x.get_uri())
finally:
    f.delete()

known_recordings_dict = dict(
    recordings=le_recordings,
    sortings=le_sortings
)
known_recordings_uri = kp.store_object(known_recordings_dict, basename='known_recordings.json')

print('Uploading files to compute resource')
with hi.RemoteJobHandler(compute_resource_uri=compute_resource_uri) as jh:
    with hi.Config(job_handler=jh, container=True):
        upload_files_to_compute_resource([
            known_recordings_uri,
            x.get_uri(),
            [
                dict(
                    sortingId=x['sortingId'],
                    sortingPath=x['sortingPath'],
                    sortingObject=x['sortingObject']
                )
                for x in le_sortings
            ]
        ])
        hi.wait()

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
    f.write(f'KNOWN_RECORDINGS_URI = "{known_recordings_uri}" # auto-generated by prepare_datasets.py')

######################################################################################################
print('Preparing snippets h5 files')
with hi.RemoteJobHandler(compute_resource_uri=compute_resource_uri) as jh:
    with hi.Config(job_handler=jh, container=True):
        for s in le_sortings:
            print(f'Preparing snippets h5 for {s["sortingId"]}')
            recording_object = s['recordingObject']
            sorting_object = s['sortingObject']
            with hi.Config(required_files=sorting_object):
                le.prepare_snippets_h5.run(
                    recording_object=recording_object,
                    sorting_object=sorting_object
                )
        hi.wait()


