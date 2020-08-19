#!/usr/bin/env python

from neuropixels_data_sep_2020.extractors.labboxephyssortingextractor import LabboxEphysSortingExtractor
import hither as hi
import kachery as ka
import kachery_p2p as kp
import pandas as pd
import spikeextractors as se
from .cortexlab_utils import cortexlab_create_recording_object, cortexlab_create_sorting_object
from .create_subrecording_object import create_subrecording_object
from ..uploader import upload_file_to_compute_resource
from ..extractors import H5SortingExtractorV1

def prepare_cortexlab_datasets():
    R1 = cortexlab_create_recording_object.run(
        bin_uri='sha1://1b8592f0240603ae1019379cb47bad6475503aaf/tmp.dat?manifest=d05ca5b6e60e0fa8f2ff6f2f2ed822ff37da49c9',
        bin_size=87170751360, # Later kachery-p2p will allow us to get this information from bin_uri
        channel_map_npy_uri='sha1://b4de65964a758201db09f1e00d70ce40bca3a87e/channel_map.npy',
        channel_positions_npy_uri='sha1://434c1bca7fd857bc5a1c9215bd890025d082fe8d/channel_positions.py',
        raw_num_channels=385,
        samplerate=30000
    )

    times_npy_uri = 'sha1://2d8264241321fda3b6c987412b353232068c3e93/spike_times.npy?manifest=b7f91b25b95252cdeb299b8249a622d49eddabcc'
    labels_npy_uri = 'sha1://cd893db02d086b332ee46d56b2373dd0350bf471/spike_clusters.npy?manifest=6efc0362d708fa3a9ae5ce9280898a54e6e5d189'
    cluster_groups_csv_uri = 'sha1://d7d12256973a2d7f48edefdb4d8bb03f68e59aa5/cluster_groups.csv'
    upload_file_to_compute_resource(times_npy_uri)
    upload_file_to_compute_resource(labels_npy_uri)
    upload_file_to_compute_resource(cluster_groups_csv_uri)
    S1 = cortexlab_create_sorting_object.run(
        times_npy_uri=times_npy_uri,
        labels_npy_uri=labels_npy_uri,
        samplerate=30000
    )
    R2 = create_subrecording_object.run(
        recording_object=R1,
        channels=None,
        start_frame=0,
        end_frame=30000 * 10
    )
    R3 = create_subrecording_object.run(
        recording_object=R1,
        channels=[0, 1, 2, 3, 4, 5, 6, 7],
        start_frame=0,
        end_frame=30000 * 10
    )
    hi.wait()
    R1 = R1.get_result()
    S1 = S1.get_result()
    R2 = R2.get_result()
    R3 = R3.get_result()

    S1_good = _keep_good_units(S1, cluster_groups_csv_uri)

    le_recordings = []
    le_sortings = []
    le_recordings.append(dict(
        recordingId='cortexlab-single-phase-3',
        recordingLabel='cortexlab-single-phase-3 (full)',
        recordingPath=ka.store_object(R1, basename='cortexlab-single-phase-3.json'),
        recordingObject=R1,
        description='''
        A "Phase3" Neuropixels electrode array was inserted into the brain of an awake, head-fixed mouse for about an hour.
        '''.strip()
    ))
    le_sortings.append(dict(
        sortingId='cortexlab-single-phase-3:curated',
        sortingLabel='cortexlab-single-phase-3 Curated',
        sortingPath=ka.store_object(S1, basename='cortexlab-single-phase-3-curated.json'),
        sortingObject=S1,

        recordingId='cortexlab-single-phase-3',
        recordingPath=ka.store_object(R1, basename='cortexlab-single-phase-3.json'),
        recordingObject=R1,

        description='''
        Curated spike sorting for cortexlab-single-phase-3
        '''.strip()
    ))
    le_sortings.append(dict(
        sortingId='cortexlab-single-phase-3:curated_good',
        sortingLabel='cortexlab-single-phase-3 Curated (good units)',
        sortingPath=ka.store_object(S1_good, basename='cortexlab-single-phase-3-curated.json'),
        sortingObject=S1_good,

        recordingId='cortexlab-single-phase-3',
        recordingPath=ka.store_object(R1, basename='cortexlab-single-phase-3.json'),
        recordingObject=R1,

        description='''
        Curated spike sorting for cortexlab-single-phase-3 (good units only)
        '''.strip()
    ))
    le_recordings.append(dict(
        recordingId='cortexlab-single-phase-3.10sec',
        recordingLabel='cortexlab-single-phase-3 (10 sec)',
        recordingPath=ka.store_object(R2, basename='cortexlab-single-phase-3-10sec.json'),
        recordingObject=R2,
        description='Extracted 10 seconds of data from the beginning of the recording'
    ))
    le_recordings.append(dict(
        recordingId='cortexlab-single-phase-3-ch0-7.10sec',
        recordingLabel='cortexlab-single-phase-3 (ch 0-7, 10 sec)',
        recordingPath=ka.store_object(R2, basename='cortexlab-single-phase-3-ch0-7-10sec.json'),
        recordingObject=R3,
        description='Extracted a subset of channels and 10 seconds of data from the beginning of the recording'
    ))
    return le_recordings, le_sortings

def _keep_good_units(sorting_obj, cluster_groups_csv_uri):
    sorting = LabboxEphysSortingExtractor(sorting_obj)
    df = pd.read_csv(kp.load_file(cluster_groups_csv_uri), delimiter='\t')
    df_good = df.loc[df['group'] == 'good']
    good_unit_ids = df_good['cluster_id'].to_numpy().tolist()
    sorting_good = se.SubSortingExtractor(parent_sorting=sorting, unit_ids=good_unit_ids)
    with hi.TemporaryDirectory() as tmpdir:
        save_path = tmpdir + '/sorting.h5'
        H5SortingExtractorV1.write_sorting(sorting=sorting_good, save_path=save_path)
        return dict(
            sorting_format='h5_v1',
            data=dict(
                h5_path=ka.store_file(save_path)
            )
        )
