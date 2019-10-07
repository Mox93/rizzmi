// these will always run
$(function() {
    $("#element-name").change(function() {
        $("#name-field").submit();
    });
    $("#element-title").change(function() {
        $("#title-field").submit();
    });
    $("#element-des").change(function() {
        $("#title-field").submit();
    });
});

// the current open accordion will not be able to close itself
$('[data-toggle="collapse"]').on('click',function(e){
    if ( $(this).parents('.accordion').find('.collapse.show') ){
        var idx = $(this).index('[data-toggle="collapse"]');
        if (idx == $('.collapse.show').index('.collapse')) {
            e.stopPropagation();
        }
    }
});

// actions for when the collapse is shown
$('.collapse').on('show.bs.collapse', function () {
    var a = $(this).parents(".hide-choices").find('select')[0];
    $(a).css("visibility", "visible");

    var b = $(this).parents(".hide-choices").find('.driver')[0];
    var c = $(this).parents(".hide-choices").find('.driven label')[0];
    var d = $(this).parents(".hide-choices").find('.driven')[0];
    var f = $(this).parents(".left-mark")[0];

    $(b).hover( function() {
        $(c).css("visibility", "visible");
    }, function(){
        $(c).css("visibility", "hidden");
    });

    $(d).hover( function() {
        $(c).css("cursor", "pointer");
        $(c).css("visibility", "visible");
    }, function(){
        $(c).css('cursor', 'default');
        $(c).css("visibility", "hidden");
    });

    $(f).css("border-left", "3px #3498DB solid")
});

// actions for when the collapse is hidden
$('.collapse').on('hide.bs.collapse', function () {
    var a = $(this).parents(".hide-choices").find('select')[0];
    $(a).css("visibility", "hidden");

    var b = $(this).parents(".hide-choices").find('.driver')[0];
    var c = $(this).parents(".hide-choices").find('.driven label')[0];
    var d = $(this).parents(".hide-choices").find('.driven')[0];
    var f = $(this).parents(".left-mark")[0];

    $(b).hover( function() {
        $(c).css("visibility", "hidden");
    }, function(){
        $(c).css("visibility", "hidden");
    });

    $(d).hover( function() {
        $(c).css("visibility", "hidden");
    }, function(){
        $(c).css("visibility", "hidden");
    });

    $(f).css("border-left", "3px solid rgba(0,0,0,0)")
});

