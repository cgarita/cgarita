<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"> 
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<meta name="description" content="Obvservatorio Vulcanol&oacute;gico y Sismol&oacute;gico de Costa Rica" />
<meta name="keywords" content="sismologa, vulcanologa, sismogram&aacute;s en lnea, procesos tectnicos, sismos, red sismogrfica,gases volcanicos, volcanes de Costa Rica, OVSICORI" />
<meta name="Mauricio Moreira Guzmn" content="Mauricio Moreira / Original design: Programa UNAWEB- http://www.una.ac.cr/" />
<!--<link rel="stylesheet" type="text/css" href="../ssentido/css/infogeneral.css" media="screen" title="andreas02 (screen)" />
<link rel="stylesheet" type="text/css" href="../ssentido/css/print.css" media="print" />-->
<title>Sismos Registrados Automaticamente</title>
<!--<link href="css/estilo.css" rel="stylesheet" type="text/css" /> -->
</head>
<body>
<div id="container">
<br /><p><?

?></p><br />  	
    <?php
    echo '
    <script src="http://maps.google.com/maps?file=api&amp;v=2&amp;key=ABQIAAAAI9aXBwH5jwQW94RTNmR6_xTPis6MQoBTzH8WCkXbbeHqEFQqbxScQW2oU_Sm4QrbWRSfFFnjrnKoWA"
      type="text/javascript"></script>
    <script type="text/javascript">

    //<![CDATA[

    function load() {
      if (GBrowserIsCompatible()) {
        var map = new GMap2(document.getElementById("map"));
	//map.setWidth(700);
	//map.setHeight(550);
	//map.setZoomFactor(8);
	map.setCenter(new GLatLng(9.5775775, -84.2788775), 8);
        map.addControl(new GMapTypeControl());
        map.addControl(new GLargeMapControl());
        map.addControl(new GScaleControl());
	//map.setMapType(G_SATELLITE_MAP);
      }

      function addtag(point, address) {
           var marca = new GMarker(point);
           GEvent.addListener(marca ,"mouseover",function(){marca.openInfoWindowHtml(address);});
           return marca;
        } 
	function createMarker(point, icon, tag) {
  	      var marker = new GMarker(point, icon);
	      GEvent.addListener(marker, "click", function() {
             marker.openInfoWindowHtml(tag);
      });
      return marker;
    }';	


    /***********************************Recupera los datos del ult registro insertado*********************/
    include "conexion.php";
    $fecha=($_GET['fecha']);
    $hora=($_GET['hora']);
    $query="SELECT * FROM eqs where fechalocal = '".$fecha."' AND horalocal = '".$hora."'";
    $result=mysql_query($query);

    $registro=mysql_fetch_assoc($result);
        $latitud= $registro['latitud'];
        $longitud= $registro['longitud'];
	$fecha= $registro['fechalocal'];
	$hora= $registro['horalocal'];
	$magnitud= $registro['magnitud'];
        //$origen= $registro['origen'];
        //$reportado= $registro['reportado'];
        $profundidad = $registro['profundidad'];
	$localizacion= $registro['localizacion'];

/***********************************************************************************************/

/*************************Inserta la marca con los datos recuperados****************************/

  if ($magnitud <= 3.5){
   	  echo '      var x="'.$latitud.'";
               var y="'.$longitud.'";
	       var icono = new GIcon(G_DEFAULT_ICON);
 	       icono.image = "../../images/stories/OVSICORI//sismoverde.png";
	       var tamanoIcono = new GSize(20,20);
               icono.iconSize = tamanoIcono;
		icono.shadowSize = new GSize(0, 0);
               address = "Fecha:'.$fecha.'"+ "<br />";
  	       address = address + "Hora:'.$hora.'"+ "<br />";	
	       address = address + "Magnitud: '.$magnitud.'"+ "<br />";
	       address = address + "Profundidad en km: '.$profundidad.'"+ "<br />";
	       address = address + "Localizacion: '.$localizacion.'"+ "<br />";
	       var point = new GLatLng('.$latitud.', '.$longitud.');
               var marker = createMarker(point,icono,address);
               map.addOverlay(marker);
         ';
	}
	else
	{
	if ($magnitud <= 4.5){
	  echo '      var x="'.$latitud.'";
               var y="'.$longitud.'";
	       var icono = new GIcon(G_DEFAULT_ICON);
 	       icono.image = "../../images/stories/OVSICORI//sismoazul.png";
	       var tamanoIcono = new GSize(20,20);
               icono.iconSize = tamanoIcono; 
	       icono.shadowSize = new GSize(0, 0);
               address = "Fecha:'.$fecha.'"+ "<br />";
  	       address = address + "Hora:'.$hora.'"+ "<br />";	
	       address = address + "Magnitud: '.$magnitud.'"+ "<br />";
               address = address + "Profundidad en km: '.$profundidad.'"+ "<br />";
               address = address + "Localizacion: '.$localizacion.'"+ "<br />";	
	       var point = new GLatLng('.$latitud.', '.$longitud.');
               var marker = createMarker(point,icono,address);
               map.addOverlay(marker);
         ';
	}
	else
	{
	  echo '      var x="'.$latitud.'";
               var y="'.$longitud.'";
               var icono = new GIcon(G_DEFAULT_ICON);
 	       icono.image = "../../images/stories/OVSICORI//sismorojo.png";
		var tamanoIcono = new GSize(20,20);
               icono.iconSize = tamanoIcono; 
		icono.shadowSize = new GSize(0, 0);
	       address = "Fecha:'.$fecha.'"+ "<br />";
	       address = address + "Hora:'.$hora.'"+ "<br />";
	       address = address + "Magnitud: '.$magnitud.'"+ "<br />";
               address = address + "Profundidad en km: '.$profundidad.'"+ "<br />";
	       address = address + "Localizacion: '.$localizacion.'"+ "<br />";
	       var point = new GLatLng('.$latitud.', '.$longitud.');
               var marker = createMarker(point,icono,address);
               map.addOverlay(marker);
         ';
	}
	}
        
     
    
   echo '
    }
    //]]>
    </script>
         ';

  ?>
  </head>
  <body onload="load()" onunload="GUnload()">
    <div id="map" style="width:700px;height:500px"></div>
    <p><strong><img src="../../images/stories/OVSICORI//sismoverde.png" border="0" />  Magnitud <= 3.5 |
  <img src="../../images/stories/OVSICORI//sismoazul.png" border="0" />  Magnitud <= 4.5 |
  <img src="../../images/stories/OVSICORI//sismorojo.png" border="0" />  Magnitud  > 4.5</strong></p>	
   <p><a class="normal" href="indexleqs.php">Regresar</a></p>
 <div id="footer"><table><tr>
<td width="300">&nbsp;</td>
<td align="center"><strong>OVSICORI-UNA</strong></td>
</tr></table></div>
</div> 	
  </body>
</html>
