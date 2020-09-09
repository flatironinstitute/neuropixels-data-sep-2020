#!/usr/bin/env python

import hither as hi
import kachery as ka
import kachery_p2p as kp
from .create_subrecording_object import create_subrecording_object

def prepare_allen_datasets():
    bin1_uri = 'sha1://39ae3fcccd3803170dd97fc9a8799e7169214419/allen_mouse419112_probeE.dat?manifest=f021b78c2fac87af872d6e6cf3f7505194395692'
    bin2_uri = 'sha1://c5acd91cfde60bc8ba619f5b03245fe6c034f682/allen_mouse415148_probeE.dat?manifest=8c99b1ffd502dc5281fc569e652d45b787df5ebc'
    channel_info_uri = 'sha1://349d7f018f4f09da5c230a9d46e07c2aeffbc1e2/channel_info.csv'
    channel_positions = _load_channel_positions_from_csv(channel_info_uri)
    X1 = dict(
        recording_format='bin1',
        data=dict(
            raw=bin1_uri,
            raw_num_channels=384,
            num_frames=105000000, # infer from file size and guess of samplerate
            samplerate=30000, # guess
            channel_ids=list(range(0, 384)), # for now
            # The following are placeholders... we need the actual geom file.
            channel_map=dict(zip([str(c) for c in range(0, 384)], [c for c in range(0, 384)])),
            channel_positions=channel_positions
        )
    )
    XX2 = dict(
        recording_format='bin1',
        data=dict(
            raw=bin2_uri,
            raw_num_channels=384,
            num_frames=105000000, # infer from file size and guess of samplerate
            samplerate=30000, # guess
            channel_ids=list(range(0, 384)), # for now
            # The following are placeholders... we need the actual geom file.
            channel_map=dict(zip([str(c) for c in range(0, 384)], [c for c in range(0, 384)])),
            channel_positions=channel_positions
        )
    )

    times1_npy_uri = 'sha1://57029ae68643881f5d4015397be87ba0d4815b52/curated_unit_times.npy?manifest=80b52bf7cd37ef7fb0d4ba5d1dfa543ffb207ce1'
    labels1_npy_uri = 'sha1://61762d8f0bdac57db64ceec1636e0009af0f02ef/curated_unit_IDs.npy?manifest=f716950fadb97a5a154d8762220194af6381e2c1'
    unit_channels1_npy_uri = 'sha1://8b3a98b9d45c1c62eb4402245800e278873bd8e5/curated_unit_channels.npy?manifest=91e899e3d4649f3ae457f6bf0926211dea8aa8fe'
    S1 = dict(
        sorting_format='npy1',
        data=dict(
            times_npy_uri=times1_npy_uri,
            labels_npy_uri=labels1_npy_uri,
            samplerate=30000
        )
    )

    times2_npy_uri = 'sha1://4c717829e3ce6530349a38bd5f72fac216916276/curated_unit_times.npy?manifest=557d7cf852892b6f333b9355a3ea2293558b2a29'
    labels2_npy_uri = 'sha1://f55da958a7725edf8bde63eecf1d53edcb9de76d/curated_unit_IDs.npy?manifest=e028ca15c01ea5f53e2bd341ab001741e7842084'
    unit_channels2_npy_uri = 'sha1://7f2079292b1ef29264b9152073d09dfa3b4dcbe7/curated_unit_channels.npy?manifest=2b35e2b83c9af0431b8aa1ab69e1846e21f24668'
    S2 = dict(
        sorting_format='npy1',
        data=dict(
            times_npy_uri=times2_npy_uri,
            labels_npy_uri=labels2_npy_uri,
            samplerate=30000
        )
    )

    X1a = create_subrecording_object.run(
        recording_object=X1,
        channels=[0, 1, 2, 3, 4, 5, 6, 7],
        start_frame=0,
        end_frame=30000 * 10
    )
    X1b = create_subrecording_object.run(
        recording_object=X1,
        channels=None,
        start_frame=0,
        end_frame=30000 * 10
    )
    hi.wait()
    X1a = X1a.get_result()
    X1b = X1b.get_result()

    # labbox-ephys format for recordings
    le_recordings = []
    le_sortings = []
    le_recordings.append(dict(
        recordingId='allen_mouse419112_probeE',
        recordingLabel='allen_mouse419112_probeE (full)',
        recordingPath=ka.store_object(X1, basename='allen_mouse419112_probeE.json'),
        recordingObject=X1,
        description='''
        A one hour neuropixels recording from Allen Institute
        '''.strip()
    ))
    le_recordings.append(dict(
        recordingId='allen_mouse415148_probeE',
        recordingLabel='allen_mouse415148_probeE (full)',
        recordingPath=ka.store_object(XX2, basename='allen_mouse415148_probeE.json'),
        recordingObject=XX2,
        description='''
        A one hour neuropixels recording from Allen Institute
        '''.strip()
    ))
    le_sortings.append(dict(
        sortingId='allen_mouse419112_probeE:curated',
        sortingLabel='allen_mouse419112_probeE Curated',
        sortingPath=ka.store_object(S1, basename='allen_mouse419112_probeE-curated.json'),
        sortingObject=S1,

        recordingId='allen_mouse419112_probeE',
        recordingPath=ka.store_object(X1, basename='allen_mouse419112_probeE.json'),
        recordingObject=X1,
        description='''
        Curated spike sorting for allen_mouse419112_probeE
        '''.strip()
    ))
    le_sortings.append(dict(
        sortingId='allen_mouse415148_probeE:curated',
        sortingLabel='allen_mouse415148_probeE Curated',
        sortingPath=ka.store_object(S2, basename='allen_mouse415148_probeE-curated.json'),
        sortingObject=S2,

        recordingId='allen_mouse415148_probeE',
        recordingPath=ka.store_object(XX2, basename='allen_mouse415148_probeE.json'),
        recordingObject=XX2,

        description='''
        Curated spike sorting for allen_mouse415148_probeE **Updated 9 Sep 2020**
        '''.strip()
    ))
    le_recordings.append(dict(
        recordingId='allen_mouse419112_probeE-ch0-7.10sec',
        recordingLabel='allen_mouse419112_probeE (ch 0-7, 10 sec)',
        recordingPath=ka.store_object(X1a, basename='allen_mouse419112_probeE-ch0-7-10sec.json'),
        recordingObject=X1a,
        description='''
        Subset of channels and first 10 seconds of allen_mouse419112_probeE
        '''.strip()
    ))
    le_recordings.append(dict(
        recordingId='allen_mouse419112_probeE-10sec',
        recordingLabel='allen_mouse419112_probeE (10 sec)',
        recordingPath=ka.store_object(X1b, basename='allen_mouse419112_probeE-10sec.json'),
        recordingObject=X1b,
        description='''
        First 10 seconds of allen_mouse419112_probeE
        '''.strip()
    ))

    return le_recordings, le_sortings

def _load_channel_positions_from_csv(uri):
    csvtxt = kp.load_text(uri)
    lines = csvtxt.split('\n')
    lines = lines[1:] # skip header
    lines = [line for line in lines if line] # skip empty lines
    channel_positions = {}
    for line in lines:
        vals = line.split(',')
        ii = int(vals[0])
        x = float(vals[1])
        y = float(vals[2])
        channel_positions[str(ii)] = [x, y]
    return channel_positions

# - curated_unit_times.npy: sha1://57029ae68643881f5d4015397be87ba0d4815b52/curated_unit_times.npy
#     - curated_unit_IDs.npy: sha1://61762d8f0bdac57db64ceec1636e0009af0f02ef/curated_unit_IDs.npy?manifest=371f609a04189947e45ea8f29e60b0fd2edb1a69
#     - curated_unit_channels.npy: sha1://8b3a98b9d45c1c62eb4402245800e278873bd8e5/curated_unit_channels.npy
#     - continuous.dat: 