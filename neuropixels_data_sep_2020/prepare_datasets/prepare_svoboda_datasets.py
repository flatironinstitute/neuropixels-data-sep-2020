import kachery as ka
import kachery_p2p as kp
import scipy.io as sio
from ..uploader import upload_files_to_compute_resource
from .cortexlab_utils import cortexlab_create_sorting_object

def prepare_svoboda_datasets():
    # A Phase 3B Neuropixels probe was inserted 2.9 mm into secondary motor cortex of an awake,
    # head-fixed mouse performing a trial-based behavioural task. Overall 302 channels were
    # recorded using open source software SpikeGLX. The raw file is in 16bit integer format,
    # with the first 301 channels recorded in AP band, and the last channel for synchronization
    # purpose. 
    # After global demuxing and concatenation of trial-based recording into a continuous one using
    # CatGT, the recording was spike-sorted automatically by Kilosort2 and manually curated in
    # JRCLUST GUI. In total, 201 single units were identified.
    # data.mat file contains spike timing, cluster identify, site map, etc.
    # information. 
    # .meta file includes recording metadata, and CatGT parameters. 
    recording_obj_dataset1, sorting_obj_dataset1 = prepare_recording(
        bin_uri='sha1://f94ac8b42c423e551ad461f57c1cecf6cd5bc9d2/SC026_080619_g0_tcat.imec0.ap.bin?manifest=c3f82c2d10106b3739fca0ecb298c7330b6df72a',
        bin_file_size=76029609548,
        raw_num_channels=302,
        mat_uri='sha1://bb21a7cc8b9e409cd61ed1fc521937f72797ddad/data.mat?manifest=a736aa493def3770401301b9d2a946fd6fe5aff3',
        meta_uri='sha1://5f19fdf70696cf85b76208e41f08c0ac6b7e1e03/SC026_080619_g0_tcat.imec0.ap.meta' # perhaps will use in future
    )

    le_recordings = []
    le_recordings.append(dict(
        recordingId='svoboda-SC026_080619_g0_tcat',
        recordingLabel='svoboda-SC026_080619_g0_tcat',
        recordingPath=ka.store_object(recording_obj_dataset1, basename='svoboda-SC026_080619_g0_tcat.json'),
        recordingObject=recording_obj_dataset1,
        description='''
        A Phase 3B Neuropixels probe was inserted 2.9 mm into secondary motor cortex of an awake, head-fixed mouse performing a trial-based behavioural task.
        '''.strip()
    ))

    le_sortings = []
    le_sortings.append(dict(
        sortingId='svoboda-SC026_080619_g0_tcat:curated',
        sortingLabel='svoboda-SC026_080619_g0_tcat:curated',
        sortingPath=ka.store_object(sorting_obj_dataset1, basename='svoboda-SC026_080619_g0_tcat-curated.json'),
        sortingObject=sorting_obj_dataset1,

        recordingId='svoboda-SC026_080619_g0_tcat',
        recordingPath=ka.store_object(recording_obj_dataset1, basename='svoboda-SC026_080619_g0_tcat.json'),
        recordingObject=recording_obj_dataset1,

        description='''
        Curated spike sorting for svoboda-SC026_080619_g0_tcat
        '''.strip()
    ))

    return le_recordings, le_sortings

def prepare_recording(
        *,
        bin_uri,
        bin_file_size,
        raw_num_channels,
        mat_uri,
        meta_uri
):
    samplerate, chanmap, xcoords, ycoords, spike_times, spike_labels = load_info_from_mat(mat_uri)

    upload_files_to_compute_resource([mat_uri, meta_uri])

    times_npy_uri = ka.store_npy(spike_times)
    labels_npy_uri = ka.store_npy(spike_labels)

    sorting_object = cortexlab_create_sorting_object(
        times_npy_uri=times_npy_uri,
        labels_npy_uri=labels_npy_uri,
        samplerate=samplerate
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
    return recording_object, sorting_object

def load_info_from_mat(uri_mat):
    m = sio.loadmat(kp.load_file(uri_mat))
    print(m.keys())
    spike_times = m['spikeTimes'].squeeze()
    spike_labels = m['spikeClusters'].squeeze()
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
    return samplerate, chanmap, xcoords, ycoords, spike_times, spike_labels


