from flask import Flask, request
from dispatch import call_dispatcher

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to api gateway"

@app.route("/run_deploy_pipeline", methods=["POST"])
def run_deploy_pipepline():
    data = request.form.get("text")
    # print(data)
    data = {info.split("-")[0]: info.split("-")[1] for info in data.split()}
    print("data: ", data)
    call_dispatcher(data)
    return f"배포 파이프라인이 실행되었습니다.\n https://github.com/ssuwani/deploy-pipeline/actions\n 실행된 하이퍼 파라미터: {data}"


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
