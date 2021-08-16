function Fixture_list(target) {
	$.ajax({
		url: "http://127.0.0.1:8000/VQ1/room?room_id=" + target,
		async: true,
		success: function(result) {
			var data = result
			var id = "#" + "room" + target
			// console.log(id)
			var $table_tbody = $(id + " table tbody")
			// console.log($table_tbody)
			for (x in data) {
				$table_tbody.append("<tr id='" + x + "'></tr>");
				var $table_tr = $("#" + x)

				$table_tr.append('<td class="td-special Fixture">' + x + '</td>')
					.append('<td class="td-special pipette">' + data[x][0] + '</td>')
					.append('<td class="td-special scale">' + data[x][1] + '</td>')
					.append('<td class="td-special Temperature">None</td>')
					.append('<td class="td-special Humidity">None</td>')
					.append('<td class="td-special State">State</td>')
			}
		}
	});
};


function Fixture_state(target) {
	$.ajax({
		url: "http://127.0.0.1:8000/VQ1/fixture_state?room_id=" + target,
		async: true,
		success: function(result) {
			var data = result
			for (x in data) {
				var $td = $("#" + x + "> .State")
				// console.log(data[x])
				$td.html(data[x][0])
				$td.removeClass()
				$td.addClass(data[x][0])
				$td.addClass("td-special State")

				var $td = $("#" + x + "> .Temperature")
				// console.log(x)
				$td.html(data[x][1])
				$td.removeClass()
				if (data[x][1] > 21.5) {
					$td.addClass("wraming")
				}
				if (data[x][1] < 21) {
					$td.addClass("wraming")
				}
				// $td.addClass(data[x])
				$td.addClass("td-special Temperature")

				var $td = $("#" + x + "> .Humidity")
				// console.log(x)
				$td.html(data[x][2])
				$td.removeClass()
				if (data[x][1] > 57) {
					$td.addClass("wraming")
				}
				if (data[x][1] < 56) {
					$td.addClass("wraming")
				}
				$td.addClass("td-special Humidity")

			}
		}
	});
};


function Date_list() {
	$.ajax({
		url: "http://127.0.0.1:8000/VQ1/date_list/",
		async: true,
		success: function(result) {
			var data = result["date_list"]
			var $Testdate = $(".Test_date>ul")
			for (x in data) {
				$Testdate.append("<li id=" + data[x] + "><a>" + data[x] + "</a></li>")
				var $Testdateli = $(".Test_date>ul>li")
				$("#" + data[x]).click(function() {
					$Testdateli.removeClass("active")
					$(this).addClass("active")
					get_pipette_list()
				})
			}
			$Testdateli.eq(0).addClass("active")
			get_pipette_list()
		}
	});
}


function set_pipette_active() {
	var $pipettemodel = $(".pipette_model>ul>li")
	for (i = 0; i < $pipettemodel.length; i++) {
		$pipettemodel.eq(i).click(function() {
			$pipettemodel.removeClass("active")
			$(this).addClass("active")
		})
	}
	// console.log($pipettemodel.length)
}



function get_pipette_list() {
	var $pipettemodel = $(".pipette_model>ul>.active")
	// console.log($pipettemodel.text())
	var $Test_date = $(".Test_date>ul>.active")
	// console.log($Test_date.text())
	var $files_list = $(".files_list>ul")
	$files_list.html(null)

	$.ajax({
		url: "http://127.0.0.1:8000/VQ1/pipette_list/?date=" + $Test_date.text() + "&model=" + $pipettemodel.text(),
		async: true,
		success: function(result) {
			data = result["pipettes_list"]
			for (x in data) {
				$files_list.append("<li><a href= http://127.0.0.1:8000/VQ1/download/?date=" + $Test_date.text()+"&file_name="+data[x]+" download="+data[x]+" >"+data[x]+"</a></li>")
			}
			// add_listen_to_file()
		}
	});

}


function add_listen_to_file(){
	var $files =$(".files_list >ul>li")
	var $Test_date = $(".Test_date>ul>.active")
	console.log($Test_date.text())
	for (i = 0; i < $files.length; i++) {
		$files.eq(i).click(function() {
			// console.log($(this).html())
			$.ajax({
				url: "http://127.0.0.1:8000/VQ1/download/?date="+$Test_date.text()+"&file_name="+$(this).text(),
				async: true,
				success: function(result) {
					console.log(result)
				}
			});
		})
	}
}




set_pipette_active()
Date_list()







Fixture_list(1);
Fixture_list(2);

Fixture_state(1);
Fixture_state(2);

// window.setTimeout(alert("jhdshgaj"),5000)


// var t1 = window.setInterval('Fixture_state(1)', 2000);
// var t2 = window.setInterval('Fixture_state(2)', 2000);
// window.clearInterval(t1);
