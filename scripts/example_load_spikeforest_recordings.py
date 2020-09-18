import kachery_p2p as kp
import neuropixels_data_sep_2020 as nd
import spikeextractors as se
import os
from pathlib import Path

# Here's the URI pointing to the spikeforest data
# Note: Right now it only contains a small subset of the data, the URI will get updated
# This one will load just three of the PAIRED_ENGLISH recordings
# SF_STUDY_SETS_URI = 'sha1://9a00ff43117879d8c2248622ad7d925ab1a38f8d/spikeforest_study_sets.json'

# This one will load all of the PAIRED_ENGLISH recordings:
SF_STUDY_SETS_URI = 'sha1://e92c3a88aa6173bd891aad69140fec228f2a7ffa/spikeforest_study_sets.json'

# This one will load all of the PAIRED_* recordings
# SF_STUDY_SETS_URI = 'sha1://44ac86a2dcc233e6471f24e8891bffd0e13c188f/spikeforest_study_sets.json'

# For now, only focus on one study set
study_sets_to_load = ['PAIRED_ENGLISH']
GLOBAL_OUTPUT_DIR = Path(os.path.abspath('study'))
os.makedirs(GLOBAL_OUTPUT_DIR, exist_ok=True)


def main():
    # Load json containing info for spikeforest data
    spikeforest_study_sets = kp.load_object(SF_STUDY_SETS_URI)

    # Iterate through the study sets
    study_sets = spikeforest_study_sets['studysets']
    print(f'Study sets: {[s["name"] for s in study_sets]}')
    for study_set in study_sets:
        if study_set['name'] in study_sets_to_load:
            # Iterate through the studies
            studies = study_set['studies']
            print(f'Studies in {study_set["name"]}: {[s["name"] for s in studies]}')
            for study in studies:
                # Iterate through the recordings
                recordings = study['recordings']
                STUDY_OUTPUT_DIR = os.path.join(GLOBAL_OUTPUT_DIR, study["name"])
                os.makedirs(STUDY_OUTPUT_DIR, exist_ok=True)
                print(f'Recordings in {study["name"]}: {[r["name"] for r in recordings]}')
                for rec in recordings:

                    RECORDING_OUTPUT_DIR = os.path.join(STUDY_OUTPUT_DIR, rec["name"])
                    os.makedirs(RECORDING_OUTPUT_DIR, exist_ok=True)
                    # Create recording/sorting extractors
                    recording = nd.LabboxEphysRecordingExtractor(rec['recordingObject'], download=True)
                    sorting_true = nd.LabboxEphysSortingExtractor(rec['sortingObject'])
                    filename = f'{rec["name"].replace(" ", "_")}.dat'
                    probename = f'{rec["name"].replace(" ", "_")}.prb'
                    sortname = f'{rec["name"].replace(" ", "_")}.npz'
                    # Display information
                    print(filename, probename)
                    duration_sec = recording.get_num_frames() / recording.get_sampling_frequency()
                    print('***************************************************************************')
                    print(f"{rec['studySetName']} {rec['studyName']} {rec['name']}")
                    print(f'Num channels: {len(recording.get_channel_ids())}')
                    print(f'Duration: {duration_sec} sec')
                    print(f'Num. true units: {len(sorting_true.get_unit_ids())}')
                    # TODO: write this somewhere to disk in int16 format, similar to the download_recordings.py script

                    recording.save_to_probe_file(os.path.join(RECORDING_OUTPUT_DIR, probename))
                    se.BinDatRecordingExtractor.write_recording(
                        recording,
                        os.path.join(RECORDING_OUTPUT_DIR, filename),
                        dtype='int16'
                    )
                    se.NpzSortingExtractor.write_sorting(
                        sorting_true,
                        os.path.join(RECORDING_OUTPUT_DIR, sortname)
                    )
                    print(f'########### DONE {os.path.join(RECORDING_OUTPUT_DIR, filename)} ###########')

if __name__ == '__main__':
    main()