/**
 * jspsych-survey-text
 * a jspsych plugin for free response survey questions
 *
 * Josh de Leeuw
 *
 * documentation: docs.jspsych.org
 *
 */

(function($) {
  jsPsych['survey-text'] = (function() {

    var plugin = {};

    plugin.create = function(params) {

      params = jsPsych.pluginAPI.enforceArray(params, ['data']);

      var trials = [];
      for (var i = 0; i < params.questions.length; i++) {
        trials.push({
          preamble: typeof params.preamble == 'undefined' ? "" : params.preamble[i],
          questions: params.questions[i]
        });
      }
      return trials;
    };

    plugin.trial = function(display_element, trial) {

      // if any trial variables are functions
      // this evaluates the function and replaces
      // it with the output of the function
      trial = jsPsych.pluginAPI.normalizeTrialVariables(trial);

      // show preamble text
      display_element.append($('<div>', {
        "id": 'jspsych-survey-likert-preamble',
        "class": 'jspsych-survey-likert-preamble'
      }));

      $('#jspsych-survey-likert-preamble').html(trial.preamble);

      // add questions
      for (var i = 0; i < trial.questions.length; i++) {
        // create div
        display_element.append($('<div>', {
          "id": 'jspsych-survey-text-' + i,
          "class": 'jspsych-survey-text-question'
        }));

        // add question text
        $("#jspsych-survey-text-" + i).append('<p class="jspsych-survey-text">' + trial.questions[i] + '</p>');

        // add text box
        $("#jspsych-survey-text-" + i).append('<input type="text" name="#jspsych-survey-text-response-' + i + '"></input>');
      }

      // add submit button
      display_element.append($('<button>', {
        'id': 'jspsych-survey-text-next',
        'class': 'jspsych-survey-text'
      }));
      $("#jspsych-survey-text-next").html('Submit Answers');
      $("#jspsych-survey-text-next").click(function() {
        // measure response time
        var endTime = (new Date()).getTime();
        var response_time = endTime - startTime;

        // create object to hold responses
        var question_data = {};
        $("div.jspsych-survey-text-question").each(function(index) {
          var id = "Q" + index;
          var val = $(this).children('input').val();
          var obje = {};
          obje[id] = val;
          $.extend(question_data, obje);
        });

        // save data
        jsPsych.data.write($.extend({}, {
          "rt": response_time,
          "responses": JSON.stringify(question_data)
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
