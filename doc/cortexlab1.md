## Data from Nick Steinmetz (Cortexlab)

Single Phase 3 dataset source data: http://data.cortexlab.net/singlePhase3

See the [main README document](../README.md) for information on accessing these data.

<!-- Source data kachery URI: `sha1dir://d40edb4e52ad5abef2c1689f7b04164fbf65271b.cortexlab-single-phase-3` -->

### Recordings with imposed motion at known times

For awake, head-fixed mouse recordings, mice were both sexes, between 2 and 8 months of age. In all cases, a brief (<2 h) surgery to implant a steel headplate and 3D-printed plastic recording chamber was first performed. Following recovery, mice were acclimated over two sessions to head-fixation in the recording setup. During head-fixation mice were seated on a plastic apparatus with forepaws on a rotating rubber wheel. Three computer screens were positioned around the mouse at right angles. On or before the day of recording, mice were again briefly anaesthetized with isoflurane while one or more craniotomies were made with a dental drill. After several hours of recovery, mice were head-fixed in the setup. Probes had an Ag wire soldered onto the reference pad and shorted to ground; these reference wires were connected to an Ag/AgCl wire positioned above the skull. The craniotomies as well as the wire were submerged in a bath of lactate ringer solution, enclosed in the 3D printed plastic chamber. Electrodes were then advanced through the saline and through the intact dura, and lowered to the final position at approximately 10 µm/s. Electrodes were allowed to settle for approximately 20 min before starting recording. Recordings were made in external reference mode.

To make recordings with imposed motion between the brain and the probe, custom software was used to move the probe after insertion. The probes were affixed to steel rods held by Sensapex uMP-4 micromanipulators (Sensapex, Inc.). Two probes were inserted simultaneously held by two separate manipulators: a NP1.0 probe in one hemisphere and a NP2.0 probe in the opposite hemisphere, using location and angles of insertion matched as closely as possible between the two probes for symmetrical, matched recording sites. The hemisphere used for each probe was counterbalanced across sessions. After ~10 minutes of recording, custom software using the Sensapex API via Matlab was executed to move the manipulators in 10 steps forward and 10 alternating steps backwards, each step at 1 µm/sec for a duration of 50 sec, such that the period of the triangle wave motion was 100 sec, the total duration of the pattern was 1000 sec, and the amplitude was 50 µm. A synchronization signal was issued at the start of the motion and at the end for later alignment with neural data. The manipulator position was monitored online programmatically with further API calls during the progression of the motion to ensure that motion proceeded as expected, further confirmed by the visible pattern of motion in the detected location of spikes on the probe. After completion of the pattern of motion, another ~10 minutes of recording was carried out before ending the session.

**Obtaining the imposed motion timestamp/position data:**

* cortexlab-drift-dataset1
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