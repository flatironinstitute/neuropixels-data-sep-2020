## Data from Nick Steinmetz (Cortexlab)

Single Phase 3 dataset source data: http://data.cortexlab.net/singlePhase3

See the [main README document](../README.md) for information on accessing these data.

<!-- Source data kachery URI: `sha1dir://d40edb4e52ad5abef2c1689f7b04164fbf65271b.cortexlab-single-phase-3` -->

Recordings with imposed drift at known times:

* cortexlab-drift-dataset1 (see above)
    - Manip. timestamps: `sha1://1117aac1f15e441fc82854a736e52e4b87e6d90c/dataset1/manip.timestamps_p2.npy`
    - Manip. positions: `sha1://9d4e8e9265573707cd1890eefa50fda6a8bd8ae5/manip.positions.npy`
* cortexlab-drift-dataset2 (see above)
    - In progress.... check back later...
    <!-- - Manip. timestamps: `sha1://b03ea67a69cbbcba214582cf6de1154bcf6b1f92/manip.timestamps.npy`
    - Manip. positions: `sha1://9d4e8e9265573707cd1890eefa50fda6a8bd8ae5/manip.positions.npy` -->

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