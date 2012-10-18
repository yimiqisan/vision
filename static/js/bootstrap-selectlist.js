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
			var default_value = $('#maintype option:first').val();
			$(response).each(function() {  
				var i = $(this)[0]
				, t = $(this)[1];
				if (i != default_value) {
				    $("#maintype").append("<option value=" + i + ">" + t + "</option>");
				}
			});
		});
        
		var args = {'kind': 'property'};
		$.postJSON("/a/volume/type/", "GET", args, function(response) {
			if (response.error){
				return alert(response.error);
			}
			var default_value = $('#prop option:first').val();
			$(response).each(function() {
				var i = $(this)[0]
				, t = $(this)[1];
				if (i != default_value) {
				    $("#prop").append("<option value=" + i + ">" + t + "</option>");
				}
			});
		});
		
		
		var maintype = $('#maintype').val()
		, prop = $('#prop').val()
		, stype = $('#subtype option');
        var args = {'kind': 'subtype'};
		if (maintype) {args['maintype'] = maintype};
		if (prop) {args['property'] = prop};
		$.postJSON("/a/volume/type/", "GET", args, function(response) {
			if (response.error){
				return alert(response.error);
			}
			$("#subtype").html("<option></option>");
			var default_value = stype.val();
			$(response).each(function() {
				var i = $(this)[0]
				, t = $(this)[1];
				if (i != default_value) {
				    $("#subtype").append("<option value=" + i + ">" + t + "</option>");
				}
			});
			$("#subtype").append(stype);
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
			    if (prop == 'PERSONAL') {
			        $("[for='name']").text('姓名');
			        $("[for='engname']").text('英文姓名');
			        $("[for='builder']").parent().addClass('hide');
			        $("input[name=builder]").val('');
                    $("[for='post']").parent().addClass('hide');
			        $("input[name=post]").val('');
			        $("[for='male']").parent().removeClass('hide');
			        $("[for='born']").text('出生日期');
			        $("textarea[name=about]").val('');
			        $("[for='market']").parent().addClass('hide');
			    }else if (prop == 'ORGANIZATION') {
			        $("[for='name']").text('名称');
			        $("[for='engname']").text('英文名称');
			        $("[for='male']").parent().addClass('hide');
			        $("[for='builder']").parent().removeClass('hide');
			        $("input[name=builder]").val('');
			        $("[for='post']").parent().removeClass('hide');
			        $("input[name=post]").val('');
			        $("[for='born']").text('创建时间');
			        $("textarea[name=about]").val('');
			        $("[for='market']").parent().removeClass('hide');
			    }else if (prop == 'SHOW') {
			        $("[for='name']").text('名称');
			        $("[for='engname']").text('英文名称');
			        $("[for='male']").parent().addClass('hide');
			        $("[for='builder']").parent().removeClass('hide');
			        $("input[name=builder]").val('');
			        $("[for='post']").parent().removeClass('hide');
			        $("input[name=post]").val('');
			        $("[for='born']").text('创建时间');
			        $("textarea[name=about]").val('');
			        $("[for='market']").parent().removeClass('hide');
			    }
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

