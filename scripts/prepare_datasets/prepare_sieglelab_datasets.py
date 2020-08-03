#!/usr/bin/env python

import hither as hi
import kachery as ka
import kachery_p2p as kp

from neuropixels_data_sep_2020 import create_subrecording_object

# jc = hi.JobCache(use_tempdir=True)
jc = None

compute_resource_uri = 'feed://82a4286f85b50866c290fe5650bbe52c507362aee420ba0185b3d9c7fa638da9?name=ccmlin008.flatironinstitute.org'

bin_uri = 'sha1://39ae3fcccd3803170dd97fc9a8799e7169214419/continuous.dat?manifest=31942d7d97ff3a46fa1dbca72d8dc048bd65d5ce'
X1 = dict(
    recording_format='bin1',
    data=dict(
        raw=bin_uri,
        raw_num_channels=384,
        num_frames=105000000, # infer from file size and guess of samplerate
        samplerate=30000, # guess
        channel_ids=list(range(1, 385)), # for now
        # The following are placeholders... we need the actual geom file.
        channel_map=dict(zip([str(c+1) for c in range(0, 384)], [c for c in range(0, 384)])),
        channel_positions=dict(zip([str(c+1) for c in range(0, 384)], [[c, 0] for c in range(0, 384)]))
    )
)

# labbox-ephys format for recordings
le_recordings = []
le_recordings.append(dict(
    recordingId='sieglelab_mouse419112_probeE',
    recordingLabel='sieglelab_mouse419112_probeE',
    recordingPath=ka.store_object(X1, basename='sieglelab_mouse419112_probeE.json'),
    recordingObject=X1
))

try:
    f = kp.create_feed() # temporary feed
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
print(f'| [{x.get_uri()}](http://a9b927286911d4338ab905d0eabba09d-949726054.us-east-2.elb.amazonaws.com:8081/default/?feed={x.get_uri()}) |')


# - curated_unit_times.npy: sha1://57029ae68643881f5d4015397be87ba0d4815b52/curated_unit_times.npy
#     - curated_unit_IDs.npy: sha1://61762d8f0bdac57db64ceec1636e0009af0f02ef/curated_unit_IDs.npy?manifest=371f609a04189947e45ea8f29e60b0fd2edb1a69
#     - curated_unit_channels.npy: sha1://8b3a98b9d45c1c62eb4402245800e278873bd8e5/curated_unit_channels.npy
#     - continuous.dat: 