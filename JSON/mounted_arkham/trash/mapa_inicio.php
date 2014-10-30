<?php

if ( isset($_GET['db']) && !empty($_GET['db']))
    $db = $_GET['db'];
else $db = 'una';

if ($db === 'sentidos') $file = file_get_contents("eventos_sentidos.json");
else $file = file_get_contents("eventos.json");

$file = mb_convert_encoding($file, "UTF-8");
$json = json_decode($file,true);

#foreach($json as $registro) {
#    print_r($registro['pueblo']);
#    #echo $registro['lat'];
#    echo "\n";
#}
#exit();
function orientacion($baz) {

    if ( $baz > 350 or $baz <= 10) return  'Norte';
    elseif ( $baz > 10 and $baz <= 80) return  'Noreste';
    elseif ( $baz > 80 and $baz <= 100) return  'Este';
    elseif ( $baz > 100 and $baz <= 170) return  'Sureste';
    elseif ( $baz > 170 and $baz <= 190) return  'Sur';
    elseif ( $baz > 190 and $baz <= 260) return  'Suroeste';
    elseif ( $baz > 260 and $baz <= 280) return  'Oeste';

    return  'Noroeste';

}
function lugar($dist, $az, $pueblo, $distrito, $canton, $provincia){

    return "$dist km al ".orientacion($az)." de $pueblo, $distrito, $canton, $provincia ";
} 


?>	
<html> 
	
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Mapa Sismicidad Reciente</title> 
    <style type="text/css">
		*{ margin: 0; padding: 0; }
		html, body, #map{
			width: 100%;
			height: 99%;
		}
        .small_icon{
            width: 15px;
            height: 15px;
        }
        .boxed{
            background: none repeat scroll 0 0 #bdbdbd;
            margin: 3px;
            padding: 3px;
            border: 1px solid black;
        }
        .boxed_logo{
            margin: 3px;
            padding: 5px;
            background: none repeat scroll 0 0 #FFFFFF;
        }
    </style>

	<script type='text/javascript' src='http://maps.google.com/maps/api/js?sensor=false&amp;language=es'></script>
	<script type='text/javascript'>	
		window.onload = function(){
			
			var objetos = new Array();
			var n=1;
		
			var options = {
				zoom: 7
				, center: new google.maps.LatLng(9.5775775, -84.2788775)
				, mapTypeId: google.maps.MapTypeId.TERRAIN
			};
		 
			var map = new google.maps.Map(document.getElementById('map'), options);
		
			
            var leyenda = document.getElementById('leyenda');
            map.controls[google.maps.ControlPosition.BOTTOM_CENTER].push(leyenda);

		/**************Ciclo para recorrer todos los registros***********************/
		
		<?php		

            $defaultsize = 10; # size default
            $now = time();
            $i = -1;
			foreach($json as $registro) {
                $i += 1;
				$time= $now - $registro['time'];
				$latitud= $registro['lat'];
				$longitud= $registro['lon'];
				$fecha= $registro['diaLocal'];
				$hora= $registro['horaLocal']." ".$registro['timeZone'];
				$magnitudraw= intval($registro['magnitude']);
				$magnitud= $registro['magnitude']." ".$registro['magtype'];
				$origen= "Evid:".$registro['evid']." Orid:".$registro['orid'];
				$revisado= $registro['review'];
				$autor= $registro['auth'];
				$profundidad = $registro['depth'];
                $localizacion = lugar($registro['distancia'], $registro['acimut'], $registro['pueblo'], $registro['distrito'], $registro['canton'], $registro['provincia']);
					
				/*------------------------Tabla que ira en el marcador (leyenda) -----------------------------*/
				$tabla  ="<table><tr><td width=120><h2><img src=logo.jpg></h2></td></tr>"; 
				$tabla .= "<tr bgcolor=#DEDEEF><td width=90>Fecha:</td> <td>$fecha</td></tr>";
				$tabla .= "<tr bgcolor=#DEDEEF><td width=90>Hora:</td> <td>$hora</td></tr>";
				$tabla .= "<tr><td width=90>Profundidad:</td> <td>$profundidad</td></tr>";
				$tabla .= "<tr bgcolor=#DEDEEF><td width=90>Magnitud:</td> <td>$magnitud</td></tr>";
				$tabla .= "<tr><td width=90>Localizacion:</td> <td>$localizacion</td></tr>";					
				$tabla .= "<tr bgcolor=#DEDEEF><td width=90>Origen:</td> <td>$origen</td></tr>";
				$tabla .= "<tr><td width=90>Coordenadas:</td> <td>($latitud,$longitud)</td></tr>";
				$tabla .= "<tr bgcolor=#DEDEEF><td width=90>Autor:</td> <td>$autor</td></tr>";
				$tabla .= "<tr bgcolor=#DEDEEF><td width=90>Revisado:</td> <td>$revisado</td></tr>";
				$tabla .= "</table>";
				//$tabla .= "<tr></table>";
				/*------------------------------------------------------------------------------------*/
				if ($time <= 86400){ # menos de 1 dia
					$color="/images/stories/OVSICORI/sismorojo.png";
                    $index = 3;
				} else if($time <= 604800){ # menos de 1 semana
                    $color= "/images/stories/OVSICORI/sismoverde.png";
                    $index = 2;
                } else{
                    $index = 1;
                    $color= "/images/stories/OVSICORI/sismoazul.png";
                }
                if ($magnitudraw > 1 ) {
                    $size = intval($magnitudraw * $defaultsize);
                } else {
                    $size = $defaultsize;
                }
		?>

				var obj = new Object();
                    obj.fecha = '<?php echo $fecha;?>';
                    obj.hora = '<?php echo $hora;?>';
                    obj.profundidad = '<?php echo $profundidad;?>';
                    obj.magnitud = '<?php echo $magnitud;?>';
                    obj.localizacion = '<?php echo $localizacion;?>';
                    //obj.origen = '<?php echo $origen;?>';
                    obj.latitud = '<?php echo $latitud;?>';
                    obj.longitud = '<?php echo $longitud;?>';
                    obj.icono = '<?php echo $color;?>';
                    obj.size = '<?php echo $size;?>';
                    obj.index = '<?php echo $index;?>';
                    obj.tabla = '<?php echo $tabla;?>';
                    objetos[<?php echo $i ?>] = obj;

		<?php
			} // fin for
		?>
            var icongroup = {};

			for(var x=0; x<objetos.length; x++){

                var size = parseInt(objetos[x].size,10);
                var color = objetos[x].icono;
                //if (console) console.log('['+size+']['+color+']');

                if (typeof icongroup[color] === 'undefined' || typeof icongroup[color][size] === 'undefined') {
                    //if (console) console.log('['+objetos[x].size+']');
                    var image = {
                        url: objetos[x].icono,
                        scaledSize: new google.maps.Size(size, size),
                        //origin: new google.maps.Point(0,0), //origin
                        //anchor: new google.maps.Point(0, 0) //anchor
                    };
                    if ( typeof icongroup[color] === 'undefined' ) icongroup[color] = {};
                    icongroup[color][size] = image;
                    //if (console) console.dir(image);
                } else  {
                    //if (console) console.log('Got it!!!!');
                    var image = icongroup[color][size];
                    //if (console) console.dir(image);

                }


				var marker = new google.maps.Marker({
					position: new google.maps.LatLng(objetos[x].latitud, objetos[x].longitud),
					map: map,
					title: 'Magnitud: '+objetos[x].magnitud,
                    icon: image,
					zIndex: parseInt(objetos[x].index,10),
					tab: objetos[x].tabla
				});

                marker.set("id", objetos[x].evid);
				
				google.maps.event.addListener(marker, 'click', function(id){
					var popup = new google.maps.InfoWindow();
					popup.setContent(this.tab);
					popup.set("id",id + "window");
					popup.open(map, this);
				});

			}
		};
				
		function cerrarVentana()
		{
			window.close();
		}; 


	</script>
		
</head>

<body >
	
	<div id="map" style="width:100%;height:100%"></div>
	<div id="leyenda">
		<table>
			<tr>
                <td class='boxed'><img class='small_icon' src="/images/stories/OVSICORI/sismorojo.png" />  < 24 horas</td>
                <td class='boxed'><img class='small_icon' src="/images/stories/OVSICORI/sismoazul.png" />  1-7 dias</td>
                <td class='boxed'><img class='small_icon' src="/images/stories/OVSICORI/sismoverde.png" /> > 7  dias</td>
				<td class='boxed_logo' ><img class='small_icon' src="logo.jpg" /><strong>OVSICORI-UNA</strong></td>
			</tr>
		</table>
	</div>
	</div>
</body>
</html>
