$(function(){
	$("#show-eui-schema-details").click(function () {
		$('#eui-schema-details').toggle('slow', function() {
			if ($("#show-eui-schema-details").text() == "Show details ...")
				$("#show-eui-schema-details").text("Hide details ...");
			else
				$("#show-eui-schema-details").text("Show details ...");	
		});
	});
});
