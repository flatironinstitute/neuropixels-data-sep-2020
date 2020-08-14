**Note**: This repo is in preparation

# neuropixels-data-sep-2020
Example electrophysiology recordings for the purpose of developing and optimizing spike sorting algorithms for neuropixels probes. Methods for dealing with drift are of particular interest.

## Overview

This repository contains links to some ephys recordings using neuropixels probes together with curated spike sorting results. It also contains two recordings with known imposed drift and two hybrid pseudo-ground truth neuropixels recordings. These may be used to evaluate the performance of spike sorting methods.

You can interact with the data in various ways:

* Visualize data within the web browser (links below)
* Load data directly into Python [SpikeInterface](https://github.com/SpikeInterface) objects (more information below)
* Download files from their original source (where available in links below)

## Datasets

The following recordings were generated using [prepare_datasets.py](./scripts/prepare_datasets/prepare_datasets.py).

**NOTE**:

The recording/sorting exploration tool in the web links below is under active
development, with particular attention to adding new visualizations and improving
performance. Users may experience load times of several seconds in some cases.
Thank you for your patience.

<!-- prepare_recording.py -->

<!-- BEGIN DATA TABLE -->

<!--- Auto-generated at 08/12/2020, 14:51:28-->
| Recording ID | Web link | Description |
|------ | ---- | ----------- |
| cortexlab-single-phase-3 | [view](http://ephys1.laboratorybox.org/default/recording/cortexlab-single-phase-3?feed=sha1://eab32b0c4b338c29d95b30b9e072cd709af48ae5/feed.json) | A "Phase3" Neuropixels electrode array was inserted into the brain of an awake, head-fixed mouse for about an hour. |
| cortexlab-single-phase-3.10sec | [view](http://ephys1.laboratorybox.org/default/recording/cortexlab-single-phase-3.10sec?feed=sha1://eab32b0c4b338c29d95b30b9e072cd709af48ae5/feed.json) | Extracted 10 seconds of data from the beginning of the recording |
| cortexlab-single-phase-3-ch0-7.10sec | [view](http://ephys1.laboratorybox.org/default/recording/cortexlab-single-phase-3-ch0-7.10sec?feed=sha1://eab32b0c4b338c29d95b30b9e072cd709af48ae5/feed.json) | Extracted a subset of channels and 10 seconds of data from the beginning of the recording |
| allen_mouse419112_probeE | [view](http://ephys1.laboratorybox.org/default/recording/allen_mouse419112_probeE?feed=sha1://eab32b0c4b338c29d95b30b9e072cd709af48ae5/feed.json) | A one hour neuropixels recording from Allen Institute |
| allen_mouse415148_probeE | [view](http://ephys1.laboratorybox.org/default/recording/allen_mouse415148_probeE?feed=sha1://eab32b0c4b338c29d95b30b9e072cd709af48ae5/feed.json) | A one hour neuropixels recording from Allen Institute |
| allen_mouse419112_probeE-ch0-7.10sec | [view](http://ephys1.laboratorybox.org/default/recording/allen_mouse419112_probeE-ch0-7.10sec?feed=sha1://eab32b0c4b338c29d95b30b9e072cd709af48ae5/feed.json) | Subset of channels and first 10 seconds of allen_mouse419112_probeE |
| allen_mouse419112_probeE-10sec | [view](http://ephys1.laboratorybox.org/default/recording/allen_mouse419112_probeE-10sec?feed=sha1://eab32b0c4b338c29d95b30b9e072cd709af48ae5/feed.json) | First 10 seconds of allen_mouse419112_probeE |


| Sorting ID | Web link | Description |
|------ | ---- | ----------- |
| cortexlab-single-phase-3:curated | [view](http://ephys1.laboratorybox.org/default/sorting/cortexlab-single-phase-3:curated?feed=sha1://eab32b0c4b338c29d95b30b9e072cd709af48ae5/feed.json) | Curated spike sorting for cortexlab-single-phase-3 |
| cortexlab-single-phase-3:curated_good | [view](http://ephys1.laboratorybox.org/default/sorting/cortexlab-single-phase-3:curated_good?feed=sha1://eab32b0c4b338c29d95b30b9e072cd709af48ae5/feed.json) | Curated spike sorting for cortexlab-single-phase-3 (good units only) |
| allen_mouse419112_probeE:curated | [view](http://ephys1.laboratorybox.org/default/sorting/allen_mouse419112_probeE:curated?feed=sha1://eab32b0c4b338c29d95b30b9e072cd709af48ae5/feed.json) | Curated spike sorting for allen_mouse419112_probeE |
| allen_mouse415148_probeE:curated | [view](http://ephys1.laboratorybox.org/default/sorting/allen_mouse415148_probeE:curated?feed=sha1://eab32b0c4b338c29d95b30b9e072cd709af48ae5/feed.json) | Curated spike sorting for allen_mouse415148_probeE |


[Browse all recordings](http://ephys1.laboratorybox.org/default?feed=sha1://eab32b0c4b338c29d95b30b9e072cd709af48ae5/feed.json)
<!-- END DATA TABLE -->

## Loading into Python and exporting to various formats

Because electrophysiology recordings can be large, we have created a peer-to-peer sharing system ([kachery-p2p](https://github.com/flatironinstitute/kachery-p2p)) that runs in Linux or Mac and interfaces directly to Python. By running a kachery-p2p daemon on your computer, you are participating in the network for sharing these datasets with other users of the system.

We have integrated this system with [SpikeInterface](https://github.com/SpikeInterface) which allows lazy loading of recordings into RecordingExtractor objects.

**Step 1.** You must be running a kachery-p2p daemon on the `flatiron1` channel.
[See these instructions](https://github.com/flatironinstitute/kachery-p2p).
The kachery-p2p tool has been tested on Linux and MacOS.

**Step 2.** Load a recording into a SpikeInterface recording extractor. From within the
`neuropixels-data-sep-2020` directory tree:

```python
import neuropixels_data_sep_2020 as nd
import spikeextractors as se

# Replace this with the desired recording ID from above
recording_id = 'cortexlab-single-phase-3 (ch 0-7, 10 sec)'

# Note: if the files are not already on your, then you need
# to run a kachery-p2p daemon on the flatiron1 channel.
recording = nd.load_recording(recording_id)

# recording is a SpikeInterface recording extractor
# so you can extract information
samplerate = recording.get_sampling_frequency()
num_frames = recording.get_num_frames()
num_channels = len(recording.get_channel_ids())
channel_locations = recording.get_channel_locations()

print(f'Num. channels: {num_channels}')
print(f'Duration: {num_frames / samplerate} sec')

# You can also extract the raw traces.
# This will only download the part of the raw file needed
traces = recording.get_traces(channel_ids=[0, 1, 2, 3], start_frame=0, end_frame=5000)
print(f'Shape of extracted traces: {traces.shape}')

# Or equivalently (using SubRecordingExtractor):
recording_sub = se.SubRecordingExtractor(
    parent_recording=recording,
    channel_ids=[0, 1, 2, 3],
    start_frame=0, end_frame=5000
)
traces2 = recording_sub.get_traces()
print(f'Shape of extracted traces: {traces2.shape}')
```

Once a dataset is loaded into a SpikeInterface extractor, you can
interact with it directly in Python. The data will be
lazy-loaded from the peer-to-peer network.

You can create subextractors as above, and export to any of the
[formats supported by SpikeExtractors](https://github.com/SpikeInterface/spikeextractors/tree/master/spikeextractors/extractors).

```python
import spikeextractors as se

# Example export to raw binary .dat
se.BinDatRecordingExtractor.write_recording(recording, '/output/file.dat')
```

## Data from Nick Steinmetz

Single Phase 3 dataset source data: http://data.cortexlab.net/singlePhase3

<!-- Source data kachery URI: `sha1dir://d40edb4e52ad5abef2c1689f7b04164fbf65271b.cortexlab-single-phase-3` -->

## Data from Josh Siegle

Notes about the Allen Institute curated sorting output:

Units were selected based on the following criteria:
```
ISI violations < 0.01
amplitude cutoff < 0.01
presence ratio >= 0.99
nearest-neighbors hit rate > 0.96
SNR > 3.0
```

Each unit was then manually inspected to confirm its quality.

There were a total of 76 high-quality units across both datasets.

<!-- * mouse419112_probeE
    - curated_unit_times.npy: sha1://57029ae68643881f5d4015397be87ba0d4815b52/curated_unit_times.npy
    - curated_unit_IDs.npy: sha1://61762d8f0bdac57db64ceec1636e0009af0f02ef/curated_unit_IDs.npy?manifest=371f609a04189947e45ea8f29e60b0fd2edb1a69
    - curated_unit_channels.npy: sha1://8b3a98b9d45c1c62eb4402245800e278873bd8e5/curated_unit_channels.npy
    - continuous.dat: sha1://39ae3fcccd3803170dd97fc9a8799e7169214419/continuous.dat?manifest=31942d7d97ff3a46fa1dbca72d8dc048bd65d5ce

* mouse415148_probeE
    - curated_unit_times.npy: sha1://4c717829e3ce6530349a38bd5f72fac216916276/curated_unit_times.npy -->

