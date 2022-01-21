        <h4>Bodies</h4>
%if len(bodies) == 0:
        <p>No bodies</p>
%else:
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
                <td><a href='/planet/terraformable/{{row[4]}}'>{{row[4]}}</a></td>
                <td><a href='/planet/class/{{row[5]}}'>{{row[5]}}</a></td>
                <td><a href='/planet/atmosphere/{{row[6]}}'>{{row[6]}}</a></td>
                <td><a href='/planet/volcanism/{{row[7]}}'>{{row[7]}}</a></td>
                <td class='right'>{{row[8]}}</td>
                <td class='right'>{{row[9]}}</td>
                <td class='right'>{{row[10]}}</td>
                <td class='right'>{{row[11]}}</td>
                <td class='right'>{{row[12]}}</td>
%landable = 'Yes' if row[13] == 1 else 'No'
                <td class='center'><a href='/planet/landable/{{row[13]}}'>{{landable}}</a></td>
%discovered = 'Yes' if row[14] == 1 else 'No'
                <td class='center'><a href='/planet/discovered/{{row[14]}}'>{{discovered}}</a></td>
%mapped = 'Yes' if row[15] == 1 else 'No'
                <td class='center'><a href='/planet/mapped/{{row[15]}}'>{{mapped}}</a></td>
%scanned ='Yes' if row[16] == 1 else 'No'
                <td class='center'><a href='/planet/scanned/{{row[16]}}'>{{scanned}}</a></td>
            </tr>
%end
        </table>
    </body>
</html>	
