import hither as hi
import numpy as np
import kachery_p2p as kp
import kachery as ka
import spikeextractors as se

from ._listify_ndarray import _listify_ndarray

@hi.function('cortexlab_create_recording_object', '0.1.1')
@hi.container('docker://magland/labbox-ephys-processing:0.2.18')
def cortexlab_create_recording_object(
    bin_uri,
    bin_size, # Later kachery-p2p will allow us to get this information from bin_uri
    channel_map_npy_uri,
    channel_positions_npy_uri,
    raw_num_channels,
    samplerate
):
    # dd = kp.read_dir(dirname)
    # bin_sha1 = dd['files'][bin_fname]['sha1']
    # bin_size = dd['files'][bin_fname]['size']
    # bin_uri = f'sha1://{bin_sha1}/raw.bin'
    X_channel_map = kp.load_npy(channel_map_npy_uri)
    X_channel_positions = kp.load_npy(channel_positions_npy_uri)
    # X_channel_map = kp.load_npy(dirname + '/channel_map.npy')
    # X_channel_positions = kp.load_npy(dirname + '/channel_positions.npy')
    channel_map = dict()
    channel_ids = [ii for ii in range(len(X_channel_map))]
    for id in channel_ids:
        channel_map[str(id)] = int(X_channel_map[id])
    channel_positions = dict()
    for id in channel_ids:
        channel_positions[str(id)] = _listify_ndarray(X_channel_positions[id, :].ravel())
    num_frames = int(bin_size / raw_num_channels / 2)
    assert num_frames * raw_num_channels * 2 == bin_size, f'Unexpected size of bin file: {bin_size} <> {num_frames * raw_num_channels * 2}'
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
    return ret

# @hi.function('cortexlab_create_sorting_object', '0.1.3')
# @hi.container('docker://magland/labbox-ephys-processing:0.2.18')
# def cortexlab_create_sorting_object(
#     times_npy_uri,
#     labels_npy_uri,
#     samplerate=30000
# ):
#     with hi.TemporaryDirectory() as tmpdir:
#         import spikeextractors as se
#         import kachery as ka
#         import h5py

#         times = ka.load_npy(times_npy_uri)
#         labels = ka.load_npy(labels_npy_uri)

#         sorting = se.NumpySortingExtractor()
#         sorting.set_sampling_frequency(samplerate)
#         sorting.set_times_labels(times.ravel(), labels.ravel())

#         save_path = tmpdir + '/sorting.h5'

#         unit_ids = sorting.get_unit_ids()
#         samplerate = sorting.get_sampling_frequency()
#         with h5py.File(save_path, 'w') as f:
#             f.create_dataset('unit_ids', data=np.array(unit_ids).astype(np.int32))
#             f.create_dataset('sampling_frequency', data=np.array([samplerate]).astype(np.float64))
#             for unit_id in unit_ids:
#                 x = sorting.get_unit_spike_train(unit_id=unit_id)
#                 f.create_dataset(f'unit_spike_trains/{unit_id}', data=np.array(x).astype(np.float64))
#         return dict(
#             sorting_format='h5_v1',
#             data=dict(
#                 h5_path=ka.store_file(save_path)
#             )
#         )