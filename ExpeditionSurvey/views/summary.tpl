<!DOCTYPE html>
<html>
    <head>
        <link rel='stylesheet' href='/css/stats.css'>
        <title>Expedition Survey</title>
    </head>

    <body>
        <div>
        <h4>Exploration Summary</h4>
        <table>
            <tr>
                <td>Total Distance (LY)</td>
                <td>{{distance}}</td>
            </tr>
            <tr>
                <td>Total Fuel (T)</td>
                <td>{{fuel}}</td>
            </tr>
            <tr>
                <td>Jumps</td>
                <td><a href='/jumps'>{{jumps}}</a></td>
            </tr>
            <tr>
                <td>Systems Visited</td>
                <td><a href='/systems'>{{systems}}</a></td>
            </tr>
        </table>
        </div>

        <div class='left'>
        <h4>Star Summary</h4>
        <table>
            <tr>
                <th>Star Type</th>
                <th>Count</th>
            </tr>
%count=0
%for star in stars:
%count=count+star[1]
            <tr>
                <td><a href='/star/class/{{star[0]}}'>{{star[0]}}</a></td>
                <td>{{star[1]}}</td>
            </tr>
%end
            <tr>
                <td>Total Stars</td>
                <td>{{count}}
        </table>
        </div>

        <div class='left'>
        <h4>Body Summary</h4>
        <table>
            <tr>
                <th>Body Type</th>
                <th>Count</th>
            </tr>
%count=0
%for body in bodies:
%count=count+body[1]
            <tr>
                <td><a href='/planet/class/{{body[0]}}'>{{body[0]}}</a></td>
                <td>{{body[1]}}</td>
            </tr>
%end
            <tr>
                <td>Total Bodies</td>
                <td>{{count}}</td>
            </tr>
        </table>
        </div>

        <div class='left'>
        <h4>Signals Summary</h4>
        <table>
            <tr>
                <th>Signal Type</th>
                <th>Count</th>
            </tr>
%count=0
%for signal in signals:
%count=count+signal[1]
            <tr>
                <td><a href='/signal/type/{{signal[0]}}'>{{signal[0]}}</a></td>
                <td>{{signal[1]}}</td>
            </tr>
%end
            <tr>
                <td>Total Signals</td>
                <td>{{count}}</td>
            </tr>
        </table>
        </div>

        <div class='left'>
        <h4>Scanned Bodies</h4>
        <table>
            <tr>
                <th>Planet Class</th>
                <th>Count</th>
            </tr>
%count=0
%for planet in scannedbodies:
%count=count+planet[1]
            <tr>
                <td>{{planet[0]}}</td>
                <td>{{planet[1]}}</td>
            </tr>
%end
            <tr>
                <td>Total Scanned</td>
                <td>{{count}}</td>
            </tr>
        </table>
        </div>

        <div class='left'>
        <h4>Stars Discovered</h4>
        <table>
            <tr>
                <th>Star Type</th>
                <th>Count</th>
            </tr>
%count=0
%for star in newstars:
%count=count+star[1]
            <tr>
                <td>{{star[0]}}</td>
                <td>{{star[1]}}</td>
            </tr>
%end
            <tr>
                <td>Total New Stars</td>
                <td>{{count}}</td>
            </tr>
        </table>
        </div>

        <div class='left'>
        <h4>Bodies Discovered</h4>
        <table>
            <tr>
                <th>Body Type</th>
                <th>Count</th>
            </tr>
%count=0
%for body in newbodies:
%count=count+body[1]
            <tr>
                <td>{{body[0]}}</td>
                <td>{{body[1]}}</td>
            </tr>
%end
            <tr>
                <td>Total New Bodies</td>
                <td>{{count}}</td>
            </tr>
        </table>
        </div>

    </body>
</html>
