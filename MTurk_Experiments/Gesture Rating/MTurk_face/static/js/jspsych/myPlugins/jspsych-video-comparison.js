/**
 * based on code from Josh de Leeuw
 * Ulysses Bernardet July 2016
 * 
 * 
 **/

(function($) {
    jsPsych["video-comparison"] = (function() {
        var plugin = {};
        plugin.create = function(params) {
	    params = jsPsych.pluginAPI.enforceArray(params, ['stimuli', 'data']);
	    
            var trials = new Array(params.stimuli.length);
//	    console.log("trials.length", trials.length);
            for (var i = 0; i < trials.length; i++) {
                trials[i] = {};
                trials[i].stimuli = params.stimuli[i];
//--                trials[i].key = (typeof params.key === 'undefined') ? 32 : params.key;
		var default_moviesize = [];
		trials[i].movie_size = params.movie_size || default_moviesize;
		//--                trials[i].prompt = (typeof params.prompt === 'undefined') ? "" : params.prompt;
		trials[i].preamble = (typeof params.preamble === 'undefined') ? "" : params.preamble[i],
		trials[i].questions= params.questions[i];
		trials[i].labels= params.labels[i];
		trials[i].intervals= params.intervals[i];
		trials[i].show_ticks= (typeof params.show_ticks == 'undefined') ? true : params.show_ticks;
                trials[i].data = (typeof params.data === 'undefined') ? {} : params.data[i];
            }
            return trials;
        };

        plugin.trial = function(display_element, trial) {
	    /* document.body.style.backgroundColor = "#000000"; */
	    //--        var times = [];


	    
	    display_element.append($('<div>', {
                "id": 'jspsych-compare-videos',
                "class": 'jspsych-compare-videos'
	    }));


	    $("#jspsych-compare-videos").append($('<div>', {
                "id": 'divleft',
	    }));

	    
	    $("#divleft").append($('<video>', {
                id: 'jspsych-compare-videos-vid1',
		class: 'jspsych-compare-videos-video'
            }));

            $('#jspsych-compare-videos-vid1').attr({
                poster: "/static/images/video_poster1.png"
            });


	    $("#jspsych-compare-videos").append($('<div>', {
                "id": 'divright',
	    }));
	    
	    
	    $("#divright").append($('<video>', {
                id: 'jspsych-compare-videos-vid2',
		class: 'jspsych-compare-videos-video'
            }));
	    
            $('#jspsych-compare-videos-vid2').attr({
                poster: "/static/images/video_poster2.png"
            });

   
            if(typeof trial.movie_size[0] !== 'undefined'){
                $('#jspsych-compare-videos-vid1').attr({
                    width: trial.movie_size[0],
                    height: trial.movie_size[1]
                });
                $('#jspsych-compare-videos-vid2').attr({
                    width: trial.movie_size[0],
                    height: trial.movie_size[1]
                });

            }

	    //set the sources of the videos
            $('#jspsych-compare-videos-vid1').append('<source src="' + trial.stimuli[0] + '.mp4"> type="video/mp4"');
            $('#jspsych-compare-videos-vid1').append('<source src="' + trial.stimuli[0] + '.ogv"> type="video/ogg"');

	    $('#jspsych-compare-videos-vid2').append('<source src="' + trial.stimuli[1] + '.mp4"> type="video/mp4"');
	    $('#jspsych-compare-videos-vid2').append('<source src="' + trial.stimuli[1] + '.ogv"> type="video/ogg"');
	    
	    $("#divleft").append($('<button>', {
                'id': 'play-vid1',
	        'class': 'jspsych-compare-videos btn btn-primary btn-lg',
		'html': "play"
            }));
	    
	    $("#divright").append($('<button>', {
                'id': 'play-vid2',
		'class': 'jspsych-compare-videos btn btn-primary btn-lg',
		'html': "play",
		'disabled' : true
            }));

	    
	    // show preamble text
	    display_element.append($('<div>', {
		"id": 'jspsych-survey-likert-preamble',
		"class": 'jspsych-survey-likert-preamble'
	    }));
	    
	    $('#jspsych-survey-likert-preamble').html(trial.preamble);
	    
	    
	    // ======== ADDING THE LIKER SCALE
	    for (var i = 0; i < trial.questions.length; i++) {
		// create div
		display_element.append($('<div>', {
		    "id": 'jspsych-survey-likert-' + i,
		    "class": 'jspsych-survey-likert-question'
		}));

		// add question text
		$("#jspsych-survey-likert-" + i).append('<p class="jspsych-survey-likert-text survey-likert">' + trial.questions[i] + '</p>');

		// create slider
		$("#jspsych-survey-likert-" + i).append($('<div>', {
		    "id": 'jspsych-survey-likert-slider-' + i,
		    "class": 'jspsych-survey-likert-slider jspsych-survey-likert'
		}));
		$("#jspsych-survey-likert-slider-" + i).slider({
		    value: Math.ceil(trial.intervals[i] / 2),
		    min: 1,
		    max: trial.intervals[i],
		    step: 1
		});

		// show tick marks
		if (trial.show_ticks) {
		    $("#jspsych-survey-likert-" + i).append($('<div>', {
			"id": 'jspsych-survey-likert-sliderticks' + i,
			"class": 'jspsych-survey-likert-sliderticks jspsych-survey-likert',
			"css": {
			    "position": 'relative'
			}
		    }));
		    for (var j = 1; j < trial.intervals[i] - 1; j++) {
			$('#jspsych-survey-likert-slider-' + i).append('<div class="jspsych-survey-likert-slidertickmark"></div>');
		    }

		    $('#jspsych-survey-likert-slider-' + i + ' .jspsych-survey-likert-slidertickmark').each(function(index) {
			var left = (index + 1) * (100 / (trial.intervals[i] - 1));
			$(this).css({
			    'position': 'absolute',
			    'left': left + '%',
			    'width': '1px',
			    'height': '100%',
			    'background-color': '#222222'
			});
		    });
		}

		// create labels for slider
		$("#jspsych-survey-likert-" + i).append($('<ul>', {
		    "id": "jspsych-survey-likert-sliderlabels-" + i,
		    "class": 'jspsych-survey-likert-sliderlabels survey-likert',
		    "css": {
			"width": "100%",
			"margin": "10px 0px 0px 0px",
			"padding": "0px",
			"display": "inline-block",
			"position": "relative",
			"height": "2em"
		    }
		}));

		for (var j = 0; j < trial.labels[i].length; j++) {
		    $("#jspsych-survey-likert-sliderlabels-" + i).append('<li>' + trial.labels[i][j] + '</li>');
		}

		// position labels to match slider intervals
		var slider_width = $("#jspsych-survey-likert-slider-" + i).width();
		var num_items = trial.labels[i].length;
		var item_width = slider_width / num_items;
		var spacing_interval = slider_width / (num_items - 1);

		$("#jspsych-survey-likert-sliderlabels-" + i + " li").each(function(index) {
		    $(this).css({
			'display': 'inline-block',
			'width': item_width + 'px',
			'margin': '0px',
			'padding': '0px',
			'text-align': 'center',
			'position': 'absolute',
			'left': (spacing_interval * index) - (item_width / 2)
		    });
		});
	    }
	    // ======== END LIKER SCALE


	    // === add commments field

	    display_element.append($('<div>', {
		"id": 'jspsych-compare-videos-comment',
		"class": 'jspsych-survey-likert-text'
	    }));
	    
	    // add question text
	    $("#jspsych-compare-videos-comment").append('<p class="jspsych-survey-likert-text">Please enter any comments below</p>');
	    // add text box
	    $("#jspsych-compare-videos-comment").append('<input  class="jspsych-text-input" type="text" name="#jspsych-compare-videos-comment-response"></input>');

	    // == end comments field
	    
	    display_element.append($('<div>', {
                "id": 'jspsych-compare-button',
                "class": 'jspsych-compare-button'
	    }));


	    

	    // add submit button
//            display_element.append($('<button>', {
	    $("#jspsych-compare-button").append($('<button>', {
                'id': 'jspsych-compare-videos-next',
//                'class': 'jspsych-compare-videos btn btn-primary btn-lg',
                'class': 'jspsych-compare-videos',
		'disabled' : true
            }));


	    $('#jspsych-compare-videos-next').addClass('disabled');
	    
	    
            $("#jspsych-compare-videos-next").html('Submit Answers');
            $("#jspsych-compare-videos-next").click(function() {
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
		
		var jspsych_video_comparison_comment = $("#jspsych-compare-videos-comment").children('input').val();
		console.log(jspsych_video_comparison_comment);
		
		// save data
		jsPsych.data.write($.extend({}, {
		    "rt": response_time,
		    "responses": JSON.stringify(question_data),
		    "videos": JSON.stringify(trial_data),
		    "comment": JSON.stringify(jspsych_video_comparison_comment)

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

	    
	    $("#play-vid1").click(function() {
//		console.log("click");
		$("#jspsych-compare-videos-vid1").get(0).play();
		$('#jspsych-compare-videos-vid1').attr({
                    poster: "/static/images/ajax-loader.gif"
		});
	    });
	    
	    $("#play-vid2").click(function() {
//		console.log("click");
		$("#jspsych-compare-videos-vid2").get(0).play();
		$('#jspsych-compare-videos-vid2').attr({
                    poster: "/static/images/ajax-loader.gif"
		});
	    });

   
            var startTime = (new Date()).getTime();
	    
	    start_trial();
	    
	    function start_trial() {
		/* this block works for auto playing the videos in sequence 
	    	$("#jspsych-compare-videos-vid1").get(0).play();
	    	$("#jspsych-compare-videos-vid1").get(0).onended = function(e) {
		    $("#jspsych-compare-videos-vid2").get(0).play();
		    $("#jspsych-compare-videos-vid1").get(0).load();
	    	};
		$("#jspsych-compare-videos-vid2").get(0).onended = function(e) {
		    $("#jspsych-compare-videos-vid2").get(0).load();
		    $("#jspsych-compare-videos-next").disabled=false;
		    $('#jspsych-compare-videos-next').removeAttr('disabled');
		    $('#jspsych-compare-videos-next').removeClass('disabled');
	    	};
		*/


		var bVideo1Played = false;
		var bVideo2Played = false;
		
	    	$("#jspsych-compare-videos-vid1").get(0).onended = function(e) {
		    $("#jspsych-compare-videos-vid1").get(0).load();
		    $('#play-vid1').addClass('disabled');
		    $("#play-vid1").attr("disabled", "true");

		    $("#play-vid2").disabled=false;
		    $('#play-vid2').removeAttr('disabled');
		    $('#play-vid2').removeClass('disabled');
		    
		    $('#jspsych-compare-videos-vid1').attr({
			poster: "/static/images/video_poster1.png"
		    });

		    
		    bVideo1Played = true;
		    if(bVideo1Played && bVideo2Played){
			$("#jspsych-compare-videos-next").disabled=false;
			$('#jspsych-compare-videos-next').removeAttr('disabled');
			$('#jspsych-compare-videos-next').removeClass('disabled');
		    }
	    	};
		$("#jspsych-compare-videos-vid2").get(0).onended = function(e) {
		    $("#jspsych-compare-videos-vid2").get(0).load();
		    $('#play-vid2').addClass('disabled');
		    $("#play-vid2").attr("disabled", "true");
		    bVideo2Played = true;

		    $('#jspsych-compare-videos-vid2').attr({
			poster: "/static/images/video_poster2.png"
		    });

		    
		    if(bVideo1Played && bVideo2Played){
			$("#jspsych-compare-videos-next").disabled=false;
			$('#jspsych-compare-videos-next').removeAttr('disabled');
			$('#jspsych-compare-videos-next').removeClass('disabled');
		    }
	    	}; 

		
		
		
	    };
        }; // end  plugin.trial


        return plugin;
    })();
})(jQuery);
