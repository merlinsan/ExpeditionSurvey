<!DOCTYPE html>
<html>
    <head>
        <link rel='stylesheet' href='/css/stats.css'>
        <title>Expedition Survey</title>
    </head>

    <body>
        %include('menu.tpl')
        
        <h4>Systems</h4>
        <table>
            <tr>
                <th>System Address</th>
                <th>System</th>
                <th>X</th>
                <th>Y</th>
                <th>Z</th>
                <th>Bodies</th>
            </tr>
%for system in systems:
            <tr>
                <td class='center'><a href='/system/{{system[0]}}'>{{system[0]}}</a></td>
                <td>{{system[1]}}</td>
                <td class='right'>{{system[2]}}</td>
                <td class='right'>{{system[3]}}</td>
                <td class='right'>{{system[4]}}</td>
                <td class='center'>{{system[5]}}</td>
            </tr>
%end
        </table>
    </body>
</html>
