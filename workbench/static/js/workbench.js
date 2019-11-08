//   This file is part of EEG Workbench.
//
//   EEG Workbench is free software: you can redistribute it and/or modify
//   it under the terms of the GNU General Public License as published by
//   the Free Software Foundation, either version 3 of the License, or
//   (at your option) any later version.
//
//   EEG Workbench is distributed in the hope that it will be useful,
//   but WITHOUT ANY WARRANTY; without even the implied warranty of
//   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//   GNU General Public License for more details.
//
//   You should have received a copy of the GNU General Public License
//   along with EEG Workbench.  If not, see <http://www.gnu.org/licenses/>.

(function () {

	var current_eeg		= {};
	var current_chart_band	= "frequency";

	// utils
	function refresh_listing(d) {
		var source_sel = "#eeg-source-select";
		var target_sel = "#eeg-target-select";

		if ( d.msg === "ok" ) {
			$.each(d.data.eeg, function(i, e) { 
				var new_opt = $("<option>", { value: e, text: (e.split('.'))[0] });
				$(source_sel).append(new_opt);

				new_opt = $("<option>", { value: e, text: (e.split('.'))[0] });
				$(target_sel).append(new_opt);
			} );			
		}

	}

	// load the available sensors based on the
	// eeg data objects already uploaded to the
	// server
	function load_eeg_set(e) {
		var bttn_id	= e.currentTarget.id;
		var source_sel	= "#eeg-source-select"; // ID of source selection field
		var target_sel	= "#eeg-target-select"; // ID of target selection field
		var eeg_source_tbl = "#eeg-source-set"; // ID of source sensor table display
		var eeg_target_tbl = "#eeg-target-set"; // ID of target sensor table display
		var eeg_set = "";

		// holds the GET request parameters sent to the server
		var get_params = {};

		// determine which set was being loaded in
		// the option value as the value to the key 'file'
		if ( bttn_id === "eeg-source-load-bttn") {
			get_params = { file: $(source_sel).val() };
			eeg_set = "source";
		}
		else if ( bttn_id === "eeg-target-load-bttn") {
			get_params = { file: $(target_sel).val() };
			eeg_set = "target";
		}

		// send a GET request to retrieve sensor statistics
		$.ajax({url: "/load_sensors",
			method: "GET", 
			data: get_params, 
			dataType: "json"})
			.done( function (d) {

			    // parse the response from the server
				var stats = JSON.parse(JSON.stringify(d));

				// clear the area where the data belongs
				if (eeg_set === "source") {
					$(eeg_source_tbl + " > tbody").empty();
				}
				else if (eeg_set === "target") {
					$(eeg_target_tbl + " > tbody").empty();
				}

				// display the data recieved from the server
				for(var sensor in stats){

						// craft table html items to hold the received data
						var tr_html = "<td>" + sensor + "</td>" +
								"<td>" + stats[sensor] + "</td>" +
								'<td><input type="checkbox" name="' +
								eeg_set + '_self" value="' +
								eeg_set + '_' + sensor + '-' +
								stats[sensor] + '" /></td>' +
								'<td><input type="radio" name="' +
								eeg_set + '_cross" value="' +
								eeg_set + '_' + sensor + '-'
								+ stats[sensor] + '" /></td>';

						var new_tr = $('<tr>', { html: tr_html});

						// place the html in the correct section
						if (eeg_set === "source" ) {
							$(eeg_source_tbl + " > tbody").append(new_tr);
						}
						else if (eeg_set === "target") {
							$(eeg_target_tbl + " > tbody").append(new_tr);
						}
				}
			});
	}

	function format_csv(chart_data) {
		var dataset_type = current_chart_band;
		var csv 	= "";

		// chart cross similarity
		if (chart_data.src && chart_data.tgt ) {
			csv = "Index,Src,Tgt\n";

			// determine data with longest length
			var data_max = chart_data["src"][dataset_type]["x"].length;
			if ( data_max < chart_data["tgt"][dataset_type]["x"].length ) {
				data_max = chart_data["tgt"][dataset_type]["x"].length;
			}

			// set up data
			for( var i = 0; i < data_max; i += 1 ) {
				// x
				if (chart_data["src"][dataset_type]["x"][i]) {
					csv = csv + chart_data["src"][dataset_type]["x"][i] + ",";
				}
				else {
					csv = csv + chart_data["tgt"][dataset_type]["x"][i] + ",";
				}


				// y 
				if ( chart_data["src"][dataset_type]["x"][i] ) {
					csv = csv + chart_data["src"][dataset_type]["y"][i] + ",";
				}
				else {
					csv += ",";	
				}
				if ( chart_data["tgt"][dataset_type]["x"][i] ) {
					csv = csv + chart_data["tgt"][dataset_type]["y"][i];
				}

				csv += "\n";
			}

		}
		// otherwise, chart self similarity set
		else {

			//build header row
			csv = "Index";
			for ( var h = 0; h < chart_data.length; h += 1) {
				csv = csv + ",Set " + (h+1);
			}
			csv += "\n";

			// determine data with longest length
			var data_max = chart_data[0][dataset_type]["x"].length;
			var data_max_idx = 0; 
			for (var i = 1; i < chart_data.length; i += 1) {
				if (data_max < chart_data[i][dataset_type]["x"].length ) {
					data_max = chart_data[i][dataset_type]["x"].length;
					data_max_idx = i;
				}
			}
			
			// set up individual data points
			for( var i = 0; i < data_max; i += 1 ) {
				// index
				csv = csv + chart_data[data_max_idx][dataset_type]["x"][i]; 

				// individual sets
				for (var s = 0; s < chart_data.length; s += 1) {
					if ( chart_data[s][dataset_type]["y"].length > i ) 
					{
						csv = csv + "," + chart_data[s][dataset_type]["y"][i]; 
					}
					else {
						csv += ",";	
					}

				}

				csv += "\n";
				
			}

		}

		return csv;
	}

	/*
	Process: build the html for the statistics in d

	d: array of hash_maps
		d[i] = {sensor: { hjorth: {feature: }}}
	 */
	function init_data(ctx, d) {
		// features to calculate
		var features = [ "std_deviation", 
				"msv", 
				"activity",
				"mobility",
				"complexity",
				"skewness",
				"kurtosis",
				"mean" ];

		// variable to hold the table html
		var msv_tbl = 0;
		var set_css_sel = "-set > tbody";

		// select the appropriate css set
		if (ctx === "source") {
			set_css_sel = "-source" + set_css_sel;
		}
		else if (ctx === "target" ) {
			set_css_sel = "-target" + set_css_sel;
		}

		// For each selected feature
		for (var f = 0; f < features.length; f += 1 ) {

			// find the html for the feature
			msv_tbl = $("#" + features[f] + set_css_sel);

			// clear the table html
			msv_tbl.empty();

			// build a table using the statistics in d
			for (var i = 0; i < d.length; i += 1) {
				var tr = "<tr>";

				tr += "<td>" + i + "</td>";
				tr += "<td>" + d[i]["alpha"]["hjorth"][features[f]] + "</td>";
				tr += "<td>" + d[i]["beta"]["hjorth"][features[f]] + "</td>";
				tr += "<td>" + d[i]["gamma"]["hjorth"][features[f]] + "</td>";
				tr += "<td>" + d[i]["theta"]["hjorth"][features[f]] + "</td>";
				tr += "</tr>";

				// set the table to the constructed html
				msv_tbl.html( msv_tbl.html() + tr);
			}

		}

	}

	function init_cosinesim(cs,mlp,svm) {
		$("#cosine-sim").html(cs);
		$("#mlp-class").html(mlp);
		$("#svm-class").html(svm);
	}

	// Chart Drawing UX
	function init_charts() {

		// construct and display the stats in current_eeg
		// as html and display them
		init_data("source", current_eeg["src"]);
		init_data("target", current_eeg["tgt"]);

		console.log(current_eeg);

		// init_cosinesim( current_eeg["cross"]["cosine_sim"],
		// 	current_eeg["cross"]["mlp_class"],
		// 	current_eeg["cross"]["mlp_class"] );

		// clear charts first
		$("#source-self-chart").empty();
		$("#target-self-chart").empty();
		$("#eeg-cross-chart").empty();
		$("#source-self-chart").parent().show();
		$("#target-self-chart").parent().show();
		$("#eeg-cross-chart").parent().show();

		//var cross_dgraph = new Dygraph( document.getElementById("eeg-cross-chart"),
		// 	format_csv(current_eeg.cross),
		// 	{ width: 800 });

		var src_dgraph	= new Dygraph( document.getElementById("source-self-chart"),
				format_csv(current_eeg.src),
				{ width: 800 });

		var tgt_dgraph	= new Dygraph( document.getElementById("target-self-chart"),
				format_csv(current_eeg.tgt),
				{ width: 800 });

		$("#source-self-bttn").addClass("button-success");
		$("#target-self-bttn").removeClass("button-success");
		$("#eeg-cross-bttn").removeClass("button-success");
		$("#source-self-chart").parent().show();
		$("#target-self-chart").parent().hide();
		$("#eeg-cross-chart").parent().hide();
	
	}

	function view_chart(b) {
		var chart_bttn_row	= "eeg-chart-bttn-row";
		var bttn		= $(b.target);

		$("#" + chart_bttn_row + " button").removeClass("button-success");
		bttn.addClass("button-success");

		$(".eeg-chart-row").each( function (i,c) {  $(c).hide()});

		if (bttn.attr("id") === "source-self-bttn") {
			$("#source-self-chart").parent().show();
		}
		else if ( bttn.attr("id") === "target-self-bttn" ) {
			$("#target-self-chart").parent().show();
		}
		else if (bttn.attr("id") === "eeg-cross-bttn" ) {
			$("#eeg-cross-chart").parent().show();
		}

	}

	function switch_chart_band() {
		current_chart_band = $("#band-filters input[type=radio]:checked").val();
		init_charts();
	}

	// END Chart Drawing UX

	function compute_eeg(b) {

		var act = "compute";
		var export_json = 0;

		// make decision to export the data
		if ( b.currentTarget.id.indexOf("exportjson") > 0) {
			export_json = 1;
			
		}
		else if ( b.currentTarget.id.indexOf("export-matlab") > 0 ) {
			act = "export_matlab";
		}

		//source params
		var source_file		= $("#eeg-source-select").val(); // source selection drop down value
		var source_eegs		= [];                            // holds source eeg filenames
		var source_cross	= "";                            // holds the source cross eeg filename

		// for each set in the source list with a checked box, split the set and
		// add it to the source filenames
	 	$("#eeg-source-set input[type=checkbox]:checked").each(function(i,e) {

	 			// extract the sensor tag
	 			var es = e.value.split('_').slice(1);
	 			es = es.join('_');
				es = es.split('-').slice(0,-1);
				es = es.join('-');

				// save the sensor to send to server
				source_eegs.push(es);

	 		});

	 	// for the set with the radio button selected, split and assign it
		// as the source_cross
	 	$("#eeg-source-set input[type=radio]:checked").each(function(i,e) {

	 			// extract the sensor tag
				var es = e.value.split('_').slice(1);
				es = es.join('_');
				es = es.split('-').slice(0,-1);
				es = es.join('-');

				// save the sensor to send to server
				source_cross = es;

			});

		//target params
		var target_file		= $("#eeg-target-select").val(); // target selection drop down value
		var target_eegs 	= [];                            // holds target eeg filenames
		var target_cross	= "";                            // holds the target cross eeg filename

		// for each set in the target list with a checked box, format the value
		// and add it to the target filenames
		$("#eeg-target-set input[type=checkbox]:checked").each(function(i,e) {

				// extract the sensor tag
				var es = e.value.split('_').slice(1);
				es = es.join('_');
				es = es.split('-').slice(0,-1);
				es = es.join('-');

				// save the sensor to send to the server
				target_eegs.push(es);

			});

		// for the set with the radio button selected in the target list, format
		// the value and set it as the target cross filename
	 	$("#eeg-target-set input[type=radio]:checked").each(function(i,e) {

	 			// extract the sensor tag
				var es = e.value.split('_').slice(1);
				es = es.join('_');
				es = es.split('-').slice(0,-1);
				es = es.join('-');

				// save the sensor to send to the server
				target_cross = es;

			});

		//cross similarity params

		// for each frequency band selected in the set of available
		// frequency bands, add it to desired frequency bands used
		// for cross analysis
		var featband_param	= [];
		$("input:checkbox[name=feature_band]:checked").each( function(i,e) {
			featband_param.push(e.value); } );

		// for each feature in the list of available features, add it
		// to the desired features used for cross analysis
		var feature_param	= [];
		$("input:checkbox[name=feature]:checked").each( function(i,e) {
			feature_param.push(e.value); });

		// set the preprocessing algorithm
		var prefreq_param	= $("#eeg-prefreq-select").val();

		// set the desired classification algorithm
		//var classify_param	= $("#eeg-classify-select").val();

		// create a dictionary from the data that was
		// just calculated
		var eeg_params = { src: source_file, 
			src_eegs: source_eegs,
			src_cross: source_cross,
			tgt: target_file,
			tgt_eegs: target_eegs,
			tgt_cross: target_cross,
			feature_band: featband_param,
			prefreq: prefreq_param,
			features: feature_param,
			action: act };
			//, classify: classify_param };


			// skipped analysis
			// TODO: analyze this block of code
			if ( export_json === 1) {
				console.info(eeg_params);
				for ( var k in eeg_params ) {
					//console.info(k + ":" + eeg_params[k]);
					kid = "eegp-" + k;

					if (Array.isArray(eeg_params[k])) {
						var kval = eeg_params[k];
						k += "[]";

						for ( var i = 0; i < kval.length; i += 1) {
							if ( $("#" + kid + "_" + i).length ) {
								$("#" + kid + "_" + i).val(kval[i]);
							}
							else {
								$('<input>').attr({
									type: 'hidden',
									id: kid + "_" + i,
									name: k,
									value: kval[i]}).appendTo("#eeg-compute-form");
							}
						}
					}
					else {
						if ( $("#" + kid).length ) {
							$("#" + kid).val(eeg_params[k]);
						}
						else {
							$('<input>').attr({
								type: 'hidden',
								id: kid,
								name: k,
								value: eeg_params[k]}).appendTo("#eeg-compute-form");
						}

					}
				}
				//b.preventDefault();
			
			}
			// if the compute button was pressed
			else {
				$.ajax({ url: "/get_sensor_data",
					method: "GET",
					data: eeg_params}).done(function(r) {
							var response = JSON.parse(JSON.stringify(r));

							//console.log(response);

							// TODO: discern the format of current eeg hashmap
							alert("Format current EEG data variable correctly in line 480")
							if (act === "compute") {
								current_eeg = response;
								init_charts();
							} else {
								console.info(edata);
							} 
						}); 
			}

	}

	// page load (i.e. 'ready')
	function page_init() {

		// initialize buttons
		var eeg_source_bttn	= "#eeg-source-load-bttn";
		var eeg_target_bttn	= "#eeg-target-load-bttn";
		var eeg_compute_bttn	= "#eeg-compute-bttn";
		var eeg_json_bttn	= "#eeg-exportjson-bttn";
		var eeg_matlab_bttn	= "#eeg-export-matlab-bttn";
		var source_chart_bttn	= "#source-self-bttn";
		var target_chart_bttn	= "#target-self-bttn";
		var cross_chart_bttn	= "#eeg-cross-bttn";

		// ? grab preloaded json files ?
		// $.ajax({url: "/json"}).done(refresh_listing);

		$("#band-filters input[type=radio]").each(function(i,e){ $(e).click(switch_chart_band); });
		$(eeg_compute_bttn).click(compute_eeg);
		$(eeg_json_bttn).click(compute_eeg);
		//$(eeg_matlab_bttn).click(compute_eeg);
		$(eeg_source_bttn).click(load_eeg_set);
		$(eeg_target_bttn).click(load_eeg_set);

		$(source_chart_bttn).click(view_chart);
		$(target_chart_bttn).click(view_chart);
		$(cross_chart_bttn).click(view_chart);

	}

	$(page_init);

}());
