import kachery_p2p as kp
import spikeextractors as se
import numpy as np

class Bin1RecordingExtractor(se.RecordingExtractor):
    extractor_name = 'Bin1RecordingExtractor'
    is_writable = False
    def __init__(self, *, raw, raw_num_channels, num_frames, samplerate, channel_ids, channel_map, channel_positions, p2p, download=False):
        se.RecordingExtractor.__init__(self)
        
        self._raw = raw
        self._num_frames = num_frames
        self._samplerate = samplerate
        self._raw_num_channels = raw_num_channels
        self._channel_ids = channel_ids
        self._channel_map = channel_map
        self._channel_positions = channel_positions
        self._p2p = p2p

        if download:
            kp.load_file(self._raw)
        
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
        
        buf = kp.load_bytes(self._raw, start=i1, end=i2, p2p=self._p2p)
        X = np.frombuffer(buf, dtype=np.int16).reshape((end_frame - start_frame, self._raw_num_channels))
        
        ret = np.zeros((M, N))
        for ii, ch_id in enumerate(channel_ids):
            ret[ii, :] = X[:, self._channel_map[str(ch_id)]]
        
        return ret
