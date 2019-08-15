/**
 * Ulysses Bernardet October 2016
 * 
 * 
 **/

(function($) {
    jsPsych["rate-image-pd"] = (function() {
        var plugin = {};
        plugin.create = function(params) {
	    params = jsPsych.pluginAPI.enforceArray(params, ['stimuli', 'data']);
	    
            var trials = new Array(params.stimuli.length);
//	    console.log("trials.length", trials.length);
            for (var i = 0; i < trials.length; i++) {
                trials[i] = {};
		trials[i].stimuli = params.stimuli[i];
		var default_imagesize = [];
		trials[i].image_size = params.image_size || default_imagesize;
		trials[i].questions= params.questions[i];
		trials[i].adjectives= params.adjectives[i];
                trials[i].data = (typeof params.data === 'undefined') ? {} : params.data[i];
            }
            return trials;
        };

        plugin.trial = function(display_element, trial) {
	    /* document.body.style.backgroundColor = "#000000"; */
	    //--        var times = [];


	    
	    display_element.append($('<div>', {
                "id": 'jspsych-rate-image',
                "class": 'jspsych-rate-image'
	    }));


	    $("#jspsych-rate-image").append($('<div>', {
                "id": 'divleft',
	    }));

	    
	    $("#divleft").append($('<img>', {
                id: 'jspsych-rate-image-stimulus',
		class: 'jspsych-rate-image-stimulus',
		src: trial.stimuli[0]
            }));

	    	    
            if(typeof trial.image_size[0] !== 'undefined'){
                $('#jspsych-rate-image-stimulus').attr({
                    width: trial.image_size[0],
                    height: trial.image_size[1]
                });
            }


	    $("#jspsych-rate-image").append($('<div>', {
                "id": 'divuserinput',
	    }));
	    
	    
	    for (var i = 0; i < trial.questions.length; i++) {
		$("#divuserinput").append($('<div>', {
		    "id": 'div_q_' + i,
		    "class": 'divhorizontalnarrow'
		}));
		    
		$('#div_q_' + i).append($('<label>', {
		    "for": 'select_' + i,
		    "text":  trial.questions[i] + i,
		    "class": 'image-rate-question-label'
		}));
		
		$('#div_q_' + i).append($('<select>', {
		    "id": 'select_' + i,
		    "class": 'image-rate-pd-select',
		    "name" : 'select_' + i
		}));

		for (var j = 0; j < trial.adjectives[i].length; j++) {
		    $("#select_" + i).append($('<option>', {
			"id": 'select_' + i + '_' + trial.adjectives[i][j],
			"text" : trial.adjectives[i][j]
		    }));
		}
	    }
	    

	    // === add commments field

	    $("#divuserinput").append($('<div>', {
                "id": 'divcomment',
		"class": 'divhorizontal'
	    }));

	    
	    // add question text
	    $("#divcomment").append('<p class="image-rate-question-label">Please enter any comments below</p>');
	    // add text box
	    $("#divcomment").append('<input  class="jspsych-text-input" type="text" name="#jspsych-rate-image-comment-response"></input>');

	    // == end comments field

	    
	    // add submit button

	    $("#divuserinput").append($('<div>', {
                "id": 'divsubmitbutton',
		"class": 'divhorizontalnarrow'
	    }));
	    
            // display_element.append($('<button>', {
	    $("#divsubmitbutton").append($('<button>', {
                'id': 'jspsych-rate-image-next',
//                'class': 'jspsych-rate-image btn btn-primary btn-lg',
		'class': 'jspsych-rate-image'
            }));
	    
	    
	    
            $("#jspsych-rate-image-next").html('Submit Answers');
            $("#jspsych-rate-image-next").click(function() {
                // measure response time
                var endTime = (new Date()).getTime();
                var response_time = endTime - startTime;



		var trial_data = {
		    "stimulus": JSON.stringify(trial.stimuli)
		};
		
		// create object to hold responses
		var question_data = {};
		$("div.jspsych-survey-likert-slider").each(function(index) {
		    var id = "Q" + index;
		    var val = $(this).slider("value");
		    var obje = {};
		    obje[id] = val;
		    $.extend(question_data, obje);
		});
		
		var jspsych_image_rate_comment = $("#jspsych-rate-image-comment").children('input').val();
		console.log(jspsych_image_rate_comment);
		
		// save data
		jsPsych.data.write($.extend({}, {
		    "rt": response_time,
		    "responses": JSON.stringify(question_data),
		    "image": JSON.stringify(trial_data),
		    "comment": JSON.stringify(jspsych_image_rate_comment)

		}, trial.data));
		
		
		display_element.html('');

		if (trial.timing_post_trial > 0) {
		    setTimeout(function() {
			jsPsych.finishTrial();
		    }, trial.timing_post_trial);
		} else {
		    jsPsych.finishTrial();
		}

		
            });

	    
  
            var startTime = (new Date()).getTime();
	    
	    start_trial();
	    
	    function start_trial() {
		/* put pre-trial code here */
	    };
        }; // end  plugin.trial


        return plugin;
    })();
})(jQuery);
