import os
import requests
import json


TOKEN = os.getenv("ACCESS_TOKEN")
OWNER = "kimnjang"
REPO = "deploy-pipeline"

WORKFLOW_ID = "train-for-deploy.yml"
headers = {
    "Authorization": f"token {TOKEN}",
}


def call_dispatcher(data):
    units = data["hidden_units"]
    optimizer = data["optimizer"]
    version = data["version"]
    print(units, optimizer, version)
    data_json = {
        "ref": "main",
        "inputs": {
            "units": str(units),
            "optimizer": optimizer,
            "version": version,
        },
    }
    # data = {"ref": "main", "inputs":{"model_path": model_path, "model_tag": model_tag }}
    res = requests.post(
        f"https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows/{WORKFLOW_ID}/dispatches",
        headers=headers,
        data=json.dumps(data_json),
    )
    print(res.text)
    print(res.status_code)


if __name__ == "__main__":
    hpo = {"hidden_units": 64, "optimizer": "adam"}
    call_dispatcher(hpo)
