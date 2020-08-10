**Note**: This repo is in preparation

# neuropixels-data-sep-2020
Example neuropixels datasets for the purpose of developing and optimizing spike sorting algorithms.

## Overview

This repository contains links to some ephys recordings using neuropixels probes together with curated spike sorting results. It also contains two recordings with known imposed drift and two hybrid pseudo-ground truth neuropixels recordings. These may be used to evaluate the performance of spike sorting methods.

You can interact with the data in various ways

* Visualize data within the web browser (labbox-ephys links below)
* Downloading files from their original source (where available)
* Loading data directly into Python [SpikeInterface](https://github.com/SpikeInterface) objects (using [kachery-p2p](https://github.com/flatironinstitute/kachery-p2p))

## Datasets

The following recordings were generated using [prepare_datasets.py](./scripts/prepare_datasets/prepare_datasets.py).

<!-- prepare_recording.py -->
[View in browser (labbox-ephys)](http://a9b927286911d4338ab905d0eabba09d-949726054.us-east-2.elb.amazonaws.com:8081/default?feed=sha1://0acd8a8f10b5e5b7df39057d0eba004bac323e0d/feed.json)

| Recording  | Description |
|------ | ----------- |
| cortexlab-single-phase-3 (full) | Placeholder for cortexlab-single-phase-3 |
| cortexlab-single-phase-3 (ch 0-7, 10 sec) | Placeholder for cortexlab-single-phase-3-ch0-7.10sec |
| cortexlab-single-phase-3 (10 sec) | Placeholder for cortexlab-single-phase-3.10sec |
| sieglelab_mouse419112_probeE (full) | Placeholder for sieglelab_mouse419112_probeE |
| sieglelab_mouse419112_probeE (ch 0-7, 10 sec) | Placeholder for sieglelab_mouse419112_probeE-ch0-7.10sec |
| sieglelab_mouse419112_probeE (10 sec) | Placeholder for sieglelab_mouse419112_probeE-10sec |


| Sorting  | Description |
|------ | ----------- |
| cortexlab-single-phase-3 Curated | Placeholder for cortexlab-single-phase-3:curated |
<!-- -->

## Loading into Python and exporting to various formats

To load the data into [SpikeInterface](https://github.com/SpikeInterface) recording extractors, you must be running a kachery-p2p daemon on the flatiron1 channel. [See these instructions.](https://github.com/flatironinstitute/kachery-p2p)

```python
from neuropixels_data_sep_2020 import LabboxEphysRecordingExtractor
import spikeextractors as se

# Replace this with the desired recording URI from above
recording_uri = 'sha1://595d78d1e1a61c12c437afedd808b565cce82e5e/sieglelab_mouse419112_probeE-ch0-7-10sec.json'
# If the files are not already on your computer
# then you need to run a kachery-p2p daemon
# on the flatiron1 channel.
recording = LabboxEphysRecordingExtractor(recording_uri, download=False)

# recording is a SpikeInterface recording extractor
# so you can extract information
samplerate = recording.get_sampling_frequency()
num_frames = recording.get_num_frames()
num_channels = len(recording.get_channel_ids())
channel_locations = recording.get_channel_locations()

print(f'Num. channels: {num_channels} sec')
print(f'Duration: {num_frames / samplerate} sec')

# You can also extract the raw traces
# and if download=False above, it will
# only download the part of the raw file
# needed
traces = recording.get_traces(channel_ids=[0, 1, 2, 3], start_frame=0, end_frame=5000)
print(f'Shape of extracted traces: {traces.shape}')

# Or equivalently:
recording_sub = se.SubRecordingExtractor(
    parent_recording=recording,
    channel_ids=[0, 1, 2, 3],
    start_frame=0, end_frame=5000
)
traces2 = recording_sub.get_traces()
print(f'Shape of extracted traces: {traces2.shape}')
```

Once a dataset is loaded into a SpikeInterface extractor, you can
interact with it directly in Python. With the `download=False` flag,
the data will be lazy-loaded from the network.

You can create subextractors as above, and export to any of the
[formats supported by SpikeExtractors](https://github.com/SpikeInterface/spikeextractors/tree/master/spikeextractors/extractors).

```python
import spikeextractors as se

# Example export to raw binary .dat
se.BinDatRecordingExtractor.write_recording(recording, '/output/file.dat')

# Example export to .nwb format
se.NwbRecordingExtractor.write_recording(recording, '/output/file.dat')
```

## Data from Nick Steinmetz

Single Phase 3 dataset source data: http://data.cortexlab.net/singlePhase3

<!-- Source data kachery URI: `sha1dir://d40edb4e52ad5abef2c1689f7b04164fbf65271b.cortexlab-single-phase-3` -->

## Data from Josh Siegle

Notes about the sieglelab curated sorting output:

Selected units based on the following criteria:
```
ISI violations < 0.01
amplitude cutoff < 0.01
presence ratio >= 0.99
nearest-neighbors hit rate > 0.96
SNR > 3.0
```

Then manually inspected each one to confirm its quality.

There were a total of 76 high-quality units across both datasets.

<!-- * mouse419112_probeE
    - curated_unit_times.npy: sha1://57029ae68643881f5d4015397be87ba0d4815b52/curated_unit_times.npy
    - curated_unit_IDs.npy: sha1://61762d8f0bdac57db64ceec1636e0009af0f02ef/curated_unit_IDs.npy?manifest=371f609a04189947e45ea8f29e60b0fd2edb1a69
    - curated_unit_channels.npy: sha1://8b3a98b9d45c1c62eb4402245800e278873bd8e5/curated_unit_channels.npy
    - continuous.dat: sha1://39ae3fcccd3803170dd97fc9a8799e7169214419/continuous.dat?manifest=31942d7d97ff3a46fa1dbca72d8dc048bd65d5ce

* mouse415148_probeE
    - curated_unit_times.npy: sha1://4c717829e3ce6530349a38bd5f72fac216916276/curated_unit_times.npy -->

