var c2d2_data = [];
var c2d2_header = [];

$(function(){
	initDisplay();
	
	$("#keyword").keyup(function () {
		var searchterm = $("#keyword").val();
		
		if(searchterm.length > 2) {
			$(".scell").each(function() {
				$(this).hide();
			});
			$(".scell:contains('" + searchterm.toLowerCase() + "')").show();
		}
		else {
			$(".scell").each(function() {
				$(this).show();
			});
		}
	 });
	
	$("#reset").click(function () {
		$("#keyword").val("");
		$(".scell").each(function() {
			$(this).show();
		});
	 });
	
	$(".scell").live("click", function () {
		var index = $(this).attr("resource");
		render(index);
	});
});

function initDisplay(){
	var b = "<div id='dir'>";
	var metainfo = "";
	
	for (i in c2d2_data) {
		metainfo = valueFor(i, 'Category') + " " + valueFor(i, 'Type') + " " + valueFor(i, 'Programming Languages') + " " + valueFor(i, 'Comments');
		metainfo = metainfo.toLowerCase();
		b += "<div class='scell' resource='" + i + "'>" + valueFor(i, 'Name') + "<div class='metainfo'>" + metainfo + "</div></div>";
	} 
	b += "</div>";
	b += "<div id='details'><div style='color: #d0d0d0; text-align: center; padding: 2em; font-size: 26pt'>Select a tool or service from the list on the left or filter by keyword (e.g. 'Ruby' or 'git') to shorten the list.</div></div>";
	
	
	$("#out").html(b);
	$("#out").slideDown('slow');
}

function prepC2D2List(data){
	c2d2_data = [];
	c2d2_header = [];
	var r = 0;

	for (var i=0; i < data.feed.entry.length; i++) {
		var entry = data.feed.entry[i];
		if (entry.gs$cell.row == '1') {
			c2d2_header.push(entry.content.$t);
		}
		else {
			r = parseInt(entry.gs$cell.row) - 2;
			c = parseInt(entry.gs$cell.col) - 1;
			if(!c2d2_data[r]) c2d2_data[r] = [];
			c2d2_data[r][headerFor(c)] = entry.content.$t;
		}
	}
}

function headerFor(index){
	return c2d2_header[index];
}

function valueFor(index, header) {
	return c2d2_data[index][header];
}

function render(index){
	var b = "";

	$("#details").hide('fast');

	b += "<div class='category'>"+ valueFor(index, 'Category') + "</div>";
	b += "<h2>" + valueFor(index, 'Name') + "</h2>";
	b += "<div class='URI'><a href='" + valueFor(index, 'URI') + "' target='_new'>"+ valueFor(index, 'URI') + "</a></div>";
	if(valueFor(index, 'Image')) b += "<div><img src='" + valueFor(index, 'Image') + "' class='ssimage' width='500px' alt='screen-shot' />";
	else b += "<div><img src='https://docs.google.com/uc?id=0B1wfpys1YRkcMTEzODZkNmYtZmE2MS00ODI5LWEwMDktYTZiYmFlMzQxMzVh&export=download&hl=en' class='ssimage' alt='no screen-shot available' />";
	b += "<div class='comment'>Type: "+ valueFor(index, 'Type') + "</div>";
	b += "<div class='comment'>Programming Languages: "+ valueFor(index, 'Programming Languages') + "</div>";
	if(valueFor(index, 'Pricing')) b += "<div class='comment'>Pricing and Quota: <a href='"+ valueFor(index, 'Pricing') + "' target='_new'>details ...</a></div>";
	else b += "<div class='comment'>Pricing and Quota: unknown</div>"; 
	b += "<div class='comment'>Other comments: "+ valueFor(index, 'Comments') + "</div></div>";
	b += "<div class='ep'>"+ valueFor(index, 'Elevator Pitch') + "</div>";
	
	$("#details").html(b);
	$("#details").show('slow');
	
}