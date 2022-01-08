<!DOCTYPE html>
<html>
    <head>
        <link rel='stylesheet' href='/css/stats.css'>
        <title>Expedition Survey</title>
    </head>

    <body>
        %include('menu.tpl')

%if discovered:
        <h4>Previously Discovered Bodies</h4>
%else:
        <h4>Newly Discovered Bodies</h4>
%end

        <h4>Stars</h4>
        <table>
            <tr>
                <th>System Address</th>
                <th>Body ID</th>
                <th>Body Name</th>
                <th>Distance from<br>Arrival (LS)</th>
                <th>Star<br>Class</th>
                <th>Stellar<br>Mass</th>
                <th>Radius (Km)</th>
                <th>Absolute<br>Magnitude</th>
                <th>Age (MY)</th>
                <th>Surface<br>Temp (K)</th>
                <th>Luminosity</th>
            </tr>
%for row in stars:
            <tr>
                <td class='center'><a href='/system/{{row[0]}}'>{{row[0]}}</a></td>
                <td class='center'>{{row[1]}}</td>
                <td><a href='/star/{{row[0]}}/{{row[1]}}'>{{row[2]}}</a></td>
                <td  class='right'>{{row[3]}}</td>
                <td>{{row[4]}} {{row[5]}}</td>
                <td class='right'>{{row[6]}}</td>
                <td class='right'>{{row[7]}}</td>
                <td class='right'>{{row[8]}}</td>
                <td class='right'>{{row[9]}}</td>
                <td class='right'>{{row[10]}}</td>
                <td class='center'>{{row[11]}}</td>
            </tr>
%end
        </table>

        <h4>Bodies</h4>
        <table>
            <th>System Address</th>
            <th>Body ID</th>
            <th>Body Name</th>
            <th>Distanc from<br>Arrival (LS)</th>
            <th>Terraformable</th>
            <th>Planet Class</th>
            <th>Atmosphere</th>
            <th>Volcanism</th>
            <th>Mass (EM)</th>
            <th>Radius (Km)</th>
            <th>Surface<br>Gravity</th>
            <th>Surface<br>Temp (K)</th>
            <th>Surface<br>Pressure (P)</th>
            <th>Landable</th>
            <th>Mapped</th>
            <th>Scanned</th>
%for row in bodies:
            <tr>
                <td class='center'>{{row[0]}}</td>
                <td class='center'>{{row[1]}}</td>
                <td><a href='/body/{{row[0]}}/{{row[1]}}'>{{row[2]}}</a></td>
                <td class='right'>{{row[3]}}</td>
                <td>{{row[4]}}</td>
                <td>{{row[5]}}</td>
                <td>{{row[6]}}</td>
                <td>{{row[7]}}</td>
                <td class='right'>{{row[8]}}</td>
                <td class='right'>{{row[9]}}</td>
                <td class='right'>{{row[10]}}</td>
                <td class='right'>{{row[11]}}</td>
                <td class='right'>{{row[12]}}</td>
                <td class='center'>{{row[13]}}</td>
                <td class='center'>{{row[15]}}</td>
                <td class='center'>{{row[16]}}</td>
            </tr>
%end
        </table>
    </body>
</html>	
