base_uri = 'http://gesagt-im-parlament.ep.io'

$.ctrl = function(key, callback, args) {
    var isCtrl = false;
    $(document).keydown(function(e) {
        if(!args) args=[]; // IE barks when args is null

        if(e.ctrlKey) isCtrl = true;
        if(e.keyCode == key.charCodeAt(0) && isCtrl) {
            callback.apply(this, args);
            return false;
        }
    }).keyup(function(e) {
        if(e.ctrlKey) isCtrl = false;
    });
};

$(document).ready(function() {
    $.ctrl('m', function() {
        $('.person img').each(function() {
            src = $(this).attr('src');
            $(this).attr('src', 'http://mustachify.me/?src=' + base_uri + src);
        });
    });
})
