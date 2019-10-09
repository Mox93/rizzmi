

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

function change_dtype(e, i) {
    e.form.submit();

    var id0 = "#dtype-" + i;
    var d_type = $(id0 + " option:selected").val();
    var prop = $(e.form).find(".prop");

    for (x = 0; x < prop.length; x++) {
        if (d_type+i === prop[x].id) {
            $(prop[x]).css("display", "block");
        } else {
            $(prop[x]).css("display", "none");
        };
    };
};

function duplicate_field(e, i) {
    var url = e.form.action
    $(e.form).attr("action", url + "/new");
    console.log(e.form);
    e.form.submit();
//    $(e.form).attr("action", url);
//    console.log(e.form.action);

    var id = "field-" + i
    var itm = document.getElementById(id).lastChild;
    var cln = itm.cloneNode(true);
    document.getElementById("fields").appendChild(cln);
};


/*-------------------------------------------------------*/
