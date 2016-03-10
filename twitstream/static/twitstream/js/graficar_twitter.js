$(document).ready(function(){
	google.charts.load('current', {'packages':['corechart'], 'language': 'es'});
	// Set a callback to run when the Google Visualization API is loaded.
    google.charts.setOnLoadCallback(drawChart);
	
    function drawChart() {
    	var data = new google.visualization.DataTable();
    	
    	data.addColumn('datetime', 'Fecha y hora');
    	
    	var dateFormatter = new google.visualization.DateFormat({pattern: 'dd/MM/yyyy HH:mm'});
    	dateFormatter.format(data, 0);
    	
    	var candidatos_length = candidatos.length;
    	var tiempos_length = tiempos.length;
    	
		for (var i = 0; i < candidatos_length; i++) {
			data.addColumn('number', candidatos[i]);
		}
    	tabla = [];
    	for (var j = 0; j < tiempos_length; j++) {
    		hr = tiempos[j].split(',')
    		tabla_tiempo = [new Date(Number(hr[0]),Number(hr[1])-1,Number(hr[2]),Number(hr[3]))]
    		for (var i = 0; i < candidatos_length; i++) {
    			tabla_tiempo.push(datatwitter[tiempos[j]][candidatos[i]]);
    		}
    		tabla.push(tabla_tiempo);
    	}
    	
    	data.addRows(tabla);

        var options = {
			title: 'Popularidad en Twitter',
			legend: { position: 'bottom' },
			height: '100%',
			width: '100%',
			hAxis: {
			    format: 'M/d/yy HH:mm',
		          gridlines: {
			            count: -1,
			            units: {
			              days: {format: ['MMM dd']},
			              hours: {format: ['HH:mm', 'ha']},
			            }
			          },
			          minorGridlines: {
			            units: {
			              hours: {format: ['hh:mm a', 'ha']},
			              minutes: {format: ['HH:mm a Z', ':mm']}
			            }
			          },
			},
			vAxis: {
				gridlines: {color: 'none'},
			    minValue: 0
			},
			
        };

        var chart = new google.visualization.LineChart(document.getElementById("timeline_twitter"));

        chart.draw(data, options);
    }
});    
