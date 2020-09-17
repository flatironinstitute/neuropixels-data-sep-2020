import kachery_p2p as kp
import neuropixels_data_sep_2020 as nd
import spikeextractors as se

# Here's the URI pointing to the spikeforest data
# Note: Right now it only contains a small subset of the data, the URI will get updated
SF_STUDY_SETS_URI = 'sha1://9a00ff43117879d8c2248622ad7d925ab1a38f8d/spikeforest_study_sets.json'

def main():
    # Load json containing info for spikeforest data
    spikeforest_study_sets = kp.load_object(SF_STUDY_SETS_URI)

    # For now, only focus on one study set
    study_sets_to_load = ['PAIRED_ENGLISH']

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
                print(f'Recordings in {study["name"]}: {[r["name"] for r in recordings]}')
                for rec in recordings:
                    # Create recording/sorting extractors
                    recording = nd.LabboxEphysRecordingExtractor(rec['recordingObject'], download=True)
                    sorting_true = nd.LabboxEphysSortingExtractor(rec['sortingObject'])
                    # Display information
                    duration_sec = recording.get_num_frames() / recording.get_sampling_frequency()
                    print('***************************************************************************')
                    print(f"{rec['studySetName']} {rec['studyName']} {rec['name']}")
                    print(f'Num channels: {len(recording.get_channel_ids())}')
                    print(f'Duration: {duration_sec} sec')
                    print(f'Num. true units: {len(sorting_true.get_unit_ids())}')
                    # TODO: write this somewhere to disk in int16 format, similar to the download_recordings.py script

if __name__ == '__main__':
    main()