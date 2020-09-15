import kachery_p2p as kp

def prepare_contributed_sortings(le_recordings_by_id):
    sortings_sc = prepare_sc_sortings(le_recordings_by_id)
    sortings_mh = prepare_mh_sortings(le_recordings_by_id)
    return sortings_sc + sortings_mh

def prepare_sc_sortings(le_recordings_by_id):
    spyking_circus_sortings = {
        'cortexlab-single-phase-3': 'sha1://2e748216d16d97a8a7ad54ba05f34df1d5fc724c/file.json',
        'allen_mouse419112_probeE': 'sha1://b8ddf7527849d1734e533bb0b11787e6a1ac6eae/file.json',
        'allen_mouse415148_probeE': 'sha1://be9d013191dc7a5c539c61b87da6672281d00da8/file.json',
        'cortexlab-drift-dataset1': 'sha1://d618a4dfed3e8e74d980af60289a31186d962cb6/file.json',
        'cortexlab-drift-dataset2': 'sha1://9c8e813fbab74c3c463295c13aa1c6e28a74a157/file.json',
        # 'svoboda-SC026_080619_g0_tcat': 'sha1://1e435f56012eb3f1b2996d04a4d40edd4d0d2968/file.json',
        'svoboda-SC022_030319_g0_tcat_imec2': 'sha1://d5eb47fad3e6d4fd73c9dbea1f3e5a431ab73d2d/file.json'
    }
    le_sortings = []
    for recording_id, sorting_path in spyking_circus_sortings.items():
        le_recording = le_recordings_by_id[recording_id]
        print(sorting_path)
        sorting_object = kp.load_object(sorting_path)
        le_sortings.append(dict(
            sortingId=recording_id + ':spyking_circus',
            sortingLabel=recording_id + ':spyking_circus',
            sortingPath=sorting_path,
            sortingObject=sorting_object,

            recordingId=recording_id,
            recordingPath=le_recording['recordingPath'],
            recordingObject=le_recording['recordingObject'],

            tags=['contributed'],

            description=f'''
            SpykingCircus applied to {recording_id} (contributed by P. Yger)
            '''.strip()
        ))
    return le_sortings

def prepare_mh_sortings(le_recordings_by_id):
    x = [
        {
            'recording_id': 'allen_mouse419112_probeE',
            'sorter_name': 'hdsort',
            'npz_uri': 'sha1://28efb237ea07041eb94993a316c53c1f22f59c64/hdsort.npz?manifest=32dc916a479afa8fc7932c12818750bc6b3b9956'
        },
        {
            'recording_id': 'allen_mouse419112_probeE',
            'sorter_name': 'herdingspikes',
            'npz_uri': 'sha1://ad8ecc05529ca124ba204a9110c7a50d3f0916e0/herdingspikes.npz?manifest=640cd612d3791a4dd18b0fd704716a021ac6170b'
        },
        {
            'recording_id': 'allen_mouse419112_probeE',
            'sorter_name': 'kilosort2',
            'npz_uri': 'sha1://b5cc1eed184a9cb544cd11f49141fe59e12d473c/kilosort2.npz?manifest=7d4ec32d692c9ed3b72aaefcf0c31aa0352ec95b'
        },
        {
            'recording_id': 'allen_mouse419112_probeE',
            'sorter_name': 'spykingcircus',
            'npz_uri': 'sha1://cb07e45b1b969ebfa5a29faf7156585365104349/spykingcircus.npz?manifest=1fdb0dd7642a816db185e975bf43c85fa9bb6578'
        }
    ]
    le_sortings = []
    for a in x:
        recording_id = a['recording_id']
        sorter_name = a['sorter_name']
        print('{recording_id} {sorter_name}')
        npz_uri = a['npz_uri']
        d = kp.load_npy(npz_uri)
        print(d)
        sorting_object = {
            'sorting_format': 'npy2',
            'data': {
                'npz_uri': npz_uri,
                'unit_ids': d['unit_ids'].tolist(),
                'sampling_frequency': float(d['sampling_frequency'])
            }
        }
        sorting_path = kp.store_object(sorting_object, basename=recording_id + '--' + sorter_name + '.json')
        le_recording = le_recordings_by_id[recording_id]
        print(sorting_path)
        le_sortings.append(dict(
            sortingId=recording_id + ':mh-' + sorter_name,
            sortingLabel=recording_id + ':mh-' + sorter_name,
            sortingPath=sorting_path,
            sortingObject=sorting_object,

            recordingId=recording_id,
            recordingPath=le_recording['recordingPath'],
            recordingObject=le_recording['recordingObject'],

            tags=['contributed'],

            description=f'''
            {sorter_name} applied to {recording_id} (contributed by M. Hennig)
            '''.strip()
        ))
    return le_sortings