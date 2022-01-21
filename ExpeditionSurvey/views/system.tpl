<!DOCTYPE html>
<html>
    <head>
        <link rel='stylesheet' href='/css/stats.css'>
        <title>Expedition Survey</title>
    </head>

    <body>
        %include('menu.tpl')

        <h4>System Information</h4>
        <table>
            <tr>
                <td>System Address</td>
                <td colspan=2>{{system[0]}}</td>
            </tr>
            <tr>
                <td>System Name</td>
                <td colspan=2>{{system[1]}}</td>
            </tr>
            <tr>
                <td rowspan=3>Location (Sol)</td>
                <td class='noborder'>X:</td><td class='noborder'; class='right'>{{system[2]}}</td>
            </tr>
            <tr>
                <td class='noborder'>Y:</td><td class='noborder'; class='right'>{{system[3]}}</td>
            </tr>
            <tr>
                <td class='noborder'>Z:</td><td class='noborder'; class='right'>{{system[4]}}</td>
            </tr>
        </table>

        %include('starlist.tpl', stars=stars)

        %include('ringlist.tpl', rings=rings)
        
        %include('bodylist.tpl', bodies=bodies)
    </body>
</html>	
