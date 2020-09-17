import numpy as np
import kachery_p2p as kp
import kachery as ka


study_set_names = [
    'PAIRED_BOYDEN', 'PAIRED_CRCNS_HC1',
    'PAIRED_ENGLISH', 'PAIRED_KAMPFF',
    'PAIRED_MEA64C_YGER', 'PAIRED_MONOTRODE'
]

def main():
    SF_STUDY_SETS = kp.load_object('sha1://54d9ed77a2aa788b9ab67977476c2b51adb8a2c5/studysets.json')['StudySets']
    STUDY_SETS = []
    for SF_STUDY_SET in SF_STUDY_SETS:
        if SF_STUDY_SET['name'] in study_set_names:
            STUDY_SET = {
                'name': SF_STUDY_SET['name'],
                'info': SF_STUDY_SET['info'],
                'description': SF_STUDY_SET['description'],
                'studies': []
            }
            for SF_STUDY in SF_STUDY_SET['studies']:
                STUDY = {
                    'name': SF_STUDY['name'],
                    'studySetName': SF_STUDY['studySetName'],
                    'recordings': []
                }
                for SF_RECORDING in SF_STUDY['recordings'][:3]: # for now only load up to 3 recordings per study
                    recording_object = create_recording_object_from_spikeforest_recdir(SF_RECORDING['directory'], label=SF_RECORDING['name'])
                    sorting_object = create_sorting_object_from_spikeforest_recdir(SF_RECORDING['directory'], label=SF_RECORDING['name'])
                    print('********************************************************************************************')
                    print(f"{SF_RECORDING['studySetName']} {SF_RECORDING['studyName']} {SF_RECORDING['name']}")
                    print('********************************************************************************************')
                    RECORDING = {
                        "name": SF_RECORDING["name"],
                        "studyName": SF_RECORDING["studyName"],
                        "studySetName": SF_RECORDING["studySetName"],
                        "recordingObject": recording_object,
                        "sortingObject": sorting_object,
                        "sampleRateHz": SF_RECORDING["sampleRateHz"],
                        "numChannels": SF_RECORDING["numChannels"],
                        "durationSec": SF_RECORDING["durationSec"],
                        "numTrueUnits": SF_RECORDING["numTrueUnits"],
                        "old": {
                            "directory": SF_RECORDING["directory"],
                            "firingsTrue": SF_RECORDING["firingsTrue"],
                            "spikeSign": SF_RECORDING["spikeSign"]
                        }
                    }
                    STUDY['recordings'].append(RECORDING)
                STUDY_SET['studies'].append(STUDY)
            STUDY_SETS.append(STUDY_SET)
    spikeforest_study_sets = {
        'studysets': STUDY_SETS
    }
    # spikeforest_obj['self_reference'] = ka.store_object(spikeforest_obj)
    spikeforest_study_sets_path = ka.store_object(spikeforest_study_sets, basename='spikeforest_study_sets.json')
    print(spikeforest_study_sets_path)

def create_recording_object_from_spikeforest_recdir(recdir, label):
    raw_path = kp.load_file(recdir + '/raw.mda')
    raw_path = kp.store_file(raw_path, basename=label + '-raw.mda') # store with manifest
    print(raw_path)
    params = kp.load_object(recdir + '/params.json')
    geom_path = kp.load_file(recdir + '/geom.csv')
    geom = _load_geom_from_csv(geom_path)
    recording_object = dict(
        recording_format='mda',
        data=dict(
            raw=raw_path,
            geom=geom,
            params=params
        )
    )
    return recording_object

def create_sorting_object_from_spikeforest_recdir(recdir, label):
    params = kp.load_object(recdir + '/params.json')
    firings_path = kp.load_file(recdir + '/firings_true.mda')
    firings_path = ka.store_file(firings_path, basename=label + '-firings.mda')
    sorting_object = dict(
        sorting_format='mda',
        data=dict(
            firings=firings_path,
            samplerate=params['samplerate']
        )
    )
    print(sorting_object)
    return sorting_object

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

                    


if __name__ == '__main__':
    main()