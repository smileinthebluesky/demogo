from flask import Flask,render_template,request,make_response,redirect,jsonify
from flask_restx import Api,Resource
import requests
import boto3
import json
import os
from boto3.dynamodb.conditions import Key

app = Flask(__name__)
api = Api(app)

ClientId = os.environ.get("clientId")
url = os.environ.get("requests")
tablename = os.environ.get("table")

boto3.setup_default_session(region_name='ap-northeast-2')
client = boto3.client('cognito-idp', region_name='ap-northeast-2')
dynamodb = boto3.resource('dynamodb',endpoint_url='http://dynamodb.ap-northeast-2.amazonaws.com')
table = dynamodb.Table(tablename)

@api.route('/index')
class Index(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('login.html'),200,headers)

@api.route('/login')
class Login(Resource):
    def post(self):

        req = request.get_json()
        id = req['id']
        password = req['password']

        response = client.initiate_auth(
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={ 'USERNAME': id, 'PASSWORD': password },
        ClientId=ClientId)

        token = response['AuthenticationResult']['AccessToken']
        response = jsonify({'token':token})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

# 본인 아파트 정보 불러오기 
@api.route('/getapartment')
class Getapartment(Resource):
    def get(self):

            token = request.args.get('token')

            # 토큰으로 cognito에서 티어 받아오기
            response = client.get_user(AccessToken=token)

            # 티어와 롤을 조합해서 opa를 통해 가능한지를 판단하고, 서비스 배치
            attr = response['UserAttributes']
            
            apart_id = attr['Name'=='custom:apartment_id']['Value']
            tier = attr[3]['Value']
            data = {
            "tier": tier,
            "role": "viewApts"
            }
            headers = {
            'content-type': 'application/json',
            }
            res = requests.post(url, headers=headers,data=json.dumps(data))
            role_yn = str(res.json()['result'])

            query = {"KeyConditionExpression": Key("apartment_id").eq('a')}
            data = table.query(**query)['Items']

            if role_yn == 'False':
                list = data
            else:
                list = table.scan()['Items']
                for i in list:
                    i = json.dumps(i)

            # 고객 정보를 넣어서 html 렌더링
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('main.html',list=list, data=data[0]),200,headers)


if __name__ == '__main__':
    app.run(debug=False, port=5000)

