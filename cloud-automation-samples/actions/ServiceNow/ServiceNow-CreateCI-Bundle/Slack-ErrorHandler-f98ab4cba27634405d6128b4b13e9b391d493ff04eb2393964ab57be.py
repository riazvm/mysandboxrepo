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

def handler(context, inputs):

    errorMsg = inputs["errorMsg"]
    flowInputs = inputs["flowInputs"]
    print("Flow execution failed with error {0}".format(errorMsg))
    print("Flow inputs were: {0}".format(flowInputs))
    
    
    url = "https://slack.com/api/chat.postMessage"
    headers = {'Content-Type': 'application/json; charset=utf-8', 
               'Accept': 'application/json',
               'Authorization': 'Bearer ' + inputs['auth_token'] # Auth Token for Slack App Bot or User
               }
    payload = {
            'channel': inputs['channel'], # Slack user or channel, where you want to send the message
            #'thread_ts': inputs['slackThread'],
            'attachments': [
                {
                    'fallback': inputs['message'] + "action flow execution failed with error {0}".format(errorMsg),
                    'color': inputs['colorHex'],
                    'title': inputs['messageHeading'],
                    'text': inputs['message'] + " action flow execution failed with error {0}".format(errorMsg)
                    #'ts': inputs['slackThread'] 
                }
            ]
        }
    
    results = requests.post(
        url,
        json=payload,
        headers=headers,
    )
    print(results.text)
    
    outputs = {
        "errorMsg": errorMsg,
        "flowInputs": flowInputs
    }
    return outputs