from copy import deepcopy
from .h5extractors.h5sortingextractorv1 import H5SortingExtractorV1
from typing import Union
import kachery as ka
import kachery_p2p as kp
import hither as hi
import spikeextractors as se
from .mdaextractors import MdaSortingExtractor

def _path(x):
    if type(x) is str:
        return x
    elif isinstance(x, hi.File):
        return x.path
    else:
        raise Exception('Cannot get path from:', x)

def _try_mda_create_object(arg: Union[str, dict], samplerate=None) -> Union[None, dict]:
    if isinstance(arg, str):
        path = arg
        if not ka.get_file_info(path):
            return None
        return dict(
            sorting_format='mda',
            data=dict(
                firings=path,
                samplerate=samplerate
            )
        )
    
    if isinstance(arg, dict):
        if 'firings' in arg:
            return dict(
                recording_format='mda',
                data=dict(
                    firings=arg['firings'],
                    samplerate=arg.get('samplerate', None)
                )
            )
    
    return None

def _create_object_for_arg(arg: Union[str, dict], samplerate=None) -> Union[dict, None]:
    # check to see if it already has the sorting_format field. If so, just return arg
    if (isinstance(arg, dict)) and ('sorting_format' in arg):
        return arg

    # if has form dict(path='...') then replace by the string
    if (isinstance(arg, dict)) and ('path' in arg) and (type(arg['path']) == str):
        arg = arg['path']

    # if has type LabboxEphysRecordingExtractor, then just get the object from arg.object()
    if isinstance(arg, LabboxEphysSortingExtractor):
        return arg.object()

    # if arg is a string ending with .json then replace arg by the object
    if (isinstance(arg, str)) and (arg.endswith('.json')):
        path = arg
        obj = kp.load_object(path)
        if obj is None:
            raise Exception(f'Unable to load object: {path}')
        return obj
    
    # See if it has format 'mda'
    obj = _try_mda_create_object(arg, samplerate=samplerate)
    if obj is not None:
        return obj
    
    return None    

class LabboxEphysSortingExtractor(se.SortingExtractor):
    def __init__(self, arg, samplerate=None):
        super().__init__()
        if (isinstance(arg, dict)) and ('sorting_format' in arg):
            obj = dict(arg)
        else:
            obj = _create_object_for_arg(arg, samplerate=samplerate)
            assert obj is not None, f'Unable to create sorting from arg: {arg}'
        self._object: dict = obj

        sorting_format = self._object['sorting_format']
        data: dict = self._object['data']
        if sorting_format == 'mda':
            firings_path = kp.load_file(data['firings'])
            assert firings_path is not None, f'Unable to load firings file: {data["firings"]}'
            self._sorting: se.SortingExtractor = MdaSortingExtractor(firings_file=firings_path, samplerate=data['samplerate'])
        elif sorting_format == 'h5_v1':
            h5_path = kp.load_file(data['h5_path'])
            self._sorting = H5SortingExtractorV1(h5_path=h5_path)
        elif sorting_format == 'npy1':
            times_npy = kp.load_npy(data['times_npy_uri'])
            labels_npy = kp.load_npy(data['labels_npy_uri'])
            samplerate = data['samplerate']
            S = se.NumpySortingExtractor()
            S.set_sampling_frequency(samplerate)
            S.set_times_labels(times_npy.ravel(), labels_npy.ravel())
            self._sorting = S            
        else:
            raise Exception(f'Unexpected sorting format: {sorting_format}')

        self.copy_unit_properties(sorting=self._sorting)
    
    def object(self):
        return deepcopy(self._object)
    
    def hash(self) -> str:
        return ka.get_object_hash(self.object())

    def get_unit_ids(self):
        return self._sorting.get_unit_ids()

    def get_unit_spike_train(self, unit_id, start_frame=None, end_frame=None):
        return self._sorting.get_unit_spike_train(unit_id=unit_id, start_frame=start_frame, end_frame=end_frame)
    
    def get_sampling_frequency(self):
        return self._sorting.get_sampling_frequency()
    
    def set_sampling_frequency(self, freq):
        self._sorting.set_sampling_frequency(freq)
    
    @staticmethod
    def write_sorting(sorting, save_path):
        MdaSortingExtractor.write_sorting(sorting=sorting, save_path=save_path)
