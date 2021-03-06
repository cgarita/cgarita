<?php

if ( isset($_GET['refresh']) && !empty($_GET['refresh']))
    $refresh = $_GET['refresh'];
else $refresh = false;

if ( isset($_GET['notable']) && !empty($_GET['notable']))
    $notable = $_GET['notable'];
else $notable = false;

if ( isset($_GET['db']) && !empty($_GET['db']))
    $db = $_GET['db'];
else $db = 'una';

if ($db === 'sentidos') $file = file_get_contents("eventos_sentidos.json");
else $file = file_get_contents("eventos.json");

$file = mb_convert_encoding($file, "UTF-8");
$json = json_decode($file,true);

function print_new_event($i,$registro) {

    $defaultsize = 10; # size default
    $now = time();
    $time= $now - $registro['time'];
    $latitud= $registro['lat'];
    $longitud= $registro['lon'];
    $fecha= $registro['diaLocal'];
    //$hora= $registro['horaLocal']." ".$registro['timeZone'];
    $hora= $registro['horaLocal'];
    $magnitudraw= intval($registro['magnitude']);
    $magnitud= $registro['magnitude']." ".$registro['magtype'];
    $evid= $registro['evid'];
    //$origen= "Evid:".$registro['evid']." Orid:".$registro['orid'];
    $revisado= $registro['review'];
    $autor= $registro['auth'];
    $profundidad = $registro['depth'];
    $localizacion = lugar($registro['distancia'], $registro['acimut'], $registro['pueblo'], $registro['distrito'], $registro['canton'], $registro['provincia']);
        
    //$t  ="<table><tr><td width=120><h2><img src=logo.jpg></h2></td></tr>"; 
    $t  ="<div class=noscrollbar><table>"; 
    $t .= "<tr bgcolor=#DEDEEF><td width=90>Fecha:</td> <td>$fecha</td></tr>";
    $t .= "<tr bgcolor=#DEDEEF><td width=90>Hora:</td> <td>$hora</td></tr>";
    $t .= "<tr><td width=90>Profundidad:</td> <td>$profundidad</td></tr>";
    $t .= "<tr bgcolor=#DEDEEF><td width=90>Magnitud:</td> <td>$magnitud</td></tr>";
    $t .= "<tr><td width=90>Localizacion:</td> <td>$localizacion</td></tr>";					
    //$t .= "<tr bgcolor=#DEDEEF><td width=90>Origen:</td> <td>$origen</td></tr>";
    $t .= "<tr><td width=90>Coordenadas:</td> <td>($latitud,$longitud)</td></tr>";
    $t .= "<tr bgcolor=#DEDEEF><td width=90>Autor:</td> <td>$autor</td></tr>";
    $t .= "<tr bgcolor=#DEDEEF><td width=90>Revisado:</td> <td>$revisado</td></tr>";
    $t .= "</table></div>";

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

    echo "\n\t\teventos[$i] = {
            fecha : '$fecha',
            hora : '$hora',
            profundidad : '$profundidad',
            magnitud : '$magnitud',
            localizacion : '$localizacion',
            latitud : '$latitud',
            longitud : '$longitud',
            icono : '$color',
            size : '$size',
            revisado : '$revisado',
            evid : '$evid',
            index : '$index',
            tabla : '$t'
        };\n";
}
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

    <?php echo ($refresh ? "<meta http-equiv=\"refresh\" content=\"$refresh\">" : '') ?>

    <title>Mapa Sismicidad Reciente</title> 
    <style type="text/css">
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
        #map{
            width: 100%;
            height: <?php echo ($notable ? '100%' : '800px') ?>;
        }
        .noscrollbar {
            line-height:1.35;
            overflow:hidden;
            white-space:nowrap;
            min-height: 270px;
            width: auto;
        }
        .fuente{
            background:#F0F0F0; 
            border-right-color:#666; 
            border:#CCC 1px; font-family:"Courier New", Courier, monospace; 
        }
        #tabla{
            border: 1px solid black;
            border-collapse: collapse;
            margin: 3px;
        }
        #tabla td{
            border: 1px solid black;
            padding: 3px;
        }
        #tabla th{
            background:#333;
            color:#FFF;
            padding: 13px;
        }
        .maplink {
        }
        .maplink:hover {
            cursor: pointer;
        }
    </style>

	<script type='text/javascript' src='http://maps.google.com/maps/api/js?sensor=false&language=es'></script>
	<script type='text/javascript'>	
        var notable = <?php echo ($notable ? 'true' : 'false') ?>;
        var markers = new Array();
        var map = new Object();
        var mapDiv = 'map';
        var mapDivObject = new Object();
        var openmarker = new Object();
        var eventos = new Array();
        var n=1;
        var options = {
            zoom: 7,
            scrollwheel: false,
            center: new google.maps.LatLng(9, -84),
            streetViewControl: false,
            zoomControlOptions: { style:google.maps.ZoomControlStyle.SMALL }, 
            mapTypeId: google.maps.MapTypeId.TERRAIN
        };
        
        <?php		
            $i = -1;
            foreach($json as $registro) {
                $i += 1;
                print_new_event($i,$registro);
            }
        ?>

        function show(i) {
            google.maps.event.trigger(markers[i], 'click');
        }

		window.onload = function(){

            map = new google.maps.Map(document.getElementById(mapDiv), options);
        
            mapDivObject =  document.getElementById(mapDiv);
            
            var leyenda = document.getElementById('leyenda');
            map.controls[google.maps.ControlPosition.BOTTOM_CENTER].push(leyenda);

			//for(var x=0; x<eventos.length; x++){
			for(var x=eventos.length-1; x>=0; x--){

                var size = parseInt(eventos[x].size,10);
                var color = eventos[x].icono;
                var image = {
                    url: eventos[x].icono,
                    scaledSize: new google.maps.Size(size, size),
                };

                if ( notable ) {
                } else {

                    // Add row to table first
                    var table = document.getElementById("tabla");
                    var rowCount = table.rows.length;
                    var row = table.insertRow(rowCount); 
                    row.id = eventos[x].evid + '_';
                    //row.onclick = abreVentana(eventos[x].evid);
                    row.insertCell(0).innerHTML= eventos[x].fecha;
                    row.insertCell(1).innerHTML= eventos[x].hora;
                    row.insertCell(2).innerHTML= eventos[x].magnitud;
                    row.insertCell(3).innerHTML= eventos[x].profundidad;
                    row.insertCell(4).innerHTML= eventos[x].localizacion;
                    //row.insertCell(5).innerHTML= eventos[x].origen;
                    row.insertCell(5).innerHTML= eventos[x].revisado;
                    row.insertCell(6).innerHTML= eventos[x].latitud;
                    row.insertCell(7).innerHTML= eventos[x].longitud;

                    row.addEventListener("click", function( event ) {
                        var evento = this.id.split('_')[0];
                        show(evento);
                    });

                }

				var marker = new google.maps.Marker({
					position: new google.maps.LatLng(eventos[x].latitud, eventos[x].longitud),
					map: map,
                    draggable: false,
                    raiseOnDrag: false,
                    icon: image,
                    info: new google.maps.InfoWindow({ content: eventos[x].tabla }),
                    clickable: true,
					zIndex: parseInt(eventos[x].index,10)
				});

                //marker.id = eventos[x].evid;
                markers[eventos[x].evid] = marker;

                google.maps.event.addListener(marker, 'click', function() {
                    if(typeof openmarker.info !== 'undefined') openmarker.info.close();
                    this.info.open(this.getMap(),this)
                    openmarker = this;
                    mapDivObject.scrollIntoView(true);
                });

			}
		}; //window.onload()
				
	</script>
		
</head>

<body>
	
	<div id="map"></div>
	<div id="leyenda">
		<table>
			<tr>
                <td class='boxed'><img class='small_icon' src="sismorojo.png" />  < 24 horas</td>
                <td class='boxed'><img class='small_icon' src="sismoazul.png" />  1-7 dias</td>
                <td class='boxed'><img class='small_icon' src="sismoverde.png" /> > 7  dias</td>
				<td class='boxed_logo' ><img class='small_icon' src="logo.jpg" /><strong>OVSICORI-UNA</strong></td>
			</tr>
		</table>
	</div>

<?php 

if ( $notable ) {
    echo "</body></html>";
    return;
} else {
?>
    <div>
        <table id=tabla>
            <thead>
                <tr>
                    <th>Fecha</th>
                    <th>Hora</th>
                    <th>Magnitud</th>
                    <th>Profundidad</th>
                    <th width=120 >Localizacion</th>
                    <!--
                    <th width=120 >Origen</th>
                    -->
                    <th>Revisado</th>
                    <th>Latitud</th>
                    <th>Longitud</th>
                </tr>
            </thead>
            <tbody>
            </tbody>
        </table>
    </div>
</body>
</html>
<?php
} 
?>
