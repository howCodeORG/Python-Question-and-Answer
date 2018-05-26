// using jQuery
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
}

$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});

$('#answer_question').click(function(e) {
    e.preventDefault();
    $.post(
        "/ajax-answer-question",
        JSON.stringify({
        answer: $("#answer").val(),
        posted_by: $("#posted_by").val(),
        qid: $("#qid").val(),
        }),
        function(data, success) {
        	if (data["Success"]) {
                var answer = '<p class="answer">' + $("#answer").val() + '</p><p class="answerdetails"><span style="float: left"></span><span style="float: right">Posted by <strong>' + $("#posted_by").val() + '</strong></span></p>';
                $('#answers').append(answer)

            } else {
                console.log("Error")
            }
        }
    );
});

$(document).ready(function() {

});
