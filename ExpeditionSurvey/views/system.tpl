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

        <h4>Stars</h4>
        <table class='noborder'>
            <tr>
            %for star in stars:
                <td class="noborder">
                    <table>
                        <tr>
                            <td colspan=2>{{star[0]}}</td>
                        </tr>
                        <tr>
                            <td>Distance from arrival point</td>
                            <td>{{star[1]}} LS</td>
                        </tr>
                        <tr>
                            <td>Type and Class</td>
                            <td><a href='/star/class/{{star[2]}}'>{{star[2]}}</a> {{star[3]}}</td>
                        </tr>
                        <tr>
                            <td>Stellar Mass</td>
                            <td>{{star[4]}}</td>
                        </tr>
                        <tr>
                            <td>Radius</td>
                            <td>{{star[5]}} Km</td>
                        </tr>
                        <tr>
                            <td>Absolute Magnitude</td>
                            <td>{{star[6]}}</td>
                        </tr>
                        <tr>
                            <td>Age</td>
                            <td>{{star[7]}} Million Years</td>
                        </tr>
                        <tr>
                            <td>Surface Temperature</td>
                            <td>{{star[8]}} Kelvin</td>
                        </tr>
                        <tr>
                            <td>Luminosity</td>
                            <td><a href='/star/luminosity/{{star[9]}}'>{{star[9]}}</a></td>
                        </tr>
                        <tr>
                            <td>Previously Discovered</td>
                            <td>{{star[10]}}</td>
                        </tr>
                    </table>
                </td>
            %end
            </tr>
        </table>

        %if len(rings):
        <h4>Belts</h4>
            <table>
                <tr>
                    <th>Name</th>
                    <th>Class</th>
                    <th class='right'>Mass (MT)</th>
                    <th class='right'>Inner Radius (Km)</th>
                    <th class='right'>Outer Radius (Km)</th>
                    <th>Discovered</th>
                </tr>
                %for ring in rings:
                    <tr>
                        <td>{{ring[0]}}</td>
                        <td>{{ring[1]}}</td>
                        <td class='right'>{{ring[2]}}</td>
                        <td class='right'>{{ring[3]}}</td>
                        <td class='right'>{{ring[4]}}</td>
                        <td>{{ring[5]}}</td>
                    </tr>
                %end
            </table>
        %end

        <h4>Bodies</h4>
        %if len(bodies) == 0:
            <p>No bodies</p>

        %else:
            <table>
                <tr>
                    <th class='left'>Name</th>
                    <th class='right'>Distance (LS)</th>
                    <th class='left'>Terraformable</th>
                    <th class='left'>Class</th>
                    <th class='left'>Atmosphere</th>
                    <th class='left'>Volcanism</th>
                    <th class='right'>Mass(EM)</th>
                    <th class='right'>Radius</th>
                    <th class='right'>Gravity</th>
                    <th class='right'>Temperature</th>
                    <th class='right'>Pressure</th>
                    <th class='left'>Landable</th>
                    <th class='left'>Discovered</th>
                    <th class='left'>Mapped</th>
                    <th class='left'>Scanned</th>
                </tr>
                %for body in bodies:
                    <tr>
                        <td><a href='/body/{{body[0]}}/{{body[1]}}'>{{body[2]}}</a></td>
                        <td class='right'>{{body[3]}}</td>
                        <td><a href='/terraformable/{{body[4]}}'>{{body[4]}}</a></td>
                        <td><a href='/planet/class/{{body[5]}}'>{{body[5]}}</a></td>
                        <td><a href='/planet/atmosphere/{{body[6]}}'>{{body[6]}}</a></td>
                        <td><a href='/planet/volcanism/{{body[7]}}'>{{body[7]}}</a></td>
                        <td class='right'>{{body[8]}}</td>
                        <td class='right'>{{body[9]}}</td>
                        <td class='right'>{{body[10]}}</td>
                        <td class='right'>{{body[11]}}</td>
                        <td class='right'>{{body[12]}}</td>
                        <td><a href='/planet/landable/{{body[13]}}'>{{body[13]}}</a></td>
                        <td><a href='/planet/discovered/{{body[14]}}'>{{body[14]}}</a></td>
                        <td><a href='/planet/mapped/{{body[15]}}'>{{body[15]}}</a></td>
                        <td><a href='/planet/scanned/{{body[16]}}'>{{body[16]}}</a></td>
                    </tr>
                %end
            </table>
        %end
    </body>
</html>	
