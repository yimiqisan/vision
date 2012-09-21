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
        e && e.preventDefault();
        var $that = $(this)
        , form = $that.closest('form')
        , action = form.attr('action');
        
        $that.attr('switch', 'on');
        if ($that.hasClass('preview')) {
            form.attr('target', '_blank');
            form.attr('action', action.replace(/new/, 'preview'));
        }else{
            form.removeAttr('target');
            form.attr('action', action.replace(/preview/, 'new'));
        }
        $('.help-inline, .help-block').each(function(i, e){
            var g = $(this).closest('.control-group')
            , n = g.find('label').attr('for')
            , c = g.find('[name='+n+']');
            
            alert(n);
            
            g.removeClass('error');
            if (g.hasClass('hide')) { return true; }
            if (c.attr('type') == 'checkbox'){
                var err = true;
                c.each(function(e, i){
                    if($(this).attr('checked') == 'checked'){
                        err = false;
                    }
                })
                if (err){
                    $(this).closest('.control-group').addClass('error');
                    $that.attr('switch', 'off');
                }
            }else if (!c.val()) {
                $(this).closest('.control-group').addClass('error');
                $that.attr('switch', 'off');
            }
        })
        $that.trigger('censorn');
        var swi = $that.attr('switch');
        if (swi == 'on') {form.submit();}
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