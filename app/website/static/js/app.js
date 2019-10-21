

var globals = {active_field: null};

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
    globals.active_field = $(this).parents(".card")[0];
//    console.log($(globals.active_field).data("order"));

    var a = $(this).parents(".hide-choices").find('select')[0];
    $(a).css("visibility", "visible");

    var b = $(this).parents(".hide-choices").find('.driver')[0];
    var c = $(this).parents(".hide-choices").find('.driven label')[0];
    var d = $(this).parents(".hide-choices").find('.driven')[0];
    var f = $(this).parents(".left-mark")[0];
    var g = $(this).parents("form.left-mark")[0];

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

    $(f).css("border-left", "3px #3498DB solid");
    $(f).css("border-bottom", "1px solid rgba(0,0,0,.125)");
    $(g).css("border-top", "1px solid rgba(0,0,0,.125)");
});

$('.collapse').on('shown.bs.collapse', function () {
    var offset = $(globals.active_field).offset();

    if (offset.top + $("#toolbar").height() > $(window).scrollTop() + $(window).height()) {
        $("#toolbar").css("top", $(window).height() - $("#toolbar").height());
    } else if (offset.top < $("#navbar").offset().top + $("#navbar").height() + 20){
        $("#toolbar").css("top", "5rem");
    } else {
        $("#toolbar").css("top", offset.top - $(window).scrollTop());
    }

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

    $(f).css("border-left", "3px solid rgba(0,0,0,0)");
    $(f).css("border-top", "1px solid rgba(0,0,0,0)");
    $(f).css("border-bottom", "1px solid rgba(0,0,0,0)");
});

// Modal related stuff
$('#renameModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget) // Button that triggered the modal
    var name = button.data('name') // Extract info from data-* attributes
    var _id = button.data('id') // Extract info from data-* attributes
    // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
    // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
    var modal = $(this)
    modal.find('#element-name').val(name)
    modal.find('#element-id').val(_id)
});

// Also modal related stuff
$('#deleteModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget)
    var name = button.data('name')
    var _id = button.data('id')
    var modal = $(this)
    modal.find('#deleteModalLabel').text('Deleting: ' + name)
    modal.find('#del-element-id').val(_id)
});

function change_intype(e, i) {
    e.form.submit();

    var id0 = "#intype-" + i;
    var input_type = $(id0 + " option:selected").val();
    var prop = $(e.form).find(".prop");

    for (x = 0; x < prop.length; x++) {
        if (input_type+i == prop[x].id) {
            $(prop[x]).css("display", "block");
        } else {
            $(prop[x]).css("display", "none");
        };
    };
};

function duplicate_field(url) {
    //create a form
    var f = document.createElement("form");
    f.setAttribute('method', "post");
    f.setAttribute('action', url);
};

function name_submit(e) {
    if ($(e).val().trim() == "") {
        $(e).val("Untitled Form");
    };
    e.form.submit();
}

function title_submit(e) {
    if ($(e).val().trim() == "") {
    var name = $("#element-name").val()
        $(e).val(name);
    };
    e.form.submit();
}

