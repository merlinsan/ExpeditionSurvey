        <h4>Bodies</h4>
        <table>
            <th>System Address</th>
            <th>Body ID</th>
            <th>Body Name</th>
            <th>Distance from<br>Arrival (LS)</th>
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
            <th>Discovered</th>
            <th>Mapped</th>
            <th>Scanned</th>
%for row in bodies:
            <tr>
                <td class='center'><a href='/system/{{row[0]}}'>{{row[0]}}</a></td>
                <td class='center'>{{row[1]}}</td>
                <td><a href='/body/{{row[0]}}/{{row[1]}}'>{{row[2]}}</a></td>
                <td class='right'>{{row[3]}}</td>
%terraformable = 1 if row[4] == 'Terraformable' else 0
                <td><a href='/terraformable/{{terraformable}}'>{{row[4]}}</a></td>
                <td><a href='/planetclass/{{row[5]}}'>{{row[5]}}</a></td>
                <td>{{row[6]}}</td>
                <td>{{row[7]}}</td>
                <td class='right'>{{row[8]}}</td>
                <td class='right'>{{row[9]}}</td>
                <td class='right'>{{row[10]}}</td>
                <td class='right'>{{row[11]}}</td>
                <td class='right'>{{row[12]}}</td>
                <td class='center'>{{row[13]}}</td>
                <td class='center'>{{row[14]}}</td>
                <td class='center'>{{row[15]}}</td>
                <td class='center'>{{row[16]}}</td>
            </tr>
%end
        </table>
    </body>
</html>	
