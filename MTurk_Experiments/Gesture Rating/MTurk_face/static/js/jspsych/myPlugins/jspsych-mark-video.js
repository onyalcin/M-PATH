/**
 * Josh de Leeuw
 * March 2014
 * 
 * 
 **/


(function($) {
    jsPsych["mark-video"] = (function() {

	
        var plugin = {};

        plugin.create = function(params) {

	    params = jsPsych.pluginAPI.enforceArray(params, ['stimuli', 'data']);
	    
            var trials = new Array(params.stimuli.length);
            for (var i = 0; i < trials.length; i++) {
                trials[i] = {};
                trials[i].stimuli = params.stimuli[i];
                trials[i].key = (typeof params.key === 'undefined') ? 32 : params.key;
		var default_moviesize = [];
		trials[i].movie_size = params.movie_size || default_moviesize;
                // timing parameters
                trials[i].timing_pre_trial = (typeof params.timing_pre_trial === 'undefined') ? 0 : params.timing_pre_trial;
                trials[i].timing_post_trial = (typeof params.timing_post_trial === 'undefined') ? 1000 : params.timing_post_trial;
                // optional parameters
                trials[i].prompt = (typeof params.prompt === 'undefined') ? "" : params.prompt;
                trials[i].data = (typeof params.data === 'undefined') ? {} : params.data[i];
            }
            return trials;
        };

        plugin.trial = function(display_element, trial) {
	   /* document.body.style.backgroundColor = "#000000"; */
	    trial = jsPsych.pluginAPI.normalizeTrialVariables(trial);
	    
            var times = [];

			display_element.append($('<div>', {
                    "id": 'jspsych-mark-video',
                    "class": 'jspsych-mark-video'
			}));
			
				

			$("#jspsych-mark-video").append($('<video>', {
                id: 'jspsych-mark-video-vid',
            }));

            $('#jspsych-mark-video-vid').attr({
                poster: "/static/images/ajax-loader.gif"
            });

            $('#jspsych-mark-video-vid').attr({
                autoplay
            });

	    
	    trial.timing_stim;
	    
            if(typeof trial.movie_size[0] !== 'undefined'){
                $('#jspsych-mark-video-vid').attr({
                    width: trial.movie_size[0],
                    height: trial.movie_size[1]
                });
            }

	    for (var i = 0; i < trial.stimuli.length; i++) {
                $('#jspsych-mark-video-vid').append('<source src="' + trial.stimuli[i] + '">');
            }

            //show prompt here
            if (trial.prompt !== "") {
                display_element.append(trial.prompt);
            }

            // start trial
            if (trial.timing_pre_trial > 0) {
                setTimeout(function() {
                    start_trial();
                }, trial.timing_pre_trial);
            }
            else {
                start_trial();
            }

            function start_trial() {
                $("#jspsych-mark-video-vid").get(0).play();

		$("#jspsych-mark-video-vid").get(0).onended = function(e) {
		    // video is over
		    
		    end_trial();
		    
		    // end trial
		};
            }

            function end_trial() {
		var trial_data = {
		    "stimulus": JSON.stringify(trial.stimuli)
		};
		
		// save data
		jsPsych.data.write($.extend({}, {
		    "responses": JSON.stringify(trial_data)
		}, trial.data));
		
		// clear the display
		display_element.html('');
		
		// move on to the next trial
		if (trial.timing_post_trial > 0) {
		    setTimeout(function() {
			jsPsych.finishTrial();
		    }, trial.timing_post_trial);
		} else {
		    jsPsych.finishTrial();
		}
            }

            var resp_func = function(e) {

                if (e.which == trial.key) {
                    var time = $("#jspsych-mark-video-vid").get(0).currentTime;

                    times.push(time);

                    $("#jspsych-mark-video-vid").css({
                        border: "5px solid black"
                    });

                    var div = $('#jspsych-mark-video-vid');
                    $({
                        alpha: 1
                    }).animate({
                        alpha: 0
                    }, {
                        duration: 500,
                        step: function() {
                            div.css('border-color', 'rgba(0,0,0,' + this.alpha + ')');
                        }
                    });
                }
            };

            $(document).keydown(resp_func);

        };


        return plugin;
    })();
})(jQuery);
