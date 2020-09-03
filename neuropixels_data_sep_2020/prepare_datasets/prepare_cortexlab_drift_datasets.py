import kachery as ka
import kachery_p2p as kp
import scipy.io as sio
from ..uploader import upload_files_to_compute_resource

def prepare_cortexlab_drift_datasets():
    recording_obj_dataset1, manip_timestamps1, manip_positions1 = prepare_recording(
        bin_uri='sha1://294a665f4e4de1c7377a47182941d22da45d6ff7/steinmetz_dataset1.p2_g0_t0.imec0.ap.bin?manifest=dc01ff169e44b538e3c009b10783b43f57c068e6',
        bin_file_size=45205648180,
        raw_num_channels=385, # guessing this so that bin_file_size is divisible by raw_num_channels*2
        chanmap_mat_uri='sha1://4693f77e3883861f28dc2a634f0e1e5776bc7167/dataset1/NP2_kilosortChanMap.mat',
        manip_timestamps_uri='sha1://1117aac1f15e441fc82854a736e52e4b87e6d90c/dataset1/manip.timestamps_p2.npy',
        manip_positions_uri='sha1://9d4e8e9265573707cd1890eefa50fda6a8bd8ae5/manip.positions.npy',
        meta_uri='sha1://6cd209edd2221d8814f12ad883220482a5bde3ff/dataset1/p2_g0_t0.imec0.ap.meta' # perhaps will use in future
    )
    recording_obj_dataset2, manip_timestamps2, manip_positions2 = prepare_recording(
        bin_uri='sha1://840a6e81e9c7e6e0f9aedc8a17ce32fb22fe3eb3/steinmetz_dataset2.p2_g1_t0.imec0.ap.bin?manifest=e73b452d6e09b6495024b85835b21a7a72dd6a5a',
        bin_file_size=62099840880,
        raw_num_channels=385, # guessing this so that bin_file_size is divisible by raw_num_channels*2
        chanmap_mat_uri='sha1://4693f77e3883861f28dc2a634f0e1e5776bc7167/dataset1/NP2_kilosortChanMap.mat', # assuming same as dataset1
        manip_timestamps_uri='sha1://b03ea67a69cbbcba214582cf6de1154bcf6b1f92/manip.timestamps.npy',
        manip_positions_uri='sha1://9d4e8e9265573707cd1890eefa50fda6a8bd8ae5/manip.positions.npy',
        meta_uri='sha1://b7d175b3ddbe73d802244b209be58230a965f394/p2_g1_t0.imec0.ap.meta' # perhaps will use in future
    )


    le_recordings = []
    le_recordings.append(dict(
        recordingId='cortexlab-drift-dataset1',
        recordingLabel='cortexlab-drift-dataset1',
        recordingPath=ka.store_object(recording_obj_dataset1, basename='cortexlab-drift-dataset1.json'),
        recordingObject=recording_obj_dataset1,
        description='''
        Neuropixels 2 recording with imposed drift (dataset1).
        '''.strip()
    ))
    le_recordings.append(dict(
        recordingId='cortexlab-drift-dataset2',
        recordingLabel='cortexlab-drift-dataset2',
        recordingPath=ka.store_object(recording_obj_dataset2, basename='cortexlab-drift-dataset2.json'),
        recordingObject=recording_obj_dataset2,
        description='''
        Neuropixels 2 recording with imposed drift (dataset2).
        '''.strip()
    ))

    return le_recordings

def prepare_recording(*, bin_uri, bin_file_size, raw_num_channels, chanmap_mat_uri, manip_timestamps_uri, manip_positions_uri, meta_uri):
    manip_timestamps = kp.load_npy(manip_timestamps_uri)
    manip_positions = kp.load_npy(manip_positions_uri)
    num_frames = bin_file_size / (raw_num_channels * 2)
    print(num_frames)
    assert num_frames == int(num_frames)
    num_frames = int(num_frames)
    samplerate = 30000
    
    chanmap, xcoords, ycoords = load_chanmap_data_from_mat('sha1://4693f77e3883861f28dc2a634f0e1e5776bc7167/dataset1/NP2_kilosortChanMap.mat')
    meta_lines = kp.load_text(meta_uri).split('\n') # perhaps use in future
    num_channels = len(chanmap)
    print(f'Number of channels: {num_channels}')

    channel_ids = [int(i) for i in range(num_channels)]
    channel_map = dict(zip([str(c) for c in channel_ids], [int(chanmap[i]) for i in range(num_channels)]))
    channel_positions = dict(zip([str(c) for c in channel_ids], [[float(xcoords[i]), float(ycoords[i])] for i in range(num_channels)]))

    ret = dict(
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
    return ret, manip_timestamps, manip_positions

def load_chanmap_data_from_mat(uri_mat):
    m = sio.loadmat(kp.load_file(uri_mat))
    chanmap = m['chanMap0ind'].squeeze()
    xcoords = m['xcoords'].squeeze()
    ycoords = m['ycoords'].squeeze()
    num_chan = len(chanmap)
    assert len(xcoords) == num_chan
    assert len(ycoords) == num_chan
    return chanmap, xcoords, ycoords


