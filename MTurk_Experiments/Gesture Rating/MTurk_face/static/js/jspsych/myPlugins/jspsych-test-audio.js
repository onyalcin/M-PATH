/**
 * Ulysses Bernardet September 2016
 * 
 * 
 **/

(function($) {
    jsPsych["test-audio"] = (function() {
        var plugin = {};
        plugin.create = function(params) {
	    params = jsPsych.pluginAPI.enforceArray(params, ['stimuli', 'data']);
	    
            var trials = new Array(params.stimuli.length);
            for (var i = 0; i < trials.length; i++) {
                trials[i] = {};
                trials[i].stimuli = params.stimuli[i];
		trials[i].questions= params.questions[i];
                trials[i].data = (typeof params.data === 'undefined') ? {} : params.data[i];
            }
            return trials;
        };

        plugin.trial = function(display_element, trial) {
	    display_element.append($('<div>', {
		"id": 'jspsych-test-audioinstructions',
		"class": 'jspsych-test-audio-text',
		'html': "<h2>Test volume settings</h2>Please wear <b>headphones</b> and test that your volume setting are correct; play the sound file below, and ajust the volume to a level that you can hear the voice clearly.<br/> You can listen to the clip as many times as you wish."
	    }))

	    
	    display_element.append($('<div>', {
                "id": 'jspsych-div-audio',
                "class": 'jspsych-div-audio'
	    }));

	    $("#jspsych-div-audio").append($('<audio>', {
                id: 'jspsych-audio',
		class: 'jspsych-audio'
            }));

            $('#jspsych-audio').attr({
		controls: false
            });

            $('#jspsych-audio').append('<source src="' + trial.stimuli[0] + '">');
  
            $("#jspsych-div-audio").append($('<button>', {		
                'id': 'play-audio-button',
	        'class': 'jspsych-audio-button btn btn-primary btn-lg',
		'html': "play audio"
            }));
	    


	    // add questions
	    display_element.append($('<div>', {
		"id": 'test-audio-question',
		"class": 'jspsych-test-audio-text'
	    }));
	    
	    // add question text
	    $("#test-audio-question").append('<p class="test-audio-question">' + trial.questions[0] + '</p>');
	    	    // add text box
	    $("#test-audio-question").append('<input  class="jspsych-text-input" type="text" name="#test-audio-question-response"></input>');
	    
	    
	    display_element.append($('<div>', {
                "id": 'jspsych-compare-button',
                "class": 'jspsych-compare-button'
	    }));

	    // add submit button
//            display_element.append($('<button>', {
	    $("#jspsych-compare-button").append($('<button>', {
                'id': 'jspsych-div-audio-next',
                'class': 'jspsych-div-audio btn btn-primary btn-lg',
		'disabled' : false
            }));

	    
            $("#jspsych-div-audio-next").html('Submit Answers');
            $("#jspsych-div-audio-next").click(function() {
                // measure response time
                var endTime = (new Date()).getTime();
                var response_time = endTime - startTime;

		var trial_data = {
		    "stimulus": JSON.stringify(trial.stimuli)
		};

//		console.log(JSON.stringify(trial.stimuli));

		var test_audio_response = $("#test-audio-question").children('input').val();
//		console.log(JSON.stringify(test_audio_response));
		
		// save data
		jsPsych.data.write($.extend({}, {
		    "rt": response_time,
		    "test-audio-file": JSON.stringify(trial_data),
		    "test-audio-response": JSON.stringify(test_audio_response)
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

	    
	    $("#play-audio-button").click(function() {
//		console.log("click");
		$("#jspsych-audio").get(0).play();
	    });
	    
            var startTime = (new Date()).getTime();
	    
	    start_trial();
	    
	    function start_trial() {
	    };
        }; // end  plugin.trial


        return plugin;
    })();
})(jQuery);
