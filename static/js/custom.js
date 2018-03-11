// Offset for Site Navigation
$('#siteNav').affix({
	offset: {
		top: 100
	}
})

$(document).ready(function(){
    $("#options1").change(function(){
    		console.log($(this).val())
              $(".content1").addClass("hidden");
        for(var i = 1; i <= $(this).val(); ++i ) {
		console.log(i)

        $("#content1-"+i).removeClass("hidden");
}
    });
});

$(document).ready(function(){
    $("#options2").change(function(){
    		console.log($(this).val())
              $(".content2").addClass("hidden");
        for(var i = 1; i <= $(this).val(); ++i ) {
		console.log(i)

        $("#content2-"+i).removeClass("hidden");
}
    });
});
