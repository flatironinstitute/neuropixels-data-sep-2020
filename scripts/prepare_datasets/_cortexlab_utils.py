import hither as hi
import numpy as np
import kachery_p2p as kp
import kachery as ka
import spikeextractors as se

@hi.function('create_recording_object_cortexlab', '0.1.3')
@hi.container('docker://magland/labbox-ephys-processing:latest')
def create_recording_object_cortexlab(dirname, bin_fname, raw_num_channels, samplerate):
    dd = kp.read_dir(dirname)
    bin_sha1 = dd['files'][bin_fname]['sha1']
    bin_size = dd['files'][bin_fname]['size']
    bin_uri = f'sha1://{bin_sha1}/raw.bin'
    X_channel_map = kp.load_npy(dirname + '/channel_map.npy')
    X_channel_positions = kp.load_npy(dirname + '/channel_positions.npy')
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

@hi.function('create_subrecording_object', '0.1.0')
@hi.container('docker://magland/labbox-ephys-processing:latest')
def create_subrecording_object(
    recording_object,
    channels,
    start_frame,
    end_frame
):
    recording_format = recording_object['recording_format']
    assert recording_format == 'bin1', f'Unsupported recording format: {recording_format}'
    d = recording_object['data']
    rec = Bin1RecordingExtractor(
        raw=d['raw'],
        num_frames=d['num_frames'],
        raw_num_channels=d['raw_num_channels'],
        channel_ids=d['channel_ids'],
        samplerate=d['samplerate'],
        channel_map=d['channel_map'],
        channel_positions=d['channel_positions']
    )
    rec2 = se.SubRecordingExtractor(parent_recording=rec, channel_ids=channels, start_frame=start_frame, end_frame=end_frame)
    with hi.TemporaryDirectory() as tmpdir:
        raw_fname = tmpdir + '/raw.bin'
        rec2.get_traces().astype('int16').tofile(raw_fname)
        new_bin_uri = ka.store_file(raw_fname)
        new_channel_map = dict()
        new_channel_positions = dict()
        for ii, id in enumerate(rec2.get_channel_ids()):
            new_channel_map[str(id)] = ii
            new_channel_positions[str(id)] = rec2.get_channel_locations(channel_ids=[id])[0]
        return dict(
            recording_format='bin1',
            data=dict(
                raw=new_bin_uri,
                raw_num_channels=len(rec2.get_channel_ids()),
                num_frames=end_frame - start_frame,
                samplerate=rec2.get_sampling_frequency(),
                channel_ids=_listify_ndarray(rec2.get_channel_ids()),
                channel_map=new_channel_map,
                channel_positions=new_channel_positions
            )
        )

import spikeextractors as se
class Bin1RecordingExtractor(se.RecordingExtractor):
    extractor_name = 'Bin1RecordingExtractor'
    is_writable = False
    def __init__(self, *, raw, raw_num_channels, num_frames, samplerate, channel_ids, channel_map, channel_positions):
        se.RecordingExtractor.__init__(self)
        
        self._raw = raw
        self._num_frames = num_frames
        self._samplerate = samplerate
        self._raw_num_channels = raw_num_channels
        self._channel_ids = channel_ids
        self._channel_map = channel_map
        self._channel_positions = channel_positions
        
        for id in self._channel_ids:
            pos = self._channel_positions[str(id)]
            self.set_channel_property(id, 'location', pos)

    def get_channel_ids(self):
        return self._channel_ids

    def get_num_frames(self):
        return self._num_frames

    def get_sampling_frequency(self):
        return self._samplerate

    def get_traces(self, channel_ids=None, start_frame=None, end_frame=None):
        if start_frame is None:
            start_frame = 0
        if end_frame is None:
            end_frame = self._num_frames
        if channel_ids is None:
            channel_ids = self._channel_ids
        M = len(channel_ids)
        N = end_frame - start_frame
        
        i1 = start_frame * 2 * self._raw_num_channels
        i2 = end_frame * 2 * self._raw_num_channels
        
        buf = kp.load_bytes(self._raw, start=i1, end=i2)
        X = np.frombuffer(buf, dtype=np.int16).reshape((end_frame - start_frame, self._raw_num_channels))
        
        ret = np.zeros((M, N))
        for m in range(M):
            ret[m, :] = X[:, self._channel_map[str(m)]]
        
        return ret

def _listify_ndarray(x):
    if isinstance(x, list):
        return x
    if x.ndim == 1:
        if np.issubdtype(x.dtype, np.integer):
            return [int(val) for val in x]
        else:
            return [float(val) for val in x]
    elif x.ndim == 2:
        ret = []
        for j in range(x.shape[1]):
            ret.append(_listify_ndarray(x[:, j]))
        return ret
    elif x.ndim == 3:
        ret = []
        for j in range(x.shape[2]):
            ret.append(_listify_ndarray(x[:, :, j]))
        return ret
    elif x.ndim == 4:
        ret = []
        for j in range(x.shape[3]):
            ret.append(_listify_ndarray(x[:, :, :, j]))
        return ret
    else:
        raise Exception('Cannot listify ndarray with {} dims.'.format(x.ndim))
