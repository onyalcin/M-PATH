/**
 * jspsych-custom_survey
 * a jspsych plugin that creates two custom surveys
 *
 * 2017 Ulysses Bernardet
 * 
 */

function createTable(ID, levels, items, description) {
    var display_element = $('#jspsych-target'); // won't need this later

    display_element.append($('<div>', {
        "id": ID + 'preamble',
        "class": 'jspsych-custom_survey-preamble'
    }));
    
    $('#' + ID + 'preamble').html(description);
       
    display_element.append($('<div>', {
	"id": "div_" + ID,
	"class": 'div_table_container'
    }));


    $("#div_" + ID).append($('<table>', {
	"id": "table_" + ID,
	"class": 'table_ratings'
    }));

    var table = document.getElementById("table_" + ID);

    var tableheader = document.createElement("thead");
    table.appendChild(tableheader);

    var tr = document.createElement("tr");
    tableheader.appendChild(tr);


    //empty top-left field
    var th = document.createElement("th");
    tr.appendChild(th);


    for (var level in levels) {
	var th = document.createElement("th");
	th.append(levels[level]);
	tr.appendChild(th);
    }

    var tablebody = document.createElement("tbody");
    table.appendChild(tablebody);
    for (var item in items) {
	var tr = document.createElement("tr");
	tablebody.appendChild(tr);
	var td = document.createElement("td");
	td.append(items[item]);
	tr.appendChild(td);

	var ss = items[item];
	var item_ID = ss.replace(/\s/gi, "_").replace(/,/gi, "");

	var td_width = 100. / (levels.length+2);
	for (var ii = 0; ii < levels.length; ii++) {
	    var td = document.createElement("td");
	    td.className  = "td_scale";
	    td.setAttribute("width", td_width + "%");
	    tr.appendChild(td);

	    $(td).append($('<input>', {
		//"id": ID + "_" + item_ID,
		"type": "radio",
		"value": ii,
		"class": 'rb' + item,
		"name": ID + "_" + item_ID
	    }));
	}
    }
}


(function($) {
    jsPsych['custom_survey'] = (function() {

        var plugin = {};

        plugin.create = function(params) {
            params = jsPsych.pluginAPI.enforceArray(params, ['stimuli']);
            
            var trials = new Array(params.stimuli.length);
            for (var i = 0; i < trials.length; i++) {
                trials[i] = {};
                trials[i].type =  "custom_survey";
		trials[i].stimuli = params.stimuli[i];
            }
            return trials;
        };

        plugin.trial = function(display_element, trial) {
            
            trial = jsPsych.pluginAPI.normalizeTrialVariables(trial);

	    var display_element = $('#jspsych-target'); // won't need this later

	    var scales = ["tipi", "affect"];
	    var vitems = [
		["Extraverted, enthusiastic", "Critical, quarrelsome", "Dependable, self-disciplined", "Anxious easily upset", "Open to new experiences, complex", "Reserved, quiet", "Sympathetic, warm", "Disorganized, careless", "Calm, emotionally stable", "Conventional, uncreative"],
		["Surprised, startled, astonished", "Irritated, angry, annoyed, aggravated", "Fearful, afraid, scared", "Sad, dreary, dismal", "Guilty, ashamed", "happy, elated, cheerful, joyful", "Contented, peaceful, mellow, tranquil", "Intelligent", "Healthy"]
	    ];

	    var ID = scales[0];
	    var levels = ["Disagree strongly", "Disagree moderately", "Disagree a little", "Neither agree nor disagree", "Agree a little", "Agree moderately", "Agree strongly"];
	    var items = vitems[0];
	    var description = "How much do you agree with each of the following statements about the person you saw in the video?";
	    createTable(ID, levels, items, description);

	    var ID = scales[1];
	    var levels = ["Not at all", "", "Neutral", "", "Very much"];
	    var items = vitems[1];
	    var description = "Please rate the person in the video:";
	    createTable(ID, levels, items, description);
	    
	    display_element.append($('<button>', {
		'id': 'jspsych-custom_survey-next',
		'class': 'jspsych-custom_survey'
	    }))

	    $("#jspsych-custom_survey-next").html('Submit Answers');

	    $("#jspsych-custom_survey-next").click(function() {
		// measure response time
		
		var endTime = (new Date()).getTime();
		var response_time = endTime - startTime;
		
		var data_surveys = {};
		var data_survey = {};

		data_survey["stimulus"] = trial.stimuli;
		
		for (var scale in scales) {
		    console.log(scales[scale]);
		    var list_items = {};

		    for (var ii in vitems[scale]) {
			var nnn = vitems[scale][ii];
			var vvv = $('#table_' + scales[scale] + ' input:radio[class=rb' + ii + ']:checked').val();
			
			if(vvv === undefined){
    			    alert ("Please complete the questionnaire");
			    return;
			}
			
			console.log("\t" + nnn + ": " + vvv);
			var data_item = {};
			data_item[nnn] = vvv;
			$.extend(list_items, data_item);
		    }
		    data_survey[scales[scale]] = list_items;
		    $.extend(data_surveys, data_survey);
		}

		// save data
		jsPsych.data.write($.extend({}, {
		    "rt": response_time,
		    "responses": JSON.stringify(data_surveys )
		}, trial.data));

		display_element.html('');

		// next trial
		if (trial.timing_post_trial > 0) {
		    setTimeout(function() {
			jsPsych.finishTrial();
		    }, trial.timing_post_trial);
		} else {
		    jsPsych.finishTrial();
		}
	    });
	    var startTime = (new Date()).getTime();
	};

        return plugin;
    })();
})(jQuery);
