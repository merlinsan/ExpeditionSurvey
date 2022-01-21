%if len(rings):
        <h4>Rings</h4>
            <table>
                <tr>
                    <th>System Address</th>
                    <th>Body ID</th>
                    <th>Body Name</th>
                    <th>Ring Name</th>
                    <th>Class</th>
                    <th class='right'>Mass (MT)</th>
                    <th class='right'>Inner Radius (Km)</th>
                    <th class='right'>Outer Radius (Km)</th>
                    <th>Reserve Level</th>
                    <th>Discovered</th>
                    <th>Mapped</th>
                </tr>
                %for ring in rings:
                    <tr>
                        <td>{{ring[0]}}</td>
                        <td class='center'>{{ring[1]}}</td>
                        <td>{{ring[2]}}</td>
                        <td>{{ring[3]}}</td>
                        <td>{{ring[4]}}</td>
                        <td class='right'>{{ring[5]}}</td>
                        <td class='right'>{{ring[6]}}</td>
                        <td class='right'>{{ring[7]}}</td>
                        <td>{{ring[10]}}</td>
%discovered = 'Yes' if ring[8] == 1 else 'No'
                        <td class='center'>{{discovered}}</td>
%mapped = 'Yes' if ring[9] == 1 else 'No'
                        <td class='center'>{{mapped}}</td>
                    </tr>
                %end
            </table>
        %end
