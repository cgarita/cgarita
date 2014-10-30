<?php
	//db connections
	function db_connect() {
		
		$hostname = "EpicentroDB.db.8006053.hostedresource.com";
		$username = "EpicentroDB";
		$database = "EpicentroDB";
		$password = "Rocket123!";
		
		//$hostname = "localhost";
//		$username = "root";
//		$database = "EpicentroDB";
//		$password = "root";
	
		$$link = 0;
	
		if (USE_PCONNECT == 'true') {
			$$link = mysql_pconnect($hostname, $username, $password);
		} else {
			$$link = mysql_connect($hostname, $username, $password);
		}
	
		if ($$link)
			mysql_select_db($database);
		return $$link;
	}
	
	function db_query($query_string) {
		$result = mysql_query($query_string) or die(mysql_error());
		return $result;
	}
	//connect 
	db_connect () or die ( 'Unable to connect to database server!' );
	
	$success = false;
	$success = pushAndroid();
	$success = pushIphone();
	
	if ($success)
	{	
		//header('Location:notifications.php?sent=Mensaje enviado exitosamente.');
	}
	else
	{	
		//header('Location:notifications.php?sent=Intente de nuevo.');
	}
	function pushAndroid()
	{
		$message = $_GET['pushMessage'];
		$result = db_query("SELECT UDID FROM demo_android");
		
		$arrayRegs = array();
		while ($row = mysql_fetch_array($result, MYSQL_NUM)) {
			$arrayRegs[] = $row[0];
		}
		if (mysql_num_rows($result) > 0) {
			$url = 'https://android.googleapis.com/gcm/send';
			$fields = array('registration_ids' => $arrayRegs, 'data' => array("msg" => $message));
			$headers = array('Authorization: key=AIzaSyCwZKidtUCOsobDNlfTPigE2voiZ4y_Ifo', 'Content-Type: application/json');
			// Open connection
			$ch = curl_init();

			// Set the url, number of POST vars, POST data
			curl_setopt($ch, CURLOPT_URL, $url);

			curl_setopt($ch, CURLOPT_POST, true);
			curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
			curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

			// Disabling SSL Certificate support temporarly
			curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);

			curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($fields));

			// Execute post
			$result = curl_exec($ch);
			if ($result === FALSE) {
				die('Curl failed: ' . curl_error($ch));
			}
			// Close connection
			curl_close($ch);
			return true;
		}
	}
	function pushIphone() {
		$message = $_GET['pushMessage'];
		$result = db_query("SELECT UDID FROM demo_ios");
		if (mysql_num_rows($result) > 0) {
			while ($row = mysql_fetch_array($result)) {
				$success = sendMessage($message, $row['UDID']);
			}
			return $success;
		} else {
			//header('Location: notifications.php?sent=No hay tokens registrados.');
		}
	
	}
	function sendMessage($message, $deviceToken) {
		$passphrase = 'epicentro';
		$ctx = stream_context_create();
		stream_context_set_option($ctx, 'ssl', 'local_cert', 'ck.pem');
		stream_context_set_option($ctx, 'ssl', 'passphrase', $passphrase);
		
		// Open a connection to the APNS server
		$fp = stream_socket_client(
			'ssl://gateway.push.apple.com:2195', $err,
			$errstr, 60, STREAM_CLIENT_CONNECT|STREAM_CLIENT_PERSISTENT, $ctx);
		
		if (!$fp)
			exit("Failed to connect: $err $errstr" . PHP_EOL);
				
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
		
		
		// Close the connection to the server
		fclose($fp);
		if (!$result)
			return false;
		else
			return true;
		
	}
?>