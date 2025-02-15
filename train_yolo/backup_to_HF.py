from huggingface_hub import upload_file
from huggingface_hub import login
login(token="<token>")

repo_id = "<repo_id>"

upload_file(
    path_or_fileobj="./runs/detect/train4/weights/best.pt",
    path_in_repo="model.pt",
    repo_id=repo_id,
    repo_type="model",
    token="<token>"
)
