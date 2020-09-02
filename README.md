# neuropixels-data-sep-2020
Example electrophysiology recordings for the purpose of developing and optimizing spike sorting algorithms for neuropixels probes. Methods for dealing with drift are of particular interest.

**Note**: This repo is in preparation. We will be adding more recordings and curated sortings over time. We are also improving the reliability of the peer-to-peer file transfer as well as adding functionality to the web GUI.

## Overview

This repository contains links to some ephys recordings using neuropixels probes together with curated spike sorting results. It also contains two recordings with known imposed drift. In the future, it will contain hybrid pseudo-ground truth neuropixels recordings. These may be used to evaluate the performance of spike sorting methods. We will be adding to this collection over time.

You can interact with the data in various ways:

* Visualize data within the web browser (links below) - (this application will also available to run locally, or self-hosted)
* Load data directly into Python [SpikeInterface](https://github.com/SpikeInterface) objects (more information below)
* Download files from their original source (where available in links below)

## Datasets

The following recordings were generated using [prepare_datasets.py](./scripts/prepare_datasets/prepare_datasets.py).

**NOTE**:

The recording/sorting exploration tool in the web links below is under active
development, with particular attention to adding new visualizations and improving
performance. Users may experience long load times in some cases. Over time the
responsiveness will improve. Thank you for your patience.

<!-- prepare_recording.py -->

<!-- BEGIN DATA TABLE -->

<!--- Auto-generated at 08/31/2020, 08:21:04-->
| Recording ID | Web link | Description |
|------ | ---- | ----------- |
| cortexlab-single-phase-3 | [view](http://ephys1.laboratorybox.org/default/recording/cortexlab-single-phase-3?feed=sha1://3c435b50122f185513c0ca7bfa01a5715c28e8d5/feed.json) | A "Phase3" Neuropixels electrode array was inserted into the brain of an awake, head-fixed mouse for about an hour. |
| cortexlab-single-phase-3.10sec | [view](http://ephys1.laboratorybox.org/default/recording/cortexlab-single-phase-3.10sec?feed=sha1://3c435b50122f185513c0ca7bfa01a5715c28e8d5/feed.json) | Extracted 10 seconds of data from the beginning of the recording |
| cortexlab-single-phase-3-ch0-7.10sec | [view](http://ephys1.laboratorybox.org/default/recording/cortexlab-single-phase-3-ch0-7.10sec?feed=sha1://3c435b50122f185513c0ca7bfa01a5715c28e8d5/feed.json) | Extracted a subset of channels and 10 seconds of data from the beginning of the recording |
| cortexlab-drift-dataset1 | [view](http://ephys1.laboratorybox.org/default/recording/cortexlab-drift-dataset1?feed=sha1://3c435b50122f185513c0ca7bfa01a5715c28e8d5/feed.json) | Neuropixels 2 recording with imposed drift (dataset1). |
| cortexlab-drift-dataset2 | [view](http://ephys1.laboratorybox.org/default/recording/cortexlab-drift-dataset2?feed=sha1://3c435b50122f185513c0ca7bfa01a5715c28e8d5/feed.json) | Neuropixels 2 recording with imposed drift (dataset2). |
| allen_mouse419112_probeE | [view](http://ephys1.laboratorybox.org/default/recording/allen_mouse419112_probeE?feed=sha1://3c435b50122f185513c0ca7bfa01a5715c28e8d5/feed.json) | A one hour neuropixels recording from Allen Institute |
| allen_mouse415148_probeE | [view](http://ephys1.laboratorybox.org/default/recording/allen_mouse415148_probeE?feed=sha1://3c435b50122f185513c0ca7bfa01a5715c28e8d5/feed.json) | A one hour neuropixels recording from Allen Institute |
| allen_mouse419112_probeE-ch0-7.10sec | [view](http://ephys1.laboratorybox.org/default/recording/allen_mouse419112_probeE-ch0-7.10sec?feed=sha1://3c435b50122f185513c0ca7bfa01a5715c28e8d5/feed.json) | Subset of channels and first 10 seconds of allen_mouse419112_probeE |
| allen_mouse419112_probeE-10sec | [view](http://ephys1.laboratorybox.org/default/recording/allen_mouse419112_probeE-10sec?feed=sha1://3c435b50122f185513c0ca7bfa01a5715c28e8d5/feed.json) | First 10 seconds of allen_mouse419112_probeE |


| Sorting ID | Web link | Description |
|------ | ---- | ----------- |
| cortexlab-single-phase-3:curated | [view](http://ephys1.laboratorybox.org/default/sorting/cortexlab-single-phase-3:curated?feed=sha1://3c435b50122f185513c0ca7bfa01a5715c28e8d5/feed.json) | Curated spike sorting for cortexlab-single-phase-3 |
| cortexlab-single-phase-3:curated_good | [view](http://ephys1.laboratorybox.org/default/sorting/cortexlab-single-phase-3:curated_good?feed=sha1://3c435b50122f185513c0ca7bfa01a5715c28e8d5/feed.json) | Curated spike sorting for cortexlab-single-phase-3 (good units only) |
| allen_mouse419112_probeE:curated | [view](http://ephys1.laboratorybox.org/default/sorting/allen_mouse419112_probeE:curated?feed=sha1://3c435b50122f185513c0ca7bfa01a5715c28e8d5/feed.json) | Curated spike sorting for allen_mouse419112_probeE |
| allen_mouse415148_probeE:curated | [view](http://ephys1.laboratorybox.org/default/sorting/allen_mouse415148_probeE:curated?feed=sha1://3c435b50122f185513c0ca7bfa01a5715c28e8d5/feed.json) | Curated spike sorting for allen_mouse415148_probeE |


[Browse all recordings](http://ephys1.laboratorybox.org/default?feed=sha1://3c435b50122f185513c0ca7bfa01a5715c28e8d5/feed.json)
<!-- END DATA TABLE -->

## Loading into **Python** and exporting to various formats

Because electrophysiology recordings can be large, we have created a peer-to-peer sharing system ([kachery-p2p](https://github.com/flatironinstitute/kachery-p2p)) that runs in Linux or Mac and interfaces directly to Python. By running a kachery-p2p daemon on your computer, you are participating in the network for sharing these datasets with other users of the system.

We have integrated this system with [SpikeInterface](https://github.com/SpikeInterface) which allows lazy loading of recordings into RecordingExtractor objects.

**Prerequisites: Linux or MacOS**

**Step 1.** Clone and install this repo in development mode

```bash
git clone https://github.com/flatironinstitute/neuropixels-data-sep-2020
cd neuropixels-data-sep-2020
```

We recommend you create a conda environment based on the `environment.yml` file distributed in this repo:

```bash
conda env create -f environment.yml
conda activate neuropixels-2020
```

Install this repo in editable (development) mode:

```
pip install -e .
```

If using conda, be sure that you always activate the conda environment prior to working with this repo.

For subsequent updates, run `git pull` and rerun the `pip install -e .`

**Step 2.** You must be running a kachery-p2p daemon on the `flatiron1` channel.

```python
kachery-p2p-start-daemon --channel flatiron1
```

Keep this daemon running in a terminal. You may want to use tmux or a similar tool to keep this daemon running even if the terminal is closed.

For more information, [see these instructions](https://github.com/flatironinstitute/kachery-p2p). The kachery-p2p tool has been tested on Linux and MacOS.

**Step 3.** Load a sorting into a SpikeInterface sorting extractor using the following example script:

```python
#!/usr/bin/env python3

# You need to be running the kachery-p2p daemon, flatiron1 channel
import neuropixels_data_sep_2020 as nd
import spikeextractors as se

# sorting will be a se.SortingExtractor object
sorting = nd.load_sorting('cortexlab-single-phase-3:curated') # use a sorting ID from table above
unit_ids = sorting.get_unit_ids()
print(f'Num. units in sorting: {len(unit_ids)}')

# load a spike train for a particular unit
unit_id = unit_ids[3]
st = sorting.get_unit_spike_train(unit_id=unit_id)
print(f'Num. events in unit {unit_id}: {len(st)}')

# The output should be:
# Num. units in sorting: 675
# Num. events in unit 8: 6022
```

See also: [./scripts/load_all_sortings.py](./scripts/load_all_sortings.py)

**Step 4.** Load a recording into a SpikeInterface recording extractor:

```python
# You need to be running the kachery-p2p daemon, flatiron1 channel
import neuropixels_data_sep_2020 as nd
import spikeextractors as se

# Replace this with the desired recording ID from above
recording_id = 'cortexlab-single-phase-3 (ch 0-7, 10 sec)'

# Note: if the files are not already on your machine, then you need
# to run a kachery-p2p daemon on the flatiron1 channel.
# Use download=True to download the entire recording at once
#    download=False means lazy download
recording = nd.load_recording(recording_id, download=False)

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

## Downloading the data for use in **MATLAB or other languages**

If you plan to do your analysis in python we recommend you use spikeextractors as a container for passing data around as illustrated above. If not, or for other reasons, you can download the data directly to disk by editing and running [scripts/download_recordings.py](./scripts/download_recordings.py). In that case you may want to think about downloading a subset of the data using se.SubRecordingExtractor for testing prior to loading the entire files.

## Data from Nick Steinmetz (Cortexlab)

Single Phase 3 dataset source data: http://data.cortexlab.net/singlePhase3

<!-- Source data kachery URI: `sha1dir://d40edb4e52ad5abef2c1689f7b04164fbf65271b.cortexlab-single-phase-3` -->

Recordings with imposed drift at known times:

* cortexlab-drift-dataset1 (see above)
    - Manip. timestamps: `sha1://1117aac1f15e441fc82854a736e52e4b87e6d90c/dataset1/manip.timestamps_p2.npy`
    - Manip. positions: `sha1://9d4e8e9265573707cd1890eefa50fda6a8bd8ae5/manip.positions.npy`
* cortexlab-drift-dataset2 (see above)
    - Manip. timestamps: `sha1://b03ea67a69cbbcba214582cf6de1154bcf6b1f92/manip.timestamps.npy`
    - Manip. positions: `sha1://9d4e8e9265573707cd1890eefa50fda6a8bd8ae5/manip.positions.npy`

The following Python snippet can be used to load the timestamps and positions of the manipulated drift

```python
# Make sure you have the kachery-p2p daemon running
import kachery_p2p as kp

# Note: these are from cortexlab-drift-dataset1
timestamps_uri = 'sha1://1117aac1f15e441fc82854a736e52e4b87e6d90c/dataset1/manip.timestamps_p2.npy'
positions_uri = 'sha1://9d4e8e9265573707cd1890eefa50fda6a8bd8ae5/manip.positions.npy'

timestamps = kp.load_npy(timestamps_uri).squeeze()
positions = kp.load_npy(positions_uri).squeeze()

print(timestamps) # array of shape (22,) [0, 580.1500031, ...]
print(positions) # array of shape (22,) [0, 0, 50, 0, 50, ...]
```


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

