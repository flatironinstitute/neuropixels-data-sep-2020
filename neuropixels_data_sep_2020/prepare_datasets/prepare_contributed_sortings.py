import kachery_p2p as kp

def prepare_contributed_sortings(le_recordings_by_id):
    sortings_sc = prepare_sc_sortings(le_recordings_by_id)
    return sortings_sc

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
            SpykingCircus applied to {recording_id}
            '''.strip()
        ))
    return le_sortings