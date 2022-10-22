import boto3
import cfnresponse
import os
import datetime


def lambda_handler(event, context):
    try:
        boto3.setup_default_session(region_name='ap-northeast-2')
        client = boto3.client('cognito-idp', region_name='ap-northeast-2')
        ssm = boto3.client('ssm')
        client_id = ssm.get_parameter(Name='/demogo-multitenancy/auth/user-pool-client-id', WithDecryption=False)['Parameter']['Value']
        UserPoolId = ssm.get_parameter(Name='/demogo-multitenancy/auth/user-pool-id', WithDecryption=False)['Parameter']['Value']
        
        client.add_custom_attributes(
            UserPoolId=UserPoolId,
            CustomAttributes=[
                {
                    'Name': 'tier',
                    'AttributeDataType': 'String',
                    'Mutable': False
                },
                {
                    'Name': 'apartment_id',
                    'AttributeDataType': 'String',
                    'Mutable': False
                }
            ]
        )

        response = client.sign_up(
                    ClientId=client_id,
                    Username='penguin@amazon.com',
                    Password='12345dgda67',
                    UserAttributes=[
                            {
                                'Name': 'custom:tier',
                                'Value': 'premium'
                            },
                            {
                                'Name': 'custom:apartment_id',
                                'Value': 'a'                            
                            }
                                    ],
                        )
        resp = client.admin_confirm_sign_up(UserPoolId=UserPoolId,
                                        Username='penguin@amazon.com')
        
        response = client.sign_up(
                    ClientId=client_id,
                    Username='apple@amazon.com',
                    Password='12345dgda67',
                    UserAttributes=[
                            {
                                'Name': 'custom:tier',
                                'Value': 'standard'
                            },
                            {
                                'Name': 'custom:apartment_id',
                                'Value': 'a'                            
                            }
                                    ],
                        )
        resp = client.admin_confirm_sign_up(UserPoolId=UserPoolId,
                                        Username='apple@amazon.com')
        cfnresponse.send(event, context, cfnresponse.SUCCESS,{})
    except Exception as e:
        print(e)
        cfnresponse.send(event, context, cfnresponse.FAILED, {})
