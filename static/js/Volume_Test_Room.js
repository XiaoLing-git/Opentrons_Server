function Fixture_list(target){
	$.ajax({url:"http://127.0.0.1:8000/VQ1/room?room_id=" + target,async:true,success:function(result){
		var data = result
		var id = "#"+"room" + target
		// console.log(id)
		var $table_tbody = $(id +" table tbody")
		// console.log($table_tbody)
		for(x in data){
			$table_tbody.append("<tr id='"+x+"'></tr>");
			var $table_tr = $("#" + x)
			
			$table_tr.append('<td class="td-special Fixture">'+ x +'</td>')
					.append('<td class="td-special pipette">'+ data[x][0] +'</td>')
					.append('<td class="td-special scale">'+ data[x][1] +'</td>')
					.append('<td class="td-special Temperature">None</td>')
					.append('<td class="td-special Humidity">None</td>')
					.append('<td class="td-special State">State</td>')		
		}		 
	}});
};


function Fixture_state(target){
	$.ajax({url:"http://127.0.0.1:8000/VQ1/fixture_state?room_id=" + target,async:true,success:function(result){
		var data = result
		for(x in data){
			var $td = $("#"+x+"> .State")
			// console.log(data[x])
			$td.html(data[x][0])
			$td.removeClass()
			$td.addClass(data[x][0])
			$td.addClass("td-special State")
			
			var $td = $("#"+x+"> .Temperature")
			// console.log(x)
			$td.html(data[x][1])
			$td.removeClass()
			if(data[x][1]>21.5){
				$td.addClass("wraming")
			}
			if(data[x][1]<21){
				$td.addClass("wraming")
			}
			// $td.addClass(data[x])
			$td.addClass("td-special Temperature")
			
			var $td = $("#"+x+"> .Humidity")
			// console.log(x)
			$td.html(data[x][2])
			$td.removeClass()
			if(data[x][1]>57){
				$td.addClass("wraming")
			}
			if(data[x][1]<56){
				$td.addClass("wraming")
			}
			$td.addClass("td-special Humidity")
				
		}		 
	}});
};


Fixture_list(1);
Fixture_list(2);

Fixture_state(1);
Fixture_state(2);

var t1 = window.setInterval('Fixture_state(1)',2000);
var t2 = window.setInterval('Fixture_state(2)',2000);
// window.clearInterval(t1);