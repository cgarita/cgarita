<?php

// Put your device token here (without spaces):
//$deviceToken = '6cdf6b0d7cefe416cf2a8e83bd04026e5f95d4c7fecd6f6d83b4aa46603905af';
//$deviceToken = 'b2fc452ceb264e594f6261bcf1a4126515bf5e1ee755069503980794b2e529ff';
$deviceToken = '7a3745cb8c01737373708366a2298a31238edc08c66b3ebc29aeb1a39097b3f4';


// Put your private key's passphrase here:
$passphrase = 'epicentro';

// Put your alert message here:
$message = 'Test desde ovsicori';

////////////////////////////////////////////////////////////////////////////////

$ctx = stream_context_create();
stream_context_set_option($ctx, 'ssl', 'local_cert', 'production/ck.pem');
stream_context_set_option($ctx, 'ssl', 'passphrase', $passphrase);

// Open a connection to the APNS server
$fp = stream_socket_client(
	'ssl://gateway.push.apple.com:2195', $err,
	$errstr, 60, STREAM_CLIENT_CONNECT|STREAM_CLIENT_PERSISTENT, $ctx);

if (!$fp)
	exit("Failed to connect: $err $errstr" . PHP_EOL);

echo 'Connected to APNS' . PHP_EOL;

// Create the payload body
$body['aps'] = array(
	'alert' => $message,
	'sound' => 'default'
	);

// Encode the payload as JSON
$payload = json_encode($body);

// Build the binary notification
$msg = chr(0) . pack('n', 32) . pack('H*', $deviceToken) . pack('n', strlen($payload)) . $payload;

// Send it to the server
$result = fwrite($fp, $msg, strlen($msg));

if (!$result)
	echo 'Message not delivered' . PHP_EOL;
else
	echo 'Message successfully delivered' . PHP_EOL;

// Close the connection to the server
fclose($fp);
