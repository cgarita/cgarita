<?php	
	$cod = $_GET['codigo'];
	
	// datos para la conexion a mysql
	
	define('DB_SERVER','10.10.128.10'); // servidor
	define('DB_NAME','sentidos');	 // nombre de la Base de Datos
	define('DB_USER','sentidos');		 // nombre del usuario mysql
	define('DB_PASS','OvsSen');		 // clave de usuario mysql
	
	/*
	define('DB_SERVER','localhost'); // servidor
	define('DB_NAME','sentidos');	 // nombre de la Base de Datos
	define('DB_USER','root');		 // nombre del usuario mysql
	define('DB_PASS','root');		 // clave de usuario mysql
	*/
	$con = mysql_connect(DB_SERVER,DB_USER,DB_PASS);
	mysql_select_db(DB_NAME,$con);
	
	if(!$con){
		echo "No se ha podido conectar a la base de datos!";
		exit; 
	}
  
	  mysql_select_db("sentidos");
	  
	  $consulta = "SELECT * FROM t_sentidos WHERE codigo = $cod;";
	  $resultado = mysql_query($consulta);
	  
	  $num_resul = mysql_num_rows($resultado);
	  
	//for($i=0; $i<$num_resul; $i++) {
		$row = mysql_fetch_array($resultado);
		$id = $row['codigo'];
		$coord1 = $row['latitud'];
		$coord2 = $row['longitud'];
		
		$tabla  ="<table border=0><tr><td width=120><h2><img src=img/logo.jpg></h2></td></tr>"; 
		$tabla .= "<tr bgcolor=#DEDEEF><td width=90>Fecha:</td> <td>$row[fecha]</td></tr>";
		$tabla .= "<tr><td width=90>Hora:</td> <td>$row[hora]</td></tr>";
		$tabla .= "<tr bgcolor=#DEDEEF><td width=90>Origen:</td> <td>$row[origen]</td></tr>";
		$tabla .= "<tr><td width=90>Profundidad:</td> <td>$row[profundidad]</td></tr>";
		$tabla .= "<tr bgcolor=#DEDEEF><td width=90>Magnitud:</td> <td>$row[magnitud]</td></tr>";
		$tabla .= "<tr><td width=90>Reportado:</td> <td>$row[reportado]</td></tr>";
		$tabla .= "<tr bgcolor=#DEDEEF><td width=90>Localizacion:</td> <td>$row[localizacion]</td></tr>";
		$tabla .= "<tr><td width=90>Latitud:</td> <td>$row[latitud]</td></tr>";
		$tabla .= "<tr bgcolor=#DEDEEF><td width=90>Longitud:</td> <td>$row[longitud]</td></tr>";
		$tabla .= "<tr></table>";
	//}
?>

<html xmlns="http://www.w3.org/1999/xhtml">
	
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>SISMO SENTIDO</title>
    <style>
    *{ margin: 0; padding: 0; }
		html, body, #map{
        width: 100%;
        height: 98%;
    }
    </style>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false&amp;language=es"></script>
    
    <script type="text/javascript">
		window.onload = function(){
			coord1 = "<?php echo $coord1; ?>";
			coord2 = "<?php echo $coord2; ?>";
			
			tabla = "<?php echo $tabla; ?>";

			var options = {
				zoom: 9
				, center: new google.maps.LatLng(coord1, coord2)
				, mapTypeId: google.maps.MapTypeId.ROADMAP
			};
		 
			var map = new google.maps.Map(document.getElementById('map'), options);
		 
			var marker = new google.maps.Marker({
				position: map.getCenter()
				, map: map
				, title: 'Pulsa aquí para ver detalles del sismo!'
				, icon: 'http://gmaps-samples.googlecode.com/svn/trunk/markers/orange/blank.png'
			});
		 
			var popup = new google.maps.InfoWindow({
				content: tabla
			});
		 
			google.maps.event.addListener(marker, 'click', function(){
				popup.open(map, marker);
			});
		};
		function cerrarVentana()
		{
			window.close();
		};   
    </script>
</head>
<body>
    <div id="map"></div>
    
    <input  type="button" value="Cerrar" name="cerrar" class="botoon" onClick="cerrarVentana()">
</body>
</html>
