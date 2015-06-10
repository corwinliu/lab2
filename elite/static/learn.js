//var cur_num = 0;
var data_rec; //data from ajax（json格式）
var data_send = {};
var result = [];

var cur_state = 0;  //to avoid users press the shortcut key while not in the corresponding state

function ajax_post_json(target, json){
    $.ajax({
      type: 'POST',
      url: target,
      data: JSON.stringify (json), // or JSON.stringify ({name: 'jonas'}),
      //success: function(d) { alert('data: ' + d); },
      contentType: "application/json",
      dataType: 'text'
    });
}

function get_words(){
    	var is_render = arguments[0] ? arguments[0] : true;
    	$.getJSON("ajax/getwords/", function(json){
     	 	data_rec = json;
     		 if (json['num'] == 0){
       			 end_learn();
     		 }
      		else{
       			data_rec['cur_num'] = 0;
        			data_send = {};
        			data_send.num = data_rec['num'];
        			if (is_render){
          				tmpl_render_html("#judge_tmpl", "#main", data_rec);
          				tmpl_render_html("#progress_tmpl", "#state", data_rec);
        			}
      		}
   	});
}

  /**
   * 使用jsrender模板tmpl，以及数据d，对target处的网页进行渲染
   */
function tmpl_render_html(tmpl, target, d){
    	var html = $(tmpl).render(d);
    	$(target).html(html);
}

function changestate(continue_learn){
      if(cur_state == 0)cur_state = 1; 
      else if(cur_state == 1){
            if(continue_learn)cur_state = 2;
            else cur_state = 0;
      }else if(cur_state == 2)cur_state = 0;
}

function update_status(feedback){
    	status = data_rec['words'][data_rec['cur_num']]['status'];
   	 if (status == "dont"){
              data_rec['dont'] -= 1;
     		 if (feedback == true) {
                  status = "done"; 
                  data_rec['done'] += 1;
              }else{
                  status = "cant";
                  data_rec['cant'] += 1;
              }
   	}
   	else if (status == "cant"){
    		if (feedback == true){
                  status = "need";
                  data_rec['cant'] -= 1;
                  data_rec['need'] += 1;  
              }else{
                  status = "cant";
              } 
  	}
    	else if (status == "need"){
    	  	data_rec['need'] -= 1;
            if (feedback == true){
                    status = "done"; 
                    data_rec['done'] += 1;
              }else{
                    status = "cant";
                    data_rec['cant'] += 1;
              }
    	}
    	data_rec['words'][data_rec['cur_num']]['status'] = status;
}

function smoothAdd(id, cur_vocab){
        var el = $('#' + id);
        var h = el.height();

	 el.css({
		height:   h,
		overflow: 'hidden'
	 });

	 var ulPaddingTop    = parseInt(el.css('padding-top'));
	 var ulPaddingBottom = parseInt(el.css('padding-bottom'));
      
        var status = cur_vocab['status']; 

        if(status == "dont"){
              el.prepend('<li class=\'text-danger\'>' + cur_vocab['english_word'] + '&nbsp;' +  cur_vocab['chinese_explanation'] + '</li>');
        }else if(status == "cant"){
              el.prepend('<li class=\'text-warning\'>' + cur_vocab['english_word'] + '&nbsp;' + cur_vocab['chinese_explanation']  + '</li>');
        }else if(status == "need"){
              el.prepend('<li class= \'text-info\'>' + cur_vocab['english_word'] + '&nbsp;' + cur_vocab['chinese_explanation']  + '</li>');
        }else{
	       el.prepend('<li class=\'text-success\'> ' + cur_vocab['english_word'] + '&nbsp;' + cur_vocab['chinese_explanation']  + '</li>');
	 }

	 var first = $('li:first', el);
	 var last  = $('li:last',  el);

	 var foh = first.outerHeight();

	 var heightDiff = foh - last.outerHeight();
	 var oldMarginTop = first.css('margin-top');
	
	 first.css({
		marginTop: 0 - foh,
		position:  'relative',
		top:       0 - ulPaddingTop
	 });

	 last.css('position', 'relative');

	 el.animate({ height: h + heightDiff }, 150)

	 first.animate({ top: 0 }, 50, function() {
		first.animate({ marginTop: oldMarginTop }, 80, function() {
			last.animate({ top: ulPaddingBottom }, 50, function() {
                          last.remove();
				el.css({
					height:   'auto',
					overflow: 'visible'
				});
			});
		});
	 });

}



function know(){
      result.push(1);
      update_status(true);
      changestate(false);
      tmpl_render_html("#show_tmpl", "#main", data_rec);
      tmpl_render_html("#progress_tmpl", "#state", data_rec);
      smoothAdd('scroller',data_rec['words'][data_rec['cur_num']]);
}

function dont_know(){
      result.push(0);
      update_status(false);
      changestate(false);
      tmpl_render_html("#show_tmpl", "#main", data_rec);
      tmpl_render_html("#progress_tmpl", "#state", data_rec);
      smoothAdd('scroller',data_rec['words'][data_rec['cur_num']]);
}

function continue_learn(){
   	data_send.result = result;
    	//ajax_post_json('ajax/test/', data_send);
      changestate(false);
    	 tmpl_render_html("#load_tmpl", "#main");
       tmpl_render_html("#progress_tmpl", "#state", data_rec);

    	$.ajax({
    	  	type: 'POST',
      		url: 'ajax/test/',
      		data: JSON.stringify (data_send), // or JSON.stringify ({name: 'jonas'}),
      		success: function(d) {result = []; get_words();  data_rec['cur_num'] = 0;},
      		contentType: "application/json",
      		dataType: 'text'
    	});
}

function next_word(){
    	//if (data_rec['words'][data_rec['cur_num']]['status'] == "done") data_rec['done'] += 1;
    	data_rec['cur_num'] += 1;
    	tmpl_render_html("#progress_tmpl", "#state", data_rec);

    	if (data_rec['cur_num'] >= data_rec['num']){
               changestate(true);
    		  tmpl_render_html("#summary_tmpl", "#main");
    	}
    	else{
              changestate(false);
      		tmpl_render_html("#judge_tmpl", "#main", data_rec);
    	}
}

function end_learn(){
        tmpl_render_html("#end_tmpl", "#main");
        tmpl_render_html("#progress_tmpl", "#state",data_rec);
}


window.onkeydown = function(evt){
      evt = evt || window.event;
      //alert(evt.keyCode);
      var keyCode = evt.keyCode; 

      if(cur_state == 0){
              if(keyCode == 49 || keyCode == 97){
                      know();
              }else if(keyCode == 50 || keyCode == 98){
                      dont_know();
              }
      }else if(cur_state == 1){
              if(keyCode == 39){
                      next_word();
              }
      }else if(cur_state == 2){
              if(keyCode == 32){
                    continue_learn();
              }
      }
};

