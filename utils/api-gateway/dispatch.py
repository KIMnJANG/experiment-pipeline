import os
import requests
import json


TOKEN = os.environ.get("GITHUB_TOKEN")
OWNER = "KIMnJANG"
REPO = "mlops_mnist"

headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {TOKEN}",
}


def call_dispatcher(hpo):
    units = hpo["hidden_units"]
    optimizer = hpo["optimizer"]
    data = {"ref": "main", "inputs": {"units": units, "optimizer": optimizer}}

    res = requests.post(
        f"https://api.github.com/repos/{OWNER}/{REPO}/dispatches",
        data=json.dumps(data),
        headers=headers,
    )
    print(res.text)
    print(res.status_code)
