#!/usr/bin/env python

import hither as hi
import kachery as ka
import kachery_p2p as kp

from neuropixels_data_sep_2020 import cortexlab_create_recording_object, create_subrecording_object

jc = hi.JobCache(use_tempdir=True)
# jc = None

compute_resource_uri = 'feed://82a4286f85b50866c290fe5650bbe52c507362aee420ba0185b3d9c7fa638da9?name=ccmlin008.flatironinstitute.org'

with hi.RemoteJobHandler(uri=compute_resource_uri) as jh:
    with hi.Config(job_handler=jh, container=True, job_cache=jc):
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
        hi.wait()

le_recordings = []
le_recordings.append(dict(
    recordingId='cortexlab-single-phase-3',
    recordingLabel='cortexlab-single-phase-3 (full)',
    recordingPath=ka.store_object(X1.get_result(), basename='cortexlab-single-phase-3.json'),
    recordingObject=X1.get_result()
))
le_recordings.append(dict(
    recordingId='cortexlab-single-phase-3-ch0-7.10sec',
    recordingLabel='cortexlab-single-phase-3 (ch 0-7, 10 sec)',
    recordingPath=ka.store_object(X2.get_result(), basename='cortexlab-single-phase-3-ch0-7.10sec.json'),
    recordingObject=X2.get_result()
))

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

print('')
print('| Name  | Recording object |')
print('|------ | ---------------- |')
for le_recording in le_recordings:
    print(f'| {le_recording["recordingLabel"]} | {le_recording["recordingPath"]}')
print('')

print('| Labbox-ephys feed |')
print('| ----------------- |')
print(f'| {x.get_uri()} |')
