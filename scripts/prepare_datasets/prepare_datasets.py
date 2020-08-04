#!/usr/bin/env python

import hither as hi
import kachery_p2p as kp
import os
import sys
from neuropixels_data_sep_2020 import prepare_cortexlab_datasets, prepare_sieglelab_datasets

# jc = hi.JobCache(use_tempdir=True)
jc = None

compute_resource_uri = 'feed://82a4286f85b50866c290fe5650bbe52c507362aee420ba0185b3d9c7fa638da9?name=ccmlin008.flatironinstitute.org'

with hi.RemoteJobHandler(uri=compute_resource_uri) as jh:
    with hi.Config(job_handler=jh, container=True, job_cache=jc):
        le_recordings1 = prepare_cortexlab_datasets()
        le_recordings2 = prepare_sieglelab_datasets()

le_recordings = le_recordings1 + le_recordings2

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
    x = f.create_snapshot([dict(documentId='default', key='recordings')])
    print(x.get_uri())
finally:
    f.delete()

aws_url = 'http://a9b927286911d4338ab905d0eabba09d-949726054.us-east-2.elb.amazonaws.com:8081/default'

print('')
print(f'[View in browser (labbox-ephys)]({aws_url}?{x.get_uri()})')

print('')
print('| Name  | Recording object |')
print('|------ | ---------------- |')
for le_recording in le_recordings:
    print(f'| {le_recording["recordingLabel"]} | {le_recording["recordingPath"]}')
print('')


