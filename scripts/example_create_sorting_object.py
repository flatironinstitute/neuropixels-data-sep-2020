import numpy as np
import spikeextractors as se
import kachery as ka

def _create_sorting_object(sorting):
    unit_ids = sorting.get_unit_ids()
    times_list = []
    labels_list = []
    for i in range(len(unit_ids)):
        unit = unit_ids[i]
        times = sorting.get_unit_spike_train(unit_id=unit)
        times_list.append(times)
        labels_list.append(np.ones(times.shape) * unit)
    all_times = np.concatenate(times_list)
    all_labels = np.concatenate(labels_list)
    sort_inds = np.argsort(all_times)
    all_times = all_times[sort_inds]
    all_labels = all_labels[sort_inds]
    times_npy_uri = ka.store_npy(all_times)
    labels_npy_uri = ka.store_npy(all_labels)
    return dict(
        sorting_format='npy1',
        data=dict(
            times_npy_uri=times_npy_uri,
            labels_npy_uri=labels_npy_uri,
            samplerate=30000
        )
    )

# substitute sorting extractor here
recording, sorting = se.example_datasets.toy_example()

sorting_object = _create_sorting_object(sorting)
uri = ka.store_object(sorting_object)
print(f'Sorting URI: {uri}')