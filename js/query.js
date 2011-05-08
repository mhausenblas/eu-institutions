$(function(){	
	$("#qexec").click(function () {
		execQuery();
	});
	
});

function execQuery(){
	var qstr =  $("#qstr").val();
	
	busy();
	$.ajax({
		type: "GET",
		url: "/query/exec?",
		data: "qstr="+ encodeURIComponent(qstr),
		success: function(data){
			$("#qresult").html(data);
		},
		error:  function(msg){
			alert(msg);
		} 
	});
}

function busy(){
	$("#qresult").html("<img src='/img/busy.gif' alt='busy' />");
}