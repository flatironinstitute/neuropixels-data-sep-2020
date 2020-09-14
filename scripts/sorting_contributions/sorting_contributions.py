#!/usr/bin/env python

import neuropixels_data_sep_2020 as nd
import kachery as ka
import kachery_p2p as kp
import hither as hi
from neuropixels_data_sep_2020.uploader import upload_files_to_compute_resource

aws_url = 'http://ephys1.laboratorybox.org'
compute_resource_uri = 'feed://09b27ce6c71add9fe6effaf351fce98d867d6fa002333a8b06565b0a108fb0ba?name=ephys1'

#jc = hi.JobCache(use_tempdir=True)
jc = None

spyking_circus_sortings = {
    'cortexlab-single-phase-3': 'sha1://2e748216d16d97a8a7ad54ba05f34df1d5fc724c/file.json',
    'allen_mouse419112_probeE': 'sha1://b8ddf7527849d1734e533bb0b11787e6a1ac6eae/file.json',
    'allen_mouse415148_probeE': 'sha1://be9d013191dc7a5c539c61b87da6672281d00da8/file.json',
    'cortexlab-drift-dataset1': 'sha1://d618a4dfed3e8e74d980af60289a31186d962cb6/file.json',
    'cortexlab-drift-dataset2': 'sha1://9c8e813fbab74c3c463295c13aa1c6e28a74a157/file.json',
    'svoboda-SC026_080619_g0_tcat': 'sha1://1e435f56012eb3f1b2996d04a4d40edd4d0d2968/file.json',
    'svoboda-SC022_030319_g0_tcat_imec2': 'sha1://d5eb47fad3e6d4fd73c9dbea1f3e5a431ab73d2d/file.json'
}

le_recordings = []
le_sortings = []
le_curation_actions = []
for recording_id, sorting_path in spyking_circus_sortings.items():
    recording = nd.load_recording(recording_id)
    print(sorting_path)
    sorting = nd.LabboxEphysSortingExtractor(sorting_path)
    le_recordings.append(dict(
        recordingId=recording_id,
        recordingLabel=recording_id,
        recordingPath=ka.store_object(recording.object()),
        recordingObject=recording.object(),
        description=''
    ))
    le_sortings.append(dict(
        sortingId=recording_id + ':spyking_circus',
        sortingLabel=recording_id + ':spyking_circus',
        sortingPath=sorting_path,
        sortingObject=sorting.object(),

        recordingId=recording_id,
        recordingPath=ka.store_object(recording.object()),
        recordingObject=recording.object(),

        description=f'''
        SpykingCircus applied to {recording_id}
        '''.strip()
    ))

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