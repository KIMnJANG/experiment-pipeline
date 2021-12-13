from kubeflow import katib
import os
import requests
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--exp_name", default="katib-experiment-0028")
    parser.add_argument("--namespace", default="ep")

    args = parser.parse_args()
    return args


def waiting_experiment_end(exp_name, namespace):
    while True:
        try:
            status = client.get_experiment_status(exp_name, namespace=namespace)
            print(status)  # Running or Successed
            if status == "Succeeded":
                return True
        except:
            print("not started")


def send_message_to_slack(exp_name, namespace):
    exp = client.get_experiment(exp_name, namespace=namespace)
    metrics = exp["status"]["currentOptimalTrial"]["observation"]
    args = exp["status"]["currentOptimalTrial"]["parameterAssignments"]

    acc = metrics["metrics"][0]["latest"]
    loss = metrics["metrics"][1]["latest"]
    url = os.getenv("SLACK_WEBHOOK")
    payload = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"학습이 종료되었습니다.\n 실험명: {exp_name}",
                    "emoji": True,
                },
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Best acc:*\n{acc}"},
                    {"type": "mrkdwn", "text": f"*Best loss:*\n{loss}"},
                ],
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*{arg['name']}:*\n{arg['value']}"}
                    for arg in args
                ],
            },
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "배포 파이프라인을 실행하려면 다음 명령어를 입력하세요\n/run_deploy_pipeline optimizer-{optimizer} hidden_units-{hidden_units}",
                    "emoji": True,
                },
            },
        ],
    }

    response = requests.post(url, json=payload)
    print(response.text)


if __name__ == "__main__":
    args = get_args()
    client = katib.KatibClient()
    success = waiting_experiment_end(args.exp_name, args.namespace)
    if success:
        send_message_to_slack(args.exp_name, args.namespace)
