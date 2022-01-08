<!DOCTYPE html>
<html>
    <head>
        <link rel='stylesheet' href='/css/stats.css'>
        <title>Expedition Survey</title>
    </head>

    <body>
        %include('menu.tpl')

        <h4>{{title}}</h4>

        %include('bodylist', bodies=bodies)
    </body>
</html>	
