from typing import Union
import kachery_p2p as kp
import kachery as ka
from copy import deepcopy
from .bandpass_filter import bandpass_filter
import spikeextractors as se
import numpy as np
from .mdaextractors import MdaRecordingExtractor
from .binextractors import Bin1RecordingExtractor

from .nwbextractors import NwbRecordingExtractor

def _load_geom_from_csv(path: str) -> list:
    return _listify_ndarray(np.genfromtxt(path, delimiter=',').T)

def _listify_ndarray(x: np.ndarray) -> list:
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

def _try_mda_create_object(arg: Union[str, dict]) -> Union[None, dict]:
    if isinstance(arg, str):
        path = arg
        if path.startswith('sha1dir') or path.startswith('/'):
            dd = kp.read_dir(path)
            if dd is not None:
                if 'raw.mda' in dd['files'] and 'params.json' in dd['files'] and 'geom.csv' in dd['files']:
                    raw_path = path + '/raw.mda'
                    params_path = path + '/params.json'
                    geom_path = path + '/geom.csv'
                    geom_path_resolved = kp.load_file(geom_path)
                    assert geom_path_resolved is not None, f'Unable to load geom.csv from: {geom_path}'
                    params = kp.load_object(params_path)
                    assert params is not None, f'Unable to load params.json from: {params_path}'
                    geom = _load_geom_from_csv(geom_path_resolved)
                    return dict(
                        recording_format='mda',
                        data=dict(
                            raw=raw_path,
                            geom=geom,
                            params=params
                        )
                    )
    
    if isinstance(arg, dict):
        if ('raw' in arg) and ('geom' in arg) and ('params' in arg) and (type(arg['geom']) == list) and (type(arg['params']) == dict):
            return dict(
                recording_format='mda',
                data=dict(
                    raw=arg['raw'],
                    geom=arg['geom'],
                    params=arg['params']
                )
            )
    
    return None

def _try_nrs_create_object(arg: Union[str, dict]) -> Union[None, dict]:
    if isinstance(arg, str):
        path = arg
        if path.startswith('sha1dir') or path.startswith('/'):
            dd = kp.read_dir(path)
            if dd is not None:
                probe_file = None
                xml_file = None
                nrs_file = None
                dat_file = None
                for f in dd['files'].keys():
                    if f.endswith('.json'):
                        obj = kp.load_object(path + '/' + f)
                        if obj.get('format_version', None) in ['flatiron-probe-0.1', 'flatiron-probe-0.2']:
                            probe_file = path + '/' + f
                    elif f.endswith('.xml'):
                        xml_file = path + '/' + f
                    elif f.endswith('.nrs'):
                        nrs_file = path + '/' + f
                    elif f.endswith('.dat'):
                        dat_file = path + '/' + f
                if probe_file is not None and xml_file is not None and nrs_file is not None and dat_file is not None:
                    data = dict(
                        probe_file=probe_file,
                        xml_file=xml_file,
                        nrs_file=nrs_file,
                        dat_file=dat_file
                    )
                    return dict(
                        recording_format='nrs',
                        data=data
                    )
    
    if isinstance(arg, dict):
        if ('probe_file' in arg) and ('xml_file' in arg) and ('nrs_file' in arg) and ('dat_file' in arg):
            return dict(
                recording_format='nrs',
                data=dict(
                    probe_file=arg['probe_file'],
                    xml_file=arg['xml_file'],
                    nrs_file=arg['nrs_file'],
                    dat_file=arg['dat_file']
                )
            )
    
    return None


def _create_object_for_arg(arg: Union[str, dict]) -> Union[dict, None]:
    # if arg is a string ending with .json then replace arg by the object
    if (isinstance(arg, str)) and (arg.endswith('.json')):
        path = arg
        x = kp.load_object(path)
        if x is None:
            raise Exception(f'Unable to load object: {path}')
        return _create_object_for_arg(x)
    
    # check to see if it already has the recording_format field. If so, just return arg
    if (isinstance(arg, dict)) and ('recording_format' in arg):
        return arg

    # if has form dict(path='...') then replace by the string
    if (isinstance(arg, dict)) and ('path' in arg) and (type(arg['path']) == str):
        return _create_object_for_arg(arg['path'])

    # if has type LabboxEphysRecordingExtractor, then just get the object from arg.object()
    if isinstance(arg, LabboxEphysRecordingExtractor):
        return arg.object()

    # See if it has format 'nwb'
    if isinstance(arg, str) and arg.endswith('.nwb'):
        return dict(
            recording_format='nwb',
            data=dict(
                path=arg
            )
        )
    
    # See if it has format 'mda'
    obj = _try_mda_create_object(arg)
    if obj is not None:
        return obj
    
    # See if it has format 'nrs'
    obj = _try_nrs_create_object(arg)
    if obj is not None:
        return obj
    
    # See if it is of type filtered
    if (isinstance(arg, dict)) and ('recording' in arg) and ('filters' in arg):
        return dict(
            recording_format='filtered',
            data=dict(
                filters=arg['filters'],
                recording=_create_object_for_arg(arg['recording'])
            )
        )
    
    # See if it is type subrecording
    if (isinstance(arg, dict)) and ('recording' in arg) and ('group' in arg):
        return dict(
            recording_type='subrecording',
            data=dict(
                group=arg['group'],
                recording=_create_object_for_arg(arg['recording'])
            )
        )
    if (isinstance(arg, dict)) and ('recording' in arg) and ('groups' in arg):
        return dict(
            recording_type='subrecording',
            data=dict(
                groups=arg['groups'],
                recording=_create_object_for_arg(arg['recording'])
            )
        )
    if (isinstance(arg, dict)) and ('recording' in arg) and ('channel_ids' in arg):
        return dict(
            recording_type='subrecording',
            data=dict(
                channel_ids=arg['channel_ids'],
                recording=_create_object_for_arg(arg['recording'])
            )
        )
    
    return None    
    
# TODO: #1 reorganize this class to create a recording object that has all sha1:// paths nested
# This should be returned by the .object() method
class LabboxEphysRecordingExtractor(se.RecordingExtractor):
    def __init__(self, arg: Union[str, dict], download: bool=False):
        super().__init__()
        obj = _create_object_for_arg(arg)
        assert obj is not None
        self._object: dict = obj
        
        recording_format = self._object['recording_format']
        data: dict = self._object['data']
        if recording_format == 'mda':
            self._recording: se.RecordingExtractor = MdaRecordingExtractor(timeseries_path=data['raw'], samplerate=data['params']['samplerate'], geom=np.array(data['geom']), download=download)
        elif recording_format == 'nrs':
            self._recording: se.RecordingExtractor = NrsRecordingExtractor(**data)
        elif recording_format == 'nwb':
            path0 = kp.load_file(data['path'])
            self._recording: se.RecordingExtractor = NwbRecordingExtractor(path0, electrical_series_name='e-series')
        elif recording_format == 'bin1':
            self._recording: se.RecordingExtractor = Bin1RecordingExtractor(**data, p2p=True)
        elif recording_format == 'subrecording':
            R = LabboxEphysRecordingExtractor(data['recording'], download=download)
            if 'channel_ids' in data:
                self._recording: se.RecordingExtractor = se.SubRecordingExtractor(
                    parent_recording=R,
                    channel_ids=np.array(data['channel_ids'])
                )
            elif 'group' in data:
                channel_ids = np.array(R.get_channel_ids())
                groups = R.get_channel_groups(channel_ids=R.get_channel_ids())
                group = int(data['group'])
                inds = np.where(np.array(groups) == group)[0]
                channel_ids = channel_ids[inds]
                self._recording: se.RecordingExtractor = se.SubRecordingExtractor(
                    parent_recording=R,
                    channel_ids=channel_ids[inds]
                )
            elif 'groups' in data:
                raise Exception('This case not yet handled.')
            else:
                raise Exception('Unexpected data for subrecording')
        elif recording_format == 'filtered':
            R = LabboxEphysRecordingExtractor(data['recording'], download=download)
            self._recording: se.RecordingExtractor = _apply_filters(recording=R, filters=data['filters'])
        else:
            raise Exception(f'Unexpected recording format: {recording_format}')

        self.copy_channel_properties(recording=self._recording)
    
    @staticmethod
    def can_load(arg):
        try:
            obj = _create_object_for_arg(arg)
        except:
            obj = None
        return (obj is not None)

    def object(self) -> dict:
        return deepcopy(self._object)
    
    def hash(self) -> str:
        return ka.get_object_hash(self.object())
    
    def is_local(self):
        return _all_files_are_local_in_item(self._object)
    
    def download(self):
        return _download_files_in_item(self._object)

    def get_channel_ids(self) -> Union[list, np.ndarray]:
        return self._recording.get_channel_ids()

    def get_num_frames(self) -> int:
        return int(self._recording.get_num_frames())

    def get_sampling_frequency(self) -> float:
        return float(self._recording.get_sampling_frequency())

    def get_traces(self, channel_ids=None, start_frame=None, end_frame=None) -> np.ndarray:
        return self._recording.get_traces(channel_ids=channel_ids, start_frame=start_frame, end_frame=end_frame)

    # @staticmethod
    # def get_recording_object(recording):
    #     with hi.TemporaryDirectory() as tmpdir:
    #         MdaRecordingExtractor.write_recording(recording=recording, save_path=tmpdir)
    #         raw = ka.store_file(tmpdir + '/raw.mda')
    #         params = ka.load_object(tmpdir + '/params.json')
    #         geom = np.genfromtxt(tmpdir + '/geom.csv', delimiter=',').tolist()
    #         return dict(
    #             recording_format='mda',
    #             data=dict(
    #                 raw=raw,
    #                 params=params,
    #                 geom=geom
    #             )
    #         )

def _apply_filters(*, recording: se.RecordingExtractor, filters: list) -> se.RecordingExtractor:
    ret = recording
    for filter0 in filters:
        ret = _apply_filter(recording=ret, filter=filter0)
    return ret

def _apply_filter(*, recording: se.RecordingExtractor, filter: dict) -> se.RecordingExtractor:
    if filter['type'] == 'bandpass_filter':
        args = dict()
        if 'freq_min' in filter:
            args['freq_min'] = filter['freq_min']
        if 'freq_max' in filter:
            args['freq_max'] = filter['freq_max']
        if 'freq_wid' in filter:
            args['freq_wid'] = filter['freq_wid']
        return bandpass_filter(recording, **args)
    return None

class NrsRecordingExtractor(se.RecordingExtractor):
    extractor_name = 'NrsRecordingExtractor'
    is_writable = False
    def __init__(self, probe_file, xml_file, nrs_file, dat_file):
        se.RecordingExtractor.__init__(self)
        # info = check_load_nrs(dirpath)
        # assert info is not None
        probe_obj = kp.load_object(probe_file)
        xml_file = kp.load_file(xml_file)
        # nrs_file = kp.load_file(nrs_file)
        dat_file = kp.load_file(dat_file)

        from xml.etree import ElementTree as ET
        xml = ET.parse(xml_file)
        root_element = xml.getroot()
        try:
            txt = root_element.find('acquisitionSystem/samplingRate').text
            assert txt is not None
            self._samplerate = float(txt)
        except:
            raise Exception('Unable to load acquisitionSystem/samplingRate')
        try:
            txt = root_element.find('acquisitionSystem/nChannels').text
            assert txt is not None
            self._nChannels = int(txt)
        except:
            raise Exception('Unable to load acquisitionSystem/nChannels')
        try:
            txt = root_element.find('acquisitionSystem/nBits').text
            assert txt is not None
            self._nBits = int(txt)
        except:
            raise Exception('Unable to load acquisitionSystem/nBits')

        if self._nBits == 16:
            dtype = np.int16
        elif self._nBits == 32:
            dtype = np.int32
        else:
            raise Exception(f'Unexpected nBits: {self._nBits}')

        self._rec = se.BinDatRecordingExtractor(dat_file, sampling_frequency=self._samplerate, numchan=self._nChannels, dtype=dtype)

        self._channel_ids = probe_obj['channel']
        for ii in range(len(probe_obj['channel'])):
            channel = probe_obj['channel'][ii]
            x = probe_obj['x'][ii]
            y = probe_obj['y'][ii]
            z = probe_obj['z'][ii]
            group = probe_obj.get('group', probe_obj.get('shank'))[ii]
            self.set_channel_property(channel, 'location', [x, y, z])
            self.set_channel_property(channel, 'group', group)

    def get_channel_ids(self):
        return self._channel_ids

    def get_num_frames(self):
        return self._rec.get_num_frames()

    def get_sampling_frequency(self):
        return self._rec.get_sampling_frequency()

    def get_traces(self, channel_ids=None, start_frame=None, end_frame=None):
        if channel_ids is None:
            channel_ids = self._channel_ids
        return self._rec.get_traces(channel_ids=channel_ids, start_frame=start_frame, end_frame=end_frame)

def _all_files_are_local_in_item(x):
    if type(x) == str:
        if x.startswith('sha1://') or x.startswith('sha1dir://'):
            if not ka.get_file_info(x, fr=dict(url=None)):
                print('returning false')
                return False
        return True
    elif type(x) == dict:
        for _, val in x.items():
            if not _all_files_are_local_in_item(val):
                return False
        return True
    elif type(x) == list:
        for y in x:
            if not _all_files_are_local_in_item(y):
                return False
        return True
    elif type(x) == tuple:
        for y in x:
            if not _all_files_are_local_in_item(y):
                return False
        return True
    else:
        return True

def _download_files_in_item(x):
    if type(x) == str:
        if x.startswith('sha1://') or x.startswith('sha1dir://'):
            if not ka.get_file_info(x, fr=dict(url=None)):
                a = kp.load_file(x)
                assert a is not None, f'Unable to download file: {x}'
        return
    elif type(x) == dict:
        for _, val in x.items():
            _download_files_in_item(val)
        return
    elif type(x) == list:
        for y in x:
            _download_files_in_item(y)
        return
    elif type(x) == tuple:
        for y in x:
            _download_files_in_item(y)
        return
    else:
        return