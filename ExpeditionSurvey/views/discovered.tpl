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

        %include('starlist.tpl', stars=stars)

        %include('bodylist.tpl', bodies=bodies)

    </body>
</html>	
