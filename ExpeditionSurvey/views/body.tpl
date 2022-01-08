<!DOCTYPE html>
<html>
    <head>
        <link rel='stylesheet' href='/css/stats.css'>
        <title>Expedition Survey</title>
    </head>

    <body>
        %include('menu.tpl')

        <h4>Body Information</h4>
        <table>
            <tr>
                <td>System Address</td>
                <td>{{body[0]}}</td>
            </tr>
            <tr>
                <td>Body ID</td>
                <td>{{body[1]}}</td>
            </tr>
            <tr>
                <td>Name</td>
                <td>{{body[2]}}</td>
            </tr>
            <tr>
                <td>Distance (LS)</td>
                <td>{{body[3]}}</td>
            </tr>
            <tr>
                <td>Terraformable</td>
                <td>{{body[4]}}</td>
            </tr>
            <tr>
                <td>Class</td>
                <td>{{body[5]}}</td>
            </tr>
            <tr>
                <td>Atmosphere</td>
                <td>{{body[6]}}</td>
            </tr>
            <tr>
                <td>Volcanism</td>
                <td>{{body[7]}}</td>
            </tr>
            <tr>
                <td>Mass(EM)</td>
                <td>{{body[8]}}</td>
            </tr>
            <tr>
                <td>Radius</td>
                <td>{{body[9]}}</td>
            </tr>
            <tr>
                <td>Gravity</td>
                <td>{{body[10]}}</td>
            </tr>
            <tr>
                <td>Temperature</td>
                <td>{{body[11]}}</td>
            </tr>
            <tr>
                <td>Pressure</td>
                <td>{{body[12]}}</td>
            </tr>
            <tr>
                <td>Landable</td>
                <td>{{body[13]}}</td>
            </tr>
            <tr>
                <td>Discovered</td>
                <td>{{body[14]}}</td>
            </tr>
            <tr>
                <td>Mapped</td>
                <td>{{body[15]}}</td>
            </tr>
            <tr>
                <td>Scanned</td>
                <td>{{body[16]}}</td>
            </tr>
        </table>

        %if len(composition):
        <h4>Body Composition</h4>
        <table>
            <tr>
                <th>Composite</th>
                <th style='text-align:right'>Percentage</th>
            </tr>
            %for row in composition:
                <tr>
                    <td>{{row[0]}}</td>
                    <td style='text-align:right'>{{row[1]}}</td>
                </tr>
            %end
        </table>
        %end

        %if len(atmosphere):
        <h4>Atmospheric Composition</h4>
        <table>
            <tr>
                <th>Composite</th>
                <th style='text-align:right'>Percentage</th>
            </tr>
            %for row in atmosphere:
                <tr>
                    <td>{{row[0]}}</td>
                    <td style='text-align:right'>{{row[1]}}</td>
                </tr>
            %end
        </table>
        %end

        %if len(landings):
        <h4>Landings</h4>
        <table>
            <tr>
                <th>Latitude</th>
                <th>Longitude</th>
            </tr>
            %for row in landings:
                <tr>
                    <td>{{row[0]}}</td>
                    <td>{{row[1]}}</td>
                </tr>
            %end
        </table>
        %end

        %if len(materials):
        <h4>Materials</h4>
        <table>
            <tr>
                <th>Material</th>
                <th>Percentage</th>
            </tr>
            %for row in materials:
                <tr>
                    <td>{{row[0]}}</td>
                    <td style='text-align:right'>{{row[1]}}</td>
                </tr>
            %end
        </table>
        %end

        %if len(rings):
        <h4>Rings</h4>
        <table>
            <tr>
                <th>Name</th>
                <th>Class</th>
                <th style='text-align:right'>Mass</th>
                <th style='text-align:right'>Inner radius</th>
                <th style='text-align:right'>Outer Radius</th>
                <th>Discovered</th>
                <th>Mapped</th>
                <th>Reserves</th>
                <th>Scanned</th>
            </tr>
            %for row in rings:
                <tr>
                    <td>{{row[0]}}</td>
                    <td>{{row[1]}}</td>
                    <td style='text-align:right'>{{row[2]}}</td>
                    <td style='text-align:right'>{{row[3]}}</td>
                    <td style='text-align:right'>{{row[4]}}</td>
                    <td>{{row[5]}}</td>
                    <td>{{row[6]}}</td>
                    <td>{{row[7]}}</td>
                    <td></td>
                </tr>
            %end
        </table>
        %end

        %if len(signals):
        <h4>Signals</h4>
        <table>
            <tr>
                <th>Type</th>
                <th>Qty</th>
            </tr>
            %for row in signals:
                <tr>
                    <td>{{row[0]}}</td>
                    <td style='text-align:right'>{{row[1]}}</td>
                </tr>
            %end
        </table>
        %end
    </body>
</html>	
