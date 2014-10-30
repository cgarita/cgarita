<?php

$path = '../';

if ( isset($_GET['db']) && !empty($_GET['db']))
    $db = $_GET['db'];
else $db = 'una';

if ($db === 'sentidos') $file = file_get_contents("$path/eventos_sentidos.json");
else $file = file_get_contents("$path/eventos.json");

$file = mb_convert_encoding($file, "UTF-8");
$json = json_decode($file,true);

function orientacion($baz) {

    if ( $baz > 350 or $baz <= 10) return  'Norte';
    elseif ( $baz > 10 and $baz <= 80) return  'Noreste';
    elseif ( $baz > 80 and $baz <= 100) return  'Este';
    elseif ( $baz > 100 and $baz <= 170) return  'Sureste';
    elseif ( $baz > 170 and $baz <= 190) return  'Sur';
    elseif ( $baz > 190 and $baz <= 260) return  'Suroeste';
    elseif ( $baz > 260 and $baz <= 280) return  'Oeste';

    return  'Noroeste';

};
function lugar($dist, $az, $pueblo, $distrito, $canton, $provincia){

    return "$dist km al ".orientacion($az)." de $pueblo, $distrito, $canton, $provincia ";
};

?>
<html>
<head>
<title>Lista de sentidos</title>

<style type="text/css">
    .fuente{
        background:#F0F0F0; 
        border-right-color:#666; 
        border:#CCC 1px; font-family:"Courier New", Courier, monospace; 
    }
    header{
        background:#333;
        color:#FFF;
        font-size:16px;
    }
    .maplink {
        color: blue;
        text-decoration: underline;
    }
    .maplink:hover {
        cursor: pointer;
    }
</style>

  
<script type='text/javascript' src='http://maps.google.com/maps/api/js?sensor=false&amp;language=es'></script>
<script  language="javascript" type="text/javascript">
    function abreVentana(evid) {
        //window.open("view.php?codigo="+num+"&width=720&height=620&menubar=no")	
        if (console) console.log('evid: ' + evid);

        var id = document.getElementById(evid);
        if ( ! id ) {
            if (console) console.log('No icon on map for: ' + evid);
            return;
        }

        var infowindow = document.getElementById(num+'window');
        if ( ! infowindow ) return;

        var map = document.getElementById('map');
        if ( ! map ) return;

        if (console) console.log('open: ' + id);
        infowindow.open(map, id);
    }
</script>

</head>


<body>

<div style="width:100%">
   <table border=0>
         <thead>
            <tr>
                <th width=100 >Fecha</th>
                <th width=70 >Hora</th>
                <th width=90 >Magnitud</th>
                <th width=100 >Profundidad</th>
                <th width=120 >Localizacion</th>
                <th width=120 >Origen</th>
                <th width=120 >Revisado</th>
                <th width=80 >Latitud</th>
                <th width=80 >Longitud</th>
                <th width=80 >ver</th>
            </tr>
         </thead>
         <tbody>
<?php
		  
  foreach($json as $obj) {

        $localizacion = lugar($obj['distancia'], $obj['acimut'], $obj['pueblo'], $obj['distrito'], $obj['canton'], $obj['provincia']);
        $origen= "Evid:".$obj['evid']." Orid:".$obj['orid'];

        echo "<tr bgcolor=#F0F0F0>
            <td>$obj[diaLocal]</td>
            <td>$obj[horaLocal]</td>
            <td>$obj[magnitude]</td>
            <td>$obj[depth]</td>
            <td>$localizacion</td>
            <td>$origen</td>
            <td>$obj[review]</td>
            <td>$obj[lat]</td>
            <td>$obj[lon]</td>
            <td ><p class=maplink onclick=abreVentana($obj[evid])>mapa</p></td>
        </tr>";
  }
?>
        </tbody>
    </table>
</div>

</body>

</html>
