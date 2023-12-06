from huggingface_hub import snapshot_download
def download_from_hf(repo_id:str, local_dir:str, r_token:str):
    snapshot_download(repo_id=repo_id, local_dir=local_dir, token=r_token, local_dir_use_symlinks=False)

