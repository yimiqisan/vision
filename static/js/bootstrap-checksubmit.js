!function( $ ){
    
    "use strict"

/* CHECK CLASS DEFINITION */
var censor = '.censor, .preview'
,Check = function ( el ) {
    $(el).on('click', censor, this.censor)
}

Check.prototype = {
    constructor: Check

    , censor: function ( e ) {
        var $this = $(this)
        , form = $this.closest('form')
        , be = true;
        
        if ($this.hasClass('preview')) {
            form.attr('target', '_blank');
            var action = form.attr('action');
            form.attr('action', action.replace(/new/, 'preview'));
        }else{
            form.removeAttr('target');
            var action = form.attr('action');
            form.attr('action', action.replace(/preview/, 'new'));
        }
        $('.help-inline, .help-block').each(function(i, e){
            var c = $(this).prev()
            , g = $(this).closest('.control-group');
            g.removeClass('error');
            if (g.hasClass('hide')) { return true; }
            if (typeof c.attr('name') === 'undefined'){
                c = c.find('input');
            }
            if (c.attr('type') == 'checkbox'){
                be = false;
                c.each(function(e, i){
                    if($(this).attr('checked') == 'checked'){be = true;}
                })
                if (!be){$(this).closest('.control-group').addClass('error');}
            }else if (c.val() === '') {
                $(this).closest('.control-group').addClass('error');
                be = false;
            }
            return true;
        })
        $this.trigger('censorn');
        if (be) {form.submit();}
        return false;
    }
}

/* CHECK PLUGIN DEFINITION */
$.fn.check = function ( option ) {
    return this.each(function () {
        var $this = $(this), data = $this.data('check')
        if (!data) $this.data('check', (data = new Check(this)))
        if (typeof option == 'string') data[option].call($this)
    })
}

$.fn.check.Constructor = Check

/* CHECK DATA-API */
    $(function () {
        $('body').on('click.check.data-api', censor, Check.prototype.censor)
    })

}( window.jQuery );