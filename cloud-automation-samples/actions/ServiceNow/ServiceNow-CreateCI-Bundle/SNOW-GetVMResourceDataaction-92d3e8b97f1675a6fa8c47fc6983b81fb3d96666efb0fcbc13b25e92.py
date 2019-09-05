#
# VMware Cloud Automation Actions Sample
#
# Copyright 2019 VMware, Inc. All rights reserved
#
# The BSD-2 license (the "License") set forth below applies to all parts of the
# Cloud-automation-samples Code project. You may not use this file except in compliance
# with the License.
#
# BSD-2 License
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
# 
# Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
from botocore.vendored import requests
import json
#import boto3 ## For SSM
#client = boto3.client('ssm','ap-southeast-2')

def handler(context, inputs):
    baseUri = inputs['url']
    #casToken = client.get_parameter(Name="casToken",WithDecryption=True) For AWS SSM
    casToken = inputs['casToken']
    url = baseUri + "/iaas/login"
    headers = {"Accept":"application/json","Content-Type":"application/json"}
    #payload = {"refreshToken":casToken['Parameter']['Value']} ## if using AWS SSM
    payload = {"refreshToken":casToken}
    
    results = requests.post(url,json=payload,headers=headers)
    
    bearer = "Bearer "
    bearer = bearer + results.json()["token"]
    
    deploymentId = inputs['deploymentId']
    resourceId = inputs['resourceIds'][0]
    
    print("deploymentId: "+ deploymentId)
    print("resourceId:" + resourceId)
    
    machineUri = baseUri + "/iaas/machines/" + resourceId
    headers = {"Accept":"application/json","Content-Type":"application/json", "Authorization":bearer }
    resultMachine = requests.get(machineUri,headers=headers)
    print("machine: " + resultMachine.text)
    
    print( "serviceNowCPUCount: "+ json.loads(resultMachine.text)["customProperties"]["cpuCount"] )
    print( "serviceNowMemoryInMB: "+ json.loads(resultMachine.text)["customProperties"]["memoryInMB"] )
    
    #update customProperties for use in action flow
    outputs = {
        "cpuCount": int(json.loads(resultMachine.text)["customProperties"]["cpuCount"]),
        "memoryInMB": json.loads(resultMachine.text)["customProperties"]["memoryInMB"]
    }
    return outputs