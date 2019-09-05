<!--
#
# VMware Tito Application Sample
# Author Vincent Meoc  - vmeoc@vmware.com
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
-->
<?php

// Get the request method
$method = getMethod();
// Set the header to application/json
header('Content-Type: application/json');

try {
    // Switch the base URL
    switch(getBaseUrl()){
        case "/traffic": {
            // include script to get data
            include 'getTrafficData.php';
            // Render JSON response with the result data
            renderJsonResponse($result);
            break;
        }
        default: {
            // No function found for the given base URL
            throw new \Exception("API function not found.", 404);
        }
    }
    
} catch (Exception $ex) {
    // Render JSON error response with the exception data
    renderJsonResponse(array("error" => array("message"=>$ex->getMessage(), "code" => $ex->getCode())));
}
exit(0);

/**
 * Get the request method
 * Return GET, POST, DELETE or PUT
 * 
 * @return string
 */
function getMethod() {
    return strtoupper($_SERVER['REQUEST_METHOD']);
}
/**
 * Get the base URL without the script name and jquery params
 * 
 * @return string
 */
function getBaseUrl(){
    $url = str_replace($_SERVER['SCRIPT_NAME'], "", $_SERVER['REQUEST_URI']);
    return explode("?", $url)[0];
}
/**
 * Get a JSON string from the $data array
 * 
 * @param array $data
 * @return string
 */
function renderJsonResponse(array $data = array()) {
    $data['request_time'] = time();
    echo json_encode($data);
}
