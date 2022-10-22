# OPA와 SAM/CF를 이용한 Multi-Tenancy 서비스 구축

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
```bash
mkdir opa-service
cd opa-service
git clone https://github.com/smileinthebluesky/demogo.git
```

#### 잘 받아왔으면, Dockerfile을 이용해서 docker image를 생성합니다. 이때, docker가 running하는 상태여야 합니다.
```bash
cd demogo
docker build -t opa-service:latest . 
```
#### 시간이 조금 걸릴 수 있습니다. 차분히 기다립니다. Dockerfile이 있는 위치에서 docker build를 사용하셔야 합니다. 뒤에 . 도 잊지마세요! 완성되면 다음 명령어를 통해 이미지 생성을 확인합니다.
```bash
docker images
```

#### AWS Image Repository인 ECR에 로그인하고, Repository를 만듭니다.
```bash
aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 계정번호.dkr.ecr.ap-northeast-2.amazonaws.com
aws ecr create-repository --repository-name opaservice --region ap-northeast-2
```

#### 이제 docker image에 tagging을 하고, 아까 만든 repository로 이미지를 push합니다. 
```bash
docker tag opa-service:latest 계정번호.dkr.ecr.ap-northeast-2.amazonaws.com/opaservice:latest
docker push 계정번호.dkr.ecr.ap-northeast-2.amazonaws.com/opaservice:latest
```

#### [ECR](https://ap-northeast-2.console.aws.amazon.com/ecr/repositories?region=ap-northeast-2)에 접속해서 방금 만든 opaservice repository에 들어갑니다. Image URI 항목 아래의 Copy URI 를 눌러 URI를 카피해서 메모장에 저장합니다.
<img src="ecr.jpg">

#### 이제 본격적으로 서비스 빌드를 해보겠습니다. /demogo/demogo-multitenancy 경로에 있는 api.yaml 파일을 IDE로 오픈하고, 아래의 'here' 부분 (16번째 줄) 을 아까 저장했던 URI 로 치환합니다.
```
ContainerDefinitions:
        - Name: web
          Essential: true
          Image: here
          PortMappings:
            - ContainerPort: 80
              HostPort: 80
              Protocol: tcp
```

#### 바꿨으면 저장하고 /demogo/demogo-multitenancy 로 다시 되돌아 옵니다. 그리고 아래 명령어를 수행합니다. [SAM](https://docs.aws.amazon.com/ko_kr/serverless-application-model/latest/developerguide/what-is-sam.html) 은 다양한 기능들을 사용해 손쉽게 application을 구축할 수 있게 도와주는 다람쥐 서비스입니다.

```bash
sam build
sam deploy --guided --stack-name opa-service --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND
```

#### Deploy를 할때의 선택지는 아래를 참고하세요. 마지막 선택지까지 고르면 잠시 멈춘듯한 현상이 있는데 지극히 정상이니 걱정하지 마세요.
<img src="sam.jpg">

#### 완료되면 다음과 같이 보입니다. 이제 마음껏 서비스를 이용할 수 있습니다. 초기 데이터 적재와 초기 유저는 모두 생성되어 있습니다.
<img src="done.jpg">

#### [ECS](https://ap-northeast-2.console.aws.amazon.com/ecs/home?region=ap-northeast-2#/clusters) 콘솔로 들어가면, CFNCluster가 만들어져 있을 것입니다. Service가 있는 것을 확인하고, CFNCluster를 클릭해서 메뉴로 들어갑니다. 들어가서 Services 탭 > Service Name 탭 아래의 cfn-service 클릭 > Task 탭 선택 후, 아래의 Task 탭 아래의 Task 명 선택 > Public IP 찾아서 복사 하는 과정을 거칩니다.  그 다음, 아래의 주소로 들어갑니다. 화면이 성공적으로 호출됩니다.

```
http://publicIp/index
```
<img src="main.jpg">

#### 현재 서비스에서는 일반 회원인 apple과 프리미엄 회원인 penguin이 이미 가입되어 있습니다. 아래의 정보를 입력해서 로그인해보세요. 이상한 값을 넣으면 에러로 떨어집니다. 

|ID|Password|
|------|---|
|penguin@amazon.com|12345dgda67|
|apple@amazon.com|12345dgda67|

#### 프리미엄 회원인 penguin은 아래의 서비스를 누릴 수 있습니다. 자신의 아파트와 비슷한 대조군의 아파트가 보여지며, 가격 추세도 한 눈에 볼 수 있습니다.
<img src="penguin.jpg">

#### 일반 회원인 apple은 다소 밋밋한 화면만을 보게 되네요. 서비스를 좀 더 확장하면 차이는 보다 커지겠죠?
<img src="apple.jpg">
