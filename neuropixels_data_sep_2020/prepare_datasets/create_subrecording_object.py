import hither as hi
import numpy as np
import kachery_p2p as kp
import kachery as ka
import spikeextractors as se

from ._listify_ndarray import _listify_ndarray

@hi.function('create_subrecording_object', '0.1.1')
@hi.container('docker://magland/labbox-ephys-processing:latest')
def create_subrecording_object(
    recording_object,
    channels,
    start_frame,
    end_frame
):
    from .bin1recordingextractor import Bin1RecordingExtractor
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
        channel_positions=d['channel_positions'],
        p2p=True
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