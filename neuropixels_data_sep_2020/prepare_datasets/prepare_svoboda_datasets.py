import kachery as ka
import kachery_p2p as kp
import scipy.io as sio
import numpy as np
from ..uploader import upload_files_to_compute_resource

def prepare_svoboda_datasets():
    le_recordings = []
    le_sortings = []
    le_curation_actions = []

    # svoboda-SC026_080619_g0_tcat_imec0
    recording_obj, sorting_obj, unit_notes = prepare_recording(
        bin_uri='sha1://f94ac8b42c423e551ad461f57c1cecf6cd5bc9d2/SC026_080619_g0_tcat.imec0.ap.bin?manifest=c3f82c2d10106b3739fca0ecb298c7330b6df72a',
        bin_file_size=76029609548,
        raw_num_channels=302,
        mat_uri='sha1://bb21a7cc8b9e409cd61ed1fc521937f72797ddad/data.mat?manifest=a736aa493def3770401301b9d2a946fd6fe5aff3',
        meta_uri='sha1://5f19fdf70696cf85b76208e41f08c0ac6b7e1e03/SC026_080619_g0_tcat.imec0.ap.meta', # perhaps will use in future
        single_only=True
    )
    le_recordings.append(dict(
        recordingId='svoboda-SC026_080619_g0_tcat_imec0',
        recordingLabel='svoboda-SC026_080619_g0_tcat_imec0',
        recordingPath=ka.store_object(recording_obj, basename='svoboda-SC026_080619_g0_tcat_imec0.json'),
        recordingObject=recording_obj,
        description='''
        A Phase 3B Neuropixels probe was inserted 2.9 mm into secondary motor cortex of an awake, head-fixed mouse performing a trial-based behavioural task.
        '''.strip()
    ))
    le_sortings.append(dict(
        sortingId='svoboda-SC026_080619_g0_tcat_imec0:curated',
        sortingLabel='svoboda-SC026_080619_g0_tcat_imec0:curated',
        sortingPath=ka.store_object(sorting_obj, basename='svoboda-SC026_080619_g0_tcat_imec0-curated.json'),
        sortingObject=sorting_obj,

        recordingId='svoboda-SC026_080619_g0_tcat_imec0',
        recordingPath=ka.store_object(recording_obj, basename='svoboda-SC026_080619_g0_tcat_imec0.json'),
        recordingObject=recording_obj,

        description='''
        Curated spike sorting for svoboda-SC026_080619_g0_tcat_imec0
        '''.strip()
    ))
    for unit_id, notes in unit_notes.items():
        for note in notes:
            le_curation_actions.append(dict(
                type='ADD_UNIT_LABEL',
                sortingId='svoboda-SC026_080619_g0_tcat_imec0:curated',
                unitId=unit_id,
                label=note
            ))

    # svoboda-SC022_030319_g0_tcat_imec2
    recording_obj, sorting_obj, unit_notes = prepare_recording(
        bin_uri='sha1://9e7e76e467a28454ad9b76d29cb99d5330fffd5b/SC022_030319_g0_tcat.imec2.ap.bin?manifest=fc0b2783b88b61a5b84ac7a3dbd7fd9984557805',
        bin_file_size=112205135350,
        raw_num_channels=385,
        mat_uri='sha1://a7c467b959a66f072b5aa6ef7c13d9118b26942b/SC022_030319_g0_tcat.imec2.ap.mat?manifest=0970f173ad47c76212f4f16dd028d0850cda8745',
        meta_uri='sha1://a2bc30784266288cd6bd0b8c861dd182e538ed3c/SC022_030319_g0_tcat.imec2.ap.meta', # perhaps will use in future
        single_only=True
    )
    le_recordings.append(dict(
        recordingId='svoboda-SC022_030319_g0_tcat_imec2',
        recordingLabel='svoboda-SC022_030319_g0_tcat_imec2',
        recordingPath=ka.store_object(recording_obj, basename='svoboda-SC022_030319_g0_tcat_imec2.json'),
        recordingObject=recording_obj,
        description='''
        A Phase 3B Neuropixels probe was inserted 4.5 mm into left hemisphere striatum of an awake, head-fixed mouse performing a trial-based behavioural task.
        '''.strip()
    ))
    le_sortings.append(dict(
        sortingId='svoboda-SC022_030319_g0_tcat_imec2:curated',
        sortingLabel='svoboda-SC022_030319_g0_tcat_imec2:curated',
        sortingPath=ka.store_object(sorting_obj, basename='svoboda-SC022_030319_g0_tcat_imec2-curated.json'),
        sortingObject=sorting_obj,

        recordingId='svoboda-SC022_030319_g0_tcat_imec2',
        recordingPath=ka.store_object(recording_obj, basename='svoboda-SC022_030319_g0_tcat_imec2.json'),
        recordingObject=recording_obj,

        description='''
        Curated spike sorting for svoboda-SC022_030319_g0_tcat_imec2
        '''.strip()
    ))
    for unit_id, notes in unit_notes.items():
        for note in notes:
            le_curation_actions.append(dict(
                type='ADD_UNIT_LABEL',
                sortingId='svoboda-SC022_030319_g0_tcat_imec2:curated',
                unitId=unit_id,
                label=note
            ))
    
    # svoboda-SC026_080619_g0_tcat_imec2
    recording_obj, sorting_obj, unit_notes = prepare_recording(
        bin_uri='sha1://712b436030d1ab068eaf69c58172fffb261670ae/SC026_080619_g0_tcat.imec2.ap.bin?manifest=68c5ccc714a430143a435aee277f5c4209161e83',
        bin_file_size=96925126760,
        raw_num_channels=385,
        mat_uri='sha1://273707a53a5eb401441cd56dafdc3187bd6ae79f/SC026_080619_g0_tcat.imec2.ap.mat?manifest=dac1ac15f32067879408fa9f693c09891f6a51c1',
        meta_uri='sha1://1d9affa941e8953d61b9b80f4f8175b009384fa5/SC026_080619_g0_tcat.imec2.ap.meta', # perhaps will use in future
        single_only=True
    )
    le_recordings.append(dict(
        recordingId='svoboda-SC026_080619_g0_tcat_imec2',
        recordingLabel='svoboda-SC026_080619_g0_tcat_imec2',
        recordingPath=ka.store_object(recording_obj, basename='svoboda-SC026_080619_g0_tcat_imec2.json'),
        recordingObject=recording_obj,
        description='''
        A Phase 3B Neuropixels probe was inserted 4.7 mm into the left hemisphere hippocampus&thalamus of an awake, head-fixed mouse performing a trial-based behavioural task.
        '''.strip()
    ))
    le_sortings.append(dict(
        sortingId='svoboda-SC026_080619_g0_tcat_imec2:curated',
        sortingLabel='svoboda-SC026_080619_g0_tcat_imec2:curated',
        sortingPath=ka.store_object(sorting_obj, basename='svoboda-SC026_080619_g0_tcat_imec2-curated.json'),
        sortingObject=sorting_obj,

        recordingId='svoboda-SC026_080619_g0_tcat_imec2',
        recordingPath=ka.store_object(recording_obj, basename='svoboda-SC026_080619_g0_tcat_imec2.json'),
        recordingObject=recording_obj,

        description='''
        Curated spike sorting for svoboda-SC026_080619_g0_tcat_imec2
        '''.strip()
    ))
    for unit_id, notes in unit_notes.items():
        for note in notes:
            le_curation_actions.append(dict(
                type='ADD_UNIT_LABEL',
                sortingId='svoboda-SC026_080619_g0_tcat_imec2:curated',
                unitId=unit_id,
                label=note
            ))
    
    # svoboda-SC035_011020_g0_tcat_imec0
    recording_obj, sorting_obj, unit_notes = prepare_recording(
        bin_uri='sha1://ec1543ce5b040e5e56901859bf208b6f0afa4bb0/SC035_011020_g0_tcat.imec0.ap.bin?manifest=5cfb7bc0670ae892b2d84b81c402e0bb543578d0',
        bin_file_size=84952919590,
        raw_num_channels=385,
        mat_uri='sha1://dfb054655a665b5e9ad69c63a187b6da92a75c59/SC035_011020_g0_tcat.imec0.ap.2.mat?manifest=c25f9a710cdb810b833357d5aa3d64111d18ff2a',
        meta_uri='sha1://d11e93ae6d760a3fb57da1b8d91a86d5caae7a73/SC035_011020_g0_tcat.imec0.ap.meta', # perhaps will use in future
        single_only=True
    )
    le_recordings.append(dict(
        recordingId='svoboda-SC035_011020_g0_tcat_imec0',
        recordingLabel='svoboda-SC035_011020_g0_tcat_imec0',
        recordingPath=ka.store_object(recording_obj, basename='svoboda-SC035_011020_g0_tcat_imec0.json'),
        recordingObject=recording_obj,
        description='''
        A 2.0 4-shank Neuropixels probe was inserted 1 mm into the right hemisphere secondary motor cortex of an awake, head-fixed mouse performing a trial-based behavioural task.
        '''.strip()
    ))
    le_sortings.append(dict(
        sortingId='svoboda-SC035_011020_g0_tcat_imec0:curated',
        sortingLabel='svoboda-SC035_011020_g0_tcat_imec0:curated',
        sortingPath=ka.store_object(sorting_obj, basename='svoboda-SC035_011020_g0_tcat_imec0-curated.json'),
        sortingObject=sorting_obj,

        recordingId='svoboda-SC035_011020_g0_tcat_imec0',
        recordingPath=ka.store_object(recording_obj, basename='svoboda-SC035_011020_g0_tcat_imec0.json'),
        recordingObject=recording_obj,

        description='''
        Curated spike sorting for svoboda-SC035_011020_g0_tcat_imec0
        '''.strip()
    ))
    for unit_id, notes in unit_notes.items():
        for note in notes:
            le_curation_actions.append(dict(
                type='ADD_UNIT_LABEL',
                sortingId='svoboda-SC035_011020_g0_tcat_imec0:curated',
                unitId=unit_id,
                label=note
            ))

    return le_recordings, le_sortings, le_curation_actions

def prepare_recording(
        *,
        bin_uri,
        bin_file_size,
        raw_num_channels,
        mat_uri,
        meta_uri,
        single_only
):
    samplerate, chanmap, xcoords, ycoords, spike_times, spike_labels, unit_notes = load_info_from_mat(mat_uri)

    # exclude clusters 0 and -1
    spike_inds = np.where(spike_labels > 0)[0]
    spike_times = spike_times[spike_inds]
    spike_labels = spike_labels[spike_inds]

    if single_only:
        okay_to_use = np.zeros((len(spike_times,)))
        for unit_id, notes in unit_notes.items():
            if 'single' in notes:
                okay_to_use[np.where(spike_labels == unit_id)[0]] = 1
        spike_inds = np.where(okay_to_use)[0]
        print(f'Using {len(spike_inds)} of {len(spike_times)} events (single units only)')
        spike_times = spike_times[spike_inds]
        spike_labels = spike_labels[spike_inds]

    times_npy_uri = ka.store_npy(spike_times)
    labels_npy_uri = ka.store_npy(spike_labels)

    sorting_object = dict(
        sorting_format='npy1',
        data=dict(
            times_npy_uri=times_npy_uri,
            labels_npy_uri=labels_npy_uri,
            samplerate=samplerate
        )
    )

    num_frames = bin_file_size / (raw_num_channels * 2)
    print(num_frames)
    assert num_frames == int(num_frames)
    num_frames = int(num_frames)
    
    meta_lines = kp.load_text(meta_uri).split('\n') # perhaps use in future
    num_channels = len(chanmap)
    print(f'Number of channels: {num_channels}')

    channel_ids = [int(i) for i in range(num_channels)]
    channel_map = dict(zip([str(c) for c in channel_ids], [int(chanmap[i]) for i in range(num_channels)]))
    channel_positions = dict(zip([str(c) for c in channel_ids], [[float(xcoords[i]), float(ycoords[i])] for i in range(num_channels)]))

    recording_object = dict(
        recording_format='bin1',
        data=dict(
            raw=bin_uri,
            raw_num_channels=raw_num_channels,
            num_frames=num_frames,
            samplerate=samplerate,
            channel_ids=channel_ids,
            channel_map=channel_map,
            channel_positions=channel_positions
        )
    )

    return recording_object, sorting_object, unit_notes

def load_info_from_mat(uri_mat):
    m = sio.loadmat(kp.load_file(uri_mat))
    spike_times = m['spikeTimes'].squeeze()
    spike_labels = m['spikeClusters'].squeeze()
    cluster_notes = m['clusterNotes'].squeeze()
    samplerate = m['SampleRate'][0][0]
    siteMap = m['siteMap'].squeeze()
    xcoords = m['xcoords'].squeeze()
    ycoords = m['ycoords'].squeeze()
    chanmap = siteMap - 1
    xcoords = xcoords[chanmap]
    ycoords = ycoords[chanmap]
    num_chan = len(chanmap)
    assert len(xcoords) == num_chan
    assert len(ycoords) == num_chan
    
    unit_notes = {}
    for j in range(len(cluster_notes)):
        notes = [note for note in cluster_notes[j] if isinstance(note, str)]
        if len(notes) > 0:
            unit_notes[j+1] = notes
    
    return samplerate, chanmap, xcoords, ycoords, spike_times, spike_labels, unit_notes


