<!DOCTYPE html>
<html>
    <head>
        <link rel='stylesheet' href='/css/stats.css'>
        <title>Expedition Survey</title>
    </head>

    <body>
        %include('menu.tpl')
        
        <h4>Summary</h4>
        <table>
            <tr>
                <td>Total Distance</td>
                <td>{{distance}}</td>
            </tr>
            <tr>
                <td>Total Fuel</td>
                <td>{{fuel}}</td>
            </tr>
            <tr>
                <td>Total Jumps</td>
                <td>{{totaljumps}}</td>
            </tr>
        </table>

        <h4>Jumps</h4>
        <table>
            <tr>
                <th class='left'>Date/Time</th>
                <th class='left'>System</th>
                <th class='right'>Distance</th>
                <th class='right'>Fuel Used</th>
                <th class='right'>Total<br>Bodies</th>
                <th class='right'>Stars</th>
                <th class='right'>Other<br>Bodies</th>
            </tr>
            %for jump in jumps:
            <tr>
                <td>{{jump[0]}}</td>
                <td><a href='/system/{{jump[1]}}'>{{jump[2]}}</a></td>
                <td class='right'>{{jump[3]}}</td>
                <td class='right'>{{jump[4]}}</td>
                <td class='right'>{{jump[5]}}</td>
                <td class='right'>{{jump[6]}}</td>
%if (jump[6]+jump[7]) == jump[5]:
                <td class='right'>{{jump[7]}}</td>
%else:
                <td class='right'>&#40;{{jump[7]}}&#41;</td>
%end
            </tr>
            %end
        </table>
    </body>
</html>
