import hither as hi
import kachery_p2p as kp


# Through hither, this function will actually be run on the remote compute resource.
# By unsetting the job cache in the config we ensure the function actually runs. This
# ensures that the file actually gets downloaded from the peer network on the rcr.
# Any container used must use the same $KACHERY_STORAGE_DIR as the surrounding environment.
@hi.function('file_uploader', '0.1.0')
@hi.container('docker://magland/labbox-ephys-processing:latest')
def file_uploader(thefile: hi.File) -> str:
    import os
    return f"File loaded successfully by {os.uname()[1]}"

def upload_file_to_compute_resource(file_sha1: str) -> str:
    thefile = hi.File(file_sha1)
    with hi.Config(job_cache=None):
        result = file_uploader.run(thefile=thefile)
        hi.wait()
    return result.get_result()
    