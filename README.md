## Experiment Pipeline

```bash
.
├── .github
│   └── workflows
│       └── cd.yml
├── README.md
├── experiment
│   ├── base
│   │   ├── katib-experiment.yaml
│   │   ├── kustomization.yaml
│   │   └── slack-alert.yaml
│   └── overlays
│       └── dev
│           └── kustomization.yaml
└── gateway
    ├── gateway-deployment.yaml
    └── gateway-service.yaml
```

- `katib-experiment.yaml` <br/>
    Katib를 통한 Hyper Parameter Tuning을 진행합니다. [mnist-model](https://github.com/Ssuwani/mnist-model)에서 생성한 이미지를 바탕으로 Experiment 리소스를 정의합니다.
- `base/kustomization.yaml` <br/>
    kustomize를 통해 오브젝트를 관리할 리소스를 정의합니다.
- `slack-alert.yaml`<br/>
    Katib-Experiment의 종료를 모니터링합니다. 실험이 종료되면 Slack을 통해 실험에 관련된 정보를 알립니다.
- `overlays/dev/kustomization.yaml`<br/>
    이미지 태그 및 실험명 등, 실험에 관련된 변경 사항들을 관리합니다. 
- `gateway-deployment.yaml`<br/>
    slack-alert을 통해 Slack으로 실험관련 정보가 전달될 때 슬랙에서 사용할 수 있는 Slash Command가 함께 전달됩니다. [Slash Command](https://api.slack.com/interactivity/slash-commands)는 Deploy-Pipeline의 Worflow를 실행하기 위함인데 이를 연결해주는 게이트웨이입니다. Flask를 이용해 작성하였습니다.
- `gateway-service.yaml`<br/>
    방금 정의한 deployment를 외부로 노출합니다. LoadBalancer Type를 사용해 정의했습니다.
- `.github/workflows/cd.yml` <br/>[mnist-model](https://github.com/Ssuwani/mnist-model)으로부터 실행되기 위해 Dispatch 방식으로 정의하였습니다. 태그로서 정의된 버전정보를 받아와 `experiment/overlays/dev/kustomization.yaml` 파일을 업데이트합니다. 



현재의 레포지토리는 Experiment와 Gateway 각각의 폴더를 ArgoCD를 통해 배포됩니다. 