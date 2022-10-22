# demogo - OPA와 SAM/CF를 이용한 Multi-Tenancy 서비스 구축

###  [OPA](https://www.openpolicyagent.org/) 는 Open Policy Agent의 약자로 서비스를 할 때에 필수적인 policy를 code화 해서 따로 서버를 운영하며, 이를 통해 서비스와 policy를 분리할 수 있게 해주는 Agent입니다. 다양한 분야에서 이용할 수 있지만, 여기에서는 OPA를 통해서 Multi-Tenancy를 구축하는 것에 대해서 다루어 보려고 합니다. 

#### Lee Real Estate 서비스는 부동산 서비스로, 유주택자에게 어떤 아파트로 갈아타는 것이 좋을지에 대한 가이드를 제시합니다. 단, 프리미엄 고객에게만요. Multi-Tenancy로 분리되어 있는 일반 고객과 프리미엄 고객에게는 tier에 따라 다른 서비스를 제공하게 되는데요, OPA를 통해서 이를 간단하게 만들 수 있습니다. 이제 이를 조금의 시간을 들여서 만들어 볼 것입니다.

####  구성하게 되면 다음과 같은 아키텍쳐가 생성됩니다. 도커 이미지를 ECR에 올리는 것 외에는 모든 것이 SAM과 CF를 통해 자동화되어 있습니다! 
<img src="arch.jpeg">

####  계속 진행하기 위해서는 다음의 임무를 완수해야 합니다. 임무들을 완성하면 나중에도 도움이 될 겁니다. 

##### [AWS CLI 설치](https://docs.aws.amazon.com/ko_kr/cli/latest/userguide/getting-started-install.html)
##### [Git 설치](https://github.com/git-guides/install-git)
##### [Docker 설치](https://docs.docker.com/get-docker/)
##### [SAM 설치](https://docs.aws.amazon.com/ko_kr/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
##### [Python 3.9 버젼 설치](https://www.python.org/downloads/release/python-3915/)

#### 임무를 완료했으면, 서비스를 만들 소스를 GitHub에서 받아옵니다. 
