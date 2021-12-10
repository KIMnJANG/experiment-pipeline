import os
import requests
import json


TOKEN = "<GITHUB ACCESS TOKEN>"
OWNER = "KIMnJANG"
REPO = "mnist-model"

WORKFLOW_ID = "deploy.yml"
headers = {
    "Authorization": f"token {TOKEN}",
}


def call_dispatcher(hpo):
    units = hpo["hidden_units"]
    optimizer = hpo["optimizer"]
    print(units, optimizer)
    data = {"ref": "main", "inputs": {"units": str(units), "optimizer": optimizer}}
    # data = {"ref": "main", "inputs":{"model_path": model_path, "model_tag": model_tag }}
    res = requests.post(
        f"https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows/{WORKFLOW_ID}/dispatches",
        headers=headers,
        data=json.dumps(data),
    )
    print(res.text)
    print(res.status_code)


if __name__ == "__main__":
    hpo = {"hidden_units": 64, "optimizer": "adam"}
    call_dispatcher(hpo)
