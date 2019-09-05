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

/* Create a TCP/IP socket. */
$wf_proxy_name="127.0.0.1";
$wf_proxy_port=2878;
$metric_name="vince1706.test3.metric";
$metric_value="100";
$metric_epoch="1523021479";
$source_name="vince-France";
$tag_name="test1";
$tag_value="060418";


$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
if ($socket === false) {
    echo "socket_create() failed: reason: " . socket_strerror(socket_last_error()) . "\n";
} else {
    echo "OK.\n";
}
echo "Attempting to connect to ‘$wf_proxy_name' on port ‘$wf_proxy_port'...";
$result = socket_connect($socket, $wf_proxy_name, $wf_proxy_port);
if ($result === false) {
    echo "socket_connect() failed.\nReason: ($result) " . socket_strerror(socket_last_error($socket)) . "\n";
} else {
    echo "OK.\n";
}
$data_point = "$metric_name $metric_value $metric_epoch source=$source_name  $tag_name=$tag_value\n";
echo "Sending Wavefront Data point";
socket_write($socket, $data_point, strlen($data_point));
echo "Closing socket...";
socket_close($socket);

?>
