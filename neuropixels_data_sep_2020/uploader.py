import hither as hi

def upload_file_to_compute_resource(file_uri: str):
    upload_files_to_compute_resource([file_uri])
    
def upload_files_to_compute_resource(x):
    print(f'Uploading to compute resource: {x}')
    with hi.Config(required_files=[x], force_run=True):
        hi.noop.run()
    