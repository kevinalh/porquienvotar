var respuestas = {};
var respuestasJ = {};
var importanciasJ = {};
MIN_RESPUESTAS = 3;
var intento = 0;
var ventana_actual = 1; // 1 para Preguntas, 2 para Resultados
var importancias = {};
var matches = {};

google.charts.load('current', {packages: ['corechart','bar']});

$(document).ready(function() {

	$("#barra_error").hide();
	$("#boton_retroceso").hide();
	google.charts.setOnLoadCallback(preDibujar);
	function preDibujar() {
		$(".enviar").click(function(event) {
			var contador = 0;
			var i;
			for (i in respuestas) {
			    if (respuestas.hasOwnProperty(i)) {
			        contador++;
			    }
			}
			if (contador < MIN_RESPUESTAS) {
				event.preventDefault();
				$("#barra_error_texto").text('Debe responder por lo menos ' + MIN_RESPUESTAS + ' preguntas');
				$("#barra_error").show();
				$(window).scrollTop(0);
			} else {
				event.preventDefault();
				respuestasJ = JSON.stringify(respuestas);
				$("#barra_error").hide();
				intento++;
				cambiarVentanas();
				dibujar(respuestasJ, resultados(respuestas));
				tablaDibujar(respuestas, relpropuestas);
				$(window).scrollTop(0);
			}
		});
	}
	
	function resultados(respuestas) {
		// Euclides
		// var matches = {};
		var tmpValor = 0;
		var errores_suma = 0;
		var arrayR = Object.keys(respuestas);
		for (var i = 0; i < arrayR.length; i++) {
			importancias[arrayR[i]] = parseInt($('#slider_' + String(arrayR[i])).val(),10);
		}
		// key es Candidato.id
		for (var key in relpropuestas) {
		   if (relpropuestas.hasOwnProperty(key)) {
		      var propuestas_key = relpropuestas[key];
		      var valor_match = 0;
		      for (var prop_key in propuestas_key) {
		    	  if (propuestas_key.hasOwnProperty(prop_key)) {
		    		  if (respuestas.hasOwnProperty(prop_key)) {
		    			  tmpValor = Number(propuestas_key[prop_key])-Number(respuestas[prop_key]);
			    		  if (!(isNaN(tmpValor))) {
			    			  valor_match += importancias[prop_key]*Math.pow(tmpValor,2);
			    		  } else {
			    			  errores_suma += 1;
			    		  }
		    		  }
		    	  }
		      }
		      matches[key] = 100/(Math.sqrt(valor_match));
		   }
		}
	    if (errores_suma > 0) {
	    	console.warn("Han ocurrido %d errores en la suma", errores_suma);
	    }
		return matches;
	}
	
	function dibujar(respuestasJ, matches) {
		var dataCandidatos = new google.visualization.DataTable();
		var tablaCandidatos = [];
		for (candidato in candidatos) {
			// var lista_candidatos = $.map(relpropuestas, function(v,i) {
			//	return i;
			// });
			tmpTabla = [candidatos[Number(candidato)].alias, matches[Number(candidato)], candidatos[Number(candidato)].color];
			tablaCandidatos.push(tmpTabla);
		}
		dataCandidatos.addColumn('string','Partido');
		dataCandidatos.addColumn('number');
		dataCandidatos.addColumn({ type: 'string', role: 'style' });
		dataCandidatos.addRows(tablaCandidatos);
		dataCandidatos.sort({column: 1, desc: true});
		var ancho = 1200;
		var multiplicador = 0;
		for (var k in candidatos) {
			if (candidatos.hasOwnProperty(k)) multiplicador++;
		}
		var altura = 45*multiplicador;
		var opciones ={
				bars: 'horizontal',
				legend: 'none',
				'width': ancho, // 1200
				'height': altura, // 800
				'title': 'Coincidencias con candidatos'
		};
		var chart = new google.visualization.BarChart(document.getElementById("barrasCanvas"));
		chart.draw(dataCandidatos, opciones);
		importanciasJ = JSON.stringify(importancias);
		$("#tabsCandidatos a[href=\"#candidatoTabID_" + String(maximo(matches)) + "\"]").tab('show');
		subir_resultados(respuestasJ, importanciasJ, matches);
	}
	
	function sign(x){
	    if( +x === x ) {
	        return (x === 0) ? x : (x > 0) ? 1 : -1;
	    }
	    return NaN;
	}
	
	function maximo (matches) {
		var max = 0;
		var max_candidato = 0;
		for (var key in matches){
			if (matches.hasOwnProperty(key)) {
				if (matches[key] > max) {
					max = matches[key];
					max_candidato = key;
				}
			}
		}
		return max_candidato;
	}
	
	function tablaDibujar (respuestas, relpropuestas) {
		for (var key in respuestas) {
			if (respuestas.hasOwnProperty(key)) {
				var seleccionF = $(".tablasP_" + String(key)).find('.posUsuario');
				switch (respuestas[key]) {
					case -1:
						seleccionF.html('<i class="fa fa-thumbs-down"></i>');
						break;
					case 0:
						seleccionF.html('<i class="fa fa-circle-o"></i>');
						break;
					case 1:
						seleccionF.html('<i class="fa fa-thumbs-up"></i>');
						break;
					default:
						break;
				}
			}
		}
		
		for (var candidato in candidatos) {
			var seleccionCandidato = $('#Tab_' + String(candidatos[Number(candidato)].id));
			for (var keyPropuesta in relpropuestas[candidatos[candidato].id]) {
				var seleccionRespuesta = seleccionCandidato.find('.tablasP_' + String(keyPropuesta));
				var seleccionF = seleccionRespuesta.find('.posCandidato');
				switch (sign(Number(relpropuestas[candidatos[candidato].id][keyPropuesta]))) {
					case -1:
						seleccionF.html('<i class="fa fa-thumbs-down"></i>');
						break;
					case 0:
						seleccionF.html('<i class="fa fa-circle-o"></i>');
						break;
					case 1:
						seleccionF.html('<i class="fa fa-thumbs-up"></i>');
						break;
					default:
						break;
				}
				var seleccionM = seleccionRespuesta.find('.posMatch');
				if (respuestas.hasOwnProperty(keyPropuesta)){
					if (sign(Number(relpropuestas[candidatos[candidato].id][keyPropuesta])) == respuestas[keyPropuesta]){
						seleccionM.html('<i class="fa fa-check"></i>');
					}
					else {
						seleccionM.html('<i class="fa fa-times"></i>');
					}
				}
			}
		}
	}
	
	function cambiarVentanas () {
		$("#divPreguntas").toggle();
		$("#divResultados").toggle();
		if (intento > 0 && ventana_actual == 1) {
			$("#boton_retroceso_texto").html('<i class="fa fa-angle-left" aria-hidden="true"></i>&nbsp;Volver a las preguntas ');
			ventana_actual = 2;
			history.pushState(null, "Resultados", "resultados");
		} else if (intento > 0 && ventana_actual == 2) {
			$("#boton_retroceso_texto").html('<i class="fa fa-angle-right" aria-hidden="true"></i>&nbsp;Volver a los resultados ');
			ventana_actual = 1;
			history.replaceState(null, "Preguntas", "preguntas");
		}
		$("#boton_retroceso").show();
	}
	
	window.onpopstate = function() {
		cambiarVentanas();
	};
	
	$("#boton_retroceso").click(function(event) {
		if (intento > 0) {
			cambiarVentanas();
		}
	});
	    
	// Sube los resultados al servidor usando AJAX
	function subir_resultados(respuestasJ,importanciasJ,matches) {
        $.ajax({
            url: "enviardata",
            type: "POST",
            dataType: "json",
            data: { "respuestas_J" : respuestasJ,
            		"intento": intento,
            		"matches": matches,
            		"importancias_J" : importanciasJ,
            		"csrfmiddlewaretoken": window.csrftoken},
            success: function(json) {
                // $('#post-text').val(''); // remove the value from the input
                console.log(json); // log the returned json to the console
                console.log("success"); // another sanity check
            },
            error: function(xhr,errmsg,err) {
            	// console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    };
	
});
