!function( $ ){
    
    "use strict"

/* SELECTLIST CLASS DEFINITION */
var selectlist = '.selectlist'
,Selectlist = function ( el ) {
    $(el).on('selectlist', selectlist, this.selectlist)
}

Selectlist.prototype = {
    constructor: Selectlist

    , selectlist: function ( e ) {
        var $this = $(this)
        alert('123');
    }
}

/* SELECTLIST PLUGIN DEFINITION */
$.fn.selectlist = function ( option ) {
    return this.each(function () {
        var $this = $(this), data = $this.data('selectlist')
        if (!data) $this.data('selectlist', (data = new Overmenu(this)))
        if (typeof option == 'string') data[option].call($this)
    })
}

$.fn.selectlist.Constructor = Selectlist

/* SELECTLIST DATA-API */
    $(function () {
        //$('body').on('change.selectlist.data-api', selectlist, Selectlist.prototype.selectlist)
		var args = {'kind': 'maintype'};
		$.postJSON("/a/volume/type/", "GET", args, function(response) {
			if (response.error){
				return alert(response.error);
			}
			$(response).each(function() {  
				var i = $(this)[0]
				, t = $(this)[1];
				$("#maintype").append("<option value=" + i + ">" + t + "</option>");
			});
		});

		var args = {'kind': 'property'};
		$.postJSON("/a/volume/type/", "GET", args, function(response) {
			if (response.error){
				return alert(response.error);
			}
			$(response).each(function() {
				var i = $(this)[0]
				, t = $(this)[1];
				$("#prop").append("<option value=" + i + ">" + t + "</option>");
			});
		});

		$('#maintype').change(function(){
			var maintype = $(this).val()
			, prop = $('#prop').val();
			if (maintype) {
				var args = {'kind': 'subtype', 'maintype': maintype};
				if (prop) {args['property'] = prop};
				$.postJSON("/a/volume/type/", "GET", args, function(response) {
					if (response.error){
						return alert(response.error);
					}
					$("#subtype").html("<option></option>");
					$(response).each(function() {
						var i = $(this)[0]
						, t = $(this)[1];
						$("#subtype").append("<option value=" + i + ">" + t + "</option>");
					});
				});
			}
		})
		
		$('#prop').change(function(){
			var prop = $(this).val()
			, maintype = $('#maintype').val();
			if (prop) {
				var args = {'kind': 'subtype', 'property': prop};
				if (maintype) {args['maintype'] = maintype};
				$.postJSON("/a/volume/type/", "GET", args, function(response) {
					if (response.error){
						return alert(response.error);
					}
					$("#subtype").html("<option></option>");
					$(response).each(function() {
						var i = $(this)[0]
						, t = $(this)[1];
						$("#subtype").append("<option value=" + i + ">" + t + "</option>");
					});
				});
			}
		})
    })

}( window.jQuery );

