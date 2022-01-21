        <h4>Stars</h4>
%if len(stars) == 0:
        <p>No Stars (Should not happen)</p>
%else:
        <table>
            <th>System Address</th>
            <th>Body ID</th>
            <th>Body Name</th>
            <th>Distance from<br>Arrival (LS)</th>
            <th>Star Class</th>
            <th>Stellar Mass</th>
            <th>Radius (Km)</th>
            <th>Absolute<br>Magnitude</th>
            <th>Age (MY)</th>
            <th>Surface<br>Temperature</th>
            <th>Luminosity</th>
            <th>Discovered</th>
%for star in stars:
            <tr>
                <td class='center'><a href='/system/{{star[0]}}'>{{star[0]}}</a></td>
                <td class='center'>{{star[1]}}</td>
                <td>{{star[2]}}</td>
                <td class='right'>{{star[3]}}</td>
                <td><a href='/star/class/{{star[4]}}'>{{star[4]}} {{star[5]}}</a></td>
                <td class='right'>{{star[6]}}</td>
                <td class='right'>{{star[7]}}</td>
                <td class='right'>{{star[8]}}</td>
                <td class='right'>{{star[9]}}</td>
                <td class='right'>{{star[10]}}</td>
                <td class='center'><a href='/star/luminosity/{{star[11]}}'>{{star[11]}}</a></td>
%discovered = 'Yes' if star[12] == 1 else 'No'
                <td class='center'><a href='/star/discovered/{{star[12]}}'>{{discovered}}</a></td>
            </tr>
%end
        </table>
