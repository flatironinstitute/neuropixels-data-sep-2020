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
            'sorter_name': 'ironclust',
            'npz_uri': 'sha1://63f8577ee830f6e854fa37fa6dc9f300ddf5dcd2/ironclust.npz?manifest=63da49e17999ecf6082a1b7b1fcd50574a83ff57'
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
        },
        {
            'recording_id': 'svoboda-SC026_080619_g0_tcat_imec0',
            'sorter_name': 'hdsort',
            'npz_uri': 'sha1://dda1bfa8074c4a391bd941e6a341e493a0737768/hdsort.npz?manifest=6b0b78fe3508d1ddfed26b8666df1b7d94231c69'
        },
        {
            'recording_id': 'svoboda-SC026_080619_g0_tcat_imec0',
            'sorter_name': 'herdingspikes',
            'npz_uri': 'sha1://6136940a5e7d2beca95c35f3e000d38ce4d5e596/herdingspikes.npz?manifest=8ab6d0e2050d07f0c39e6dfb391c85513803e5ca'
        },
        {
            'recording_id': 'svoboda-SC026_080619_g0_tcat_imec0',
            'sorter_name': 'ironclust',
            'npz_uri': 'sha1://9bd3a55848d0ca9e98f899653e9554d965dbf6f1/ironclust.npz?manifest=dbf4ed27e7ce9e3fb4e6f00166423765c16bb161'
        },
        {
            'recording_id': 'svoboda-SC026_080619_g0_tcat_imec0',
            'sorter_name': 'kilosort2',
            'npz_uri': 'sha1://7c5100ee4cb77969a4697b524d12727315ac8f1e/kilosort2.npz?manifest=e36011dee42181fb4dcd76764658b848060a51f1'
        },
        {
            'recording_id': 'svoboda-SC026_080619_g0_tcat_imec0',
            'sorter_name': 'tridesclous',
            'npz_uri': 'sha1://20ac56455bc10c1c42c266d1773a4a58b258786f/tridesclous.npz?manifest=400f5b9a20d0bb3575f8e98859440db38aaccca7'
        },
        {
            'recording_id': 'cortexlab-single-phase-3',
            'sorter_name': 'hdsort',
            'npz_uri': 'sha1://d809e0ced7b37c059ee57fbda2f988a5b8dc1a55/hdsort.npz?manifest=fce43cc1a2850e0e7805a98539f24c0816a218e3'
        },
        {
            'recording_id': 'cortexlab-single-phase-3',
            'sorter_name': 'herdingspikes',
            'npz_uri': 'sha1://6b551be075b72dfa5c8df9a43541219630821197/herdingspikes.npz?manifest=b8ece277f8520feae2056f308e3269b6bd32e7a0'
        },
        {
            'recording_id': 'cortexlab-single-phase-3',
            'sorter_name': 'ironclust',
            'npz_uri': 'sha1://dfd2eaa009f6bc5b5c3f7eb979d0335f412cd575/ironclust.npz?manifest=0d9cedcf83a0de06be1a620777b2a5838e3c0d12'
        },
        {
            'recording_id': 'cortexlab-single-phase-3',
            'sorter_name': 'kilosort2',
            'npz_uri': 'sha1://3cf9943dedeb5f39344672ff701eebf12830d075/kilosort2.npz?manifest=8bbe8e6a536e63a274a3bd2e05ecc03116840855'
        },
        {
            'recording_id': 'cortexlab-single-phase-3',
            'sorter_name': 'spykingcircus',
            'npz_uri': 'sha1://d855d5314f36470719da17e4e5d2f48c808e65d3/spykingcircus.npz?manifest=af8e6189126b228ecde19237fb7a21807c7e2feb'
        },
        {
            'recording_id': 'cortexlab-single-phase-3',
            'sorter_name': 'tridesclous',
            'npz_uri': 'sha1://927721485f61cc9322536a8e9b457088b9dc16c7/tridesclous.npz?manifest=ee127bacf3d27de75b69313920af4691dd09c309'
        },
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