import json
import boto3
import cfnresponse

def lambda_handler(event, context):
    try:  
        boto3.setup_default_session(region_name='ap-northeast-2')
        dynamodb = boto3.resource('dynamodb',endpoint_url='http://dynamodb.ap-northeast-2.amazonaws.com')
        ssm = boto3.client('ssm')
        table_name = ssm.get_parameter(Name='/demogo-multitenancy/table', WithDecryption=False)['Parameter']['Value']
        table = dynamodb.Table(table_name)
        
        with table.batch_writer() as batch:
            batch.put_item(
                    Item = {
                        'apart_id':'Songpa happycity apartment',
                        'apartment_id':'a',
                        'jan':'700',
                        'Feb':'720',
                        'Mar':'710',
                        'Apr':'700',
                        'May':'690',
                        'Jun':'715',
                        'Jul':'730',
                        'Aug':'720',
                        'Sep':'720'
                    }
                )
            batch.put_item(
                    Item = {
                        'apart_id':'Mapo today apartment',
                        'apartment_id':'b',
                        'jan':'650',
                        'Feb':'660',
                        'Mar':'670',
                        'Apr':'680',
                        'May':'690',
                        'Jun':'700',
                        'Jul':'710',
                        'Aug':'720',
                        'Sep':'760'
                    }
                )
            batch.put_item(
                    Item = {
                        'apart_id':'Yeouido largepark apartment',
                        'apartment_id':'c',
                        'jan':'790',
                        'Feb':'800',
                        'Mar':'750',
                        'Apr':'710',
                        'May':'750',
                        'Jun':'740',
                        'Jul':'760',
                        'Aug':'800',
                        'Sep':'700'
                    }
                )
            batch.put_item(
                    Item = {
                        'apart_id':'Mokdong baseball apartment',
                        'apartment_id':'d',
                        'jan':'740',
                        'Feb':'730',
                        'Mar':'720',
                        'Apr':'730',
                        'May':'750',
                        'Jun':'740',
                        'Jul':'760',
                        'Aug':'720',
                        'Sep':'700'
                    }
                )

        cfnresponse.send(event, context, cfnresponse.SUCCESS,{})
    except Exception as e:
        print(e)
        cfnresponse.send(event, context, cfnresponse.FAILED, {})
