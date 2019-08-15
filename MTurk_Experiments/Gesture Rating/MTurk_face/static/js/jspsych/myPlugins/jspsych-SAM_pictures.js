/**
 * jspsych-SAM_pictures
 * a jspsych plugin for measuring items on SAM scale
 *
 * Ozge Nilay Yalcin
 * 
 */


(function($) {
    jsPsych['SAM_pictures'] = (function() {

        var plugin = {};

        plugin.create = function(params) {
            
            params = jsPsych.pluginAPI.enforceArray(params, ['stimuli', 'data', 'question', 'options']);
            
            var trials = new Array(params.stimuli.length);
            for (var i = 0; i < trials.length; i++) {
                trials[i] = {};
                trials[i].type =  "SAM_pictures";
                trials[i].a_path = params.stimuli[i];
		trials[i].stimulus_type = params.data[i].stimulus_type;
                trials[i].data = (typeof params.data === 'undefined') ? {} : params.data[i];
                trials[i].question = params.question;
                trials[i].options = params.options
            }
            return trials;
        };

        plugin.trial = function(display_element, trial) {
            
            trial = jsPsych.pluginAPI.normalizeTrialVariables(trial);

            trial.questions = ["Valence", "Arousal", "Dominance"];

	    var radiobutton_size = 15;

            trial.intervals = [7,7,7];

         var video_html = '<video id="jspsych-SAM-pictures-stimulus" width="80%" height="auto" '
         video_html += "autoplay controls >"
         video_html+='<source src="'+trial.a_path
         video_html+='" type="video/mp4">'
         video_html +="</video>"

         display_element.append(video_html);

        var text_html = '<div id="explanation"> Please rate the video using the three categories below. Don\'t think too much about it, just rate what you think the video shows. </div>'
        display_element.append(text_html)

        

            // add likert scale questions
            for (var i = 0; i < trial.questions.length; i++) {


//                // create div
                display_element.append($('<div>', {
                    "id": 'jspsych-SAM_pictures-' + i,
                    "class": 'jspsych-SAM_pictures-question',
			"css" : {
			    "text-align": "center"
			}
                }));

                $("#jspsych-SAM_pictures-" + i).append($('<img>',{
                id:'jspsych-SAM_axis-' + trial.questions[i],
                align: "center",
                src: '/static/images/' + trial.questions[i] + 'Axis.png'
                })                
                );

                $("#jspsych-SAM_pictures-" + i).append($('<table>', {
		    border: '0',
		    cellpadding: '0px',
		    cellspacing: '0px',
//		    width: '100%',
		    //		    align: "center",
                    id: 'jspsych-SAM_table-'  + trial.questions[i],
		    "css": {
			width: "80%",
			"margin-left": "10%", 
			"margin-right": "10%",
			"line-height": "1em"
		    }
		}));
		
		
		$("#jspsych-SAM_table-" + trial.questions[i]).append($('<tr>', {
		    id: 'jspsych-SAM_imgs-'  + trial.questions[i],
		    align: "center",
		}));
		
		
		$("#jspsych-SAM_table-" + trial.questions[i]).append($('<tr>', {
		    id: 'jspsych-SAM_btns-'  + trial.questions[i],
		    align: "center"
		}));
		
		
		for (var j = 0; j < trial.intervals[i]; j++) {
		    $("#jspsych-SAM_imgs-" + trial.questions[i]).append($('<td>', {
			id: "jspsych-SAM_imgs-" + trial.questions[i] + '_' + j
		    }));
		    
		    var sw = $("#jspsych-SAM-pictures-stimulus").width() / trial.intervals[0] +20;
		    
		    $("#jspsych-SAM_imgs-" + trial.questions[i] + '_' + j).append($('<img>', {
			src: '/static/images/SAM-' + trial.questions[i] + '-7_' + j + '.png',
			width: '100%'
		    }));

		    $("#jspsych-SAM_btns-" + trial.questions[i]).append($('<td>', {
			id: "jspsych-SAM_btns-" + trial.questions[i] + '_' + j
		    }));


		    $("#jspsych-SAM_btns-" + trial.questions[i] + '_' + j).append($('<input>', {
			"type": 'radio',
			"id": "jspsych-SAM_form-" + trial.questions[i] + '-index-' + j,
			"name": "radio-" + trial.questions[i],
			"value": j,
			"css":{
			    "width" : radiobutton_size + 'px',
			    "height" : radiobutton_size + 'px'
			}
		    }));
		}

            }

var survey_question = '<div id="survey"><p />'+ trial.question+ ' </div>'
        var survey_options= '<form>'
        for (var i = 0; i < trial.options.length; i++) {
                survey_question +='<input type="radio" name="choice-'+trial.options[i]+'" value="'+ trial.options[i]+ '">' + trial.options[i] +'<br>'
}

survey_options += '</form>'
survey_question +=survey_options

display_element.append(survey_question)

            // add submit button
            display_element.append($('<button>', {
                'id': 'jspsych-SAM_pictures-next',
                'class': 'jspsych-SAM_pictures btn btn-primary btn-lg'
            }));
            $("#jspsych-SAM_pictures-next").html('Submit Answers');
            $("#jspsych-SAM_pictures-next").click(function() {
                // measure response time
                var endTime = (new Date()).getTime();
                var response_time = endTime - startTime;

		
                var question_data_SAM = {};
		for (var i = 0; i < trial.questions.length; i++) {
                    var id = trial.questions[i];
		    var val=-99;
		    var radios = document.getElementsByName('radio-' + trial.questions[i]);
		    for (var j = 0, length = radios.length; j < length; j++) {
			if (radios[j].checked) {
			    val = j;
			    break;
			}
		    }
		    var obje_val = {};
                    obje_val[id] = val;
                    $.extend(question_data_SAM, obje_val);
		}

                //adding emotion data
                var question_data_emotion = "";
		for (var i = 0; i < trial.options.length; i++) {
                    var radios = document.getElementsByName('choice-' +trial.options[i]);
		    if (radios[0].checked) {
                            question_data_emotion = trial.options[i];
			    break;
			}
		}


                // save data 
                jsPsych.data.write($.extend({}, {
                    "rt": response_time,
		    "stimulus": trial.a_path,
		    "responses": JSON.stringify(question_data_SAM),
                    "emotion": question_data_emotion
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
        };

        return plugin;
    })();
})(jQuery);
