$(document).ready(function(){
	google.charts.load('current', {'packages':['corechart', 'controls'], 'language': 'es'});
	// Set a callback to run when the Google Visualization API is loaded.
    // google.charts.setOnLoadCallback(drawChart);
    google.charts.setOnLoadCallback(drawDashboard);
    
    var candidatos_length = candidatos.length;
	var tiempos_length = tiempos.length;
	
    function construirDataTable() {
    	var data = new google.visualization.DataTable();
    	
    	data.addColumn('date', 'Fechas');
    	
    	
		for (var i = 0; i < candidatos_length; i++) {
			data.addColumn('number', candidatos[i]);
		}
    	tabla = [];
    	for (var j = 1; j < tiempos_length; j++) {
    		hr = tiempos[j].split(',')
    		tabla_tiempo = [new Date(Number(hr[0]),Number(hr[1])-1,Number(hr[2]))]
    		for (var i = 0; i < candidatos_length; i++) {
    			tabla_tiempo.push(datatwitter[tiempos[j]][candidatos[i]]);
    		}
    		tabla.push(tabla_tiempo);
    	}
    	
    	data.addRows(tabla);
    	return data;
    }
    
    function drawDashboard() {
    	var data = construirDataTable();
    	
    	var dashboard = new google.visualization.Dashboard(document.getElementById('dashboard'));
    	
    	var colores_ordenados = []
    	
    	for (var i=0; i < candidatos_length; i++) {
    		colores_ordenados.push(colores[candidatos[i]]);
    	}
    	
        var options = {
			title: 'Popularidad en Twitter',
			// legend: { position: 'bottom' },
			height: '100%',
			width: '100%',
			hAxis: {
			    format: 'd/M/yy',
			      gridlines: {
			            count: -1,
			            units: {
			              days: {format: ['MMM dd']},
			            }
			          },
			},
			vAxis: {
				gridlines: {color: 'none'},
			    minValue: 0
			},
			colors: colores_ordenados,
        };
    	
        dateSlider = new google.visualization.ControlWrapper({
            'controlType': 'DateRangeFilter',
            'containerId': 'controles',
            'options': {
            	'filterColumnLabel': 'Fechas'
            }
          });
        
        chart_wrapper = new google.visualization.ChartWrapper({
            'chartType': 'LineChart',
            'containerId': 'timeline_twitter',
            'options': options,
        });
        
        var dateFormatter = new google.visualization.DateFormat({pattern: 'dd/MM/yyyy'});
    	dateFormatter.format(data, 0);
        
        dashboard.bind(dateSlider, chart_wrapper);

        dashboard.draw(data);
    }
});    
