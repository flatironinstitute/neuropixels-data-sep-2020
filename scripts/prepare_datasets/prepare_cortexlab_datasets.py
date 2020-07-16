#!/usr/bin/env python

import hither as hi
import kachery as ka

from neuropixels_data_sep_2020 import cortexlab_create_recording_object, create_subrecording_object

with hi.RemoteJobHandler(compute_resource_uri='feed://90766008f6c0c12e18b851f973f4076167b0928bfbc5c2309fb3a35ccd30bd4b?name=ccmlin008.flatironinstitute.org') as jh:
    with hi.Config(job_handler=jh, container=True):
        X1 = cortexlab_create_recording_object.run(
            dirname='sha1dir://d40edb4e52ad5abef2c1689f7b04164fbf65271b.cortexlab-single-phase-3',
            bin_fname='Hopkins_20160722_g0_t0.imec.ap_CAR.bin',
            raw_num_channels=385,
            samplerate=30000
        )
        X2 = create_subrecording_object.run(
            recording_object=X1,
            channels=[0, 1, 2, 3, 4, 5, 6, 7],
            start_frame=0,
            end_frame=30000 * 10
        )
        hi.wait()

print(ka.store_object(X1.get_result(), basename='cortexlab-single-phase-3.json'))
print(ka.store_object(X2.get_result(), basename='cortexlab-single-phase-3.ch0-7.10sec.json'))