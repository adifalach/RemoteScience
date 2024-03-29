import json
import boto3
import logging
import time
 
logger = logging.getLogger()
logger.setLevel(logging.INFO)
 
client = boto3.client('iot-data')
 
def lambda_handler(event, context):
    body = event['body'] # this is a request from the website, we update ths shadow accordingly
    body = json.loads(body)
    
    THINGNAME=body['thingname']
    if (THINGNAME == ""):
        print("No Thing Name found. Setting Thing Name = RemoteSciencePi")
        THINGNAME="RemoteSciencePi"
        
    #result = asyncio.run(async_handler(event,context))
    if body['action'] == "start": # start experiment + parameters
        # requested experiment params
        length = body['length']
        angle = body['angle']
        
        #first- reset:
        payload = json.dumps({'state': { 'desired': { 'action': 'start', 'length': "-1", 'angle': "-1", 'result': '-' } }})
        response = client.update_thing_shadow(
            thingName=THINGNAME,
            payload=payload
        )
        time.sleep(1)
        # send actual parameters
        payload = json.dumps({'state': { 'desired': { 'action': 'start', 'length': length, 'angle': angle, 'result': '-' } }})
        
        logger.info("Attempting to Update Shadow State to START EXPERIMENT")
        response = client.update_thing_shadow(
            thingName=THINGNAME,
            payload=payload
        )
    
        logger.info("IOT Shadow Updated")
        
    else: # stop experiment - FUTURE FEATURE.
        payload = json.dumps({'state': { 'desired': { 'action': 'stop', 'length': '-', 'angle': '-', 'result': '-' } }})
        
        logger.info("Attempting to Update Shadow State to STOP EXPERIMENT")
        response = client.update_thing_shadow(
            thingName=THINGNAME,
            payload=payload
        )
        logger.info("IOT Shadow Updated")
        
    return {
        'statusCode': 200,
        "headers": {
            'Access-Control-Allow-Origin':'*',
            'Access-Control-Allow-Headers':'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods':'GET,OPTIONS'
        },
        'body': json.dumps('Shadow Updated!')
    }
   