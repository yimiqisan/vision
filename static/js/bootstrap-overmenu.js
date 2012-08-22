!function( $ ){
    
    "use strict"

/* OVERMENU CLASS DEFINITION */
var overmenu = '.overmenu-group'
,Overmenu = function ( el ) {
    $(el).on('mouseover', overmenu, this.overmenu)
}

Overmenu.prototype = {
    constructor: Overmenu

    , overmenu: function ( e ) {
        var $this = $(this)
        , om = $this.find('.overmenu')
        , b = -om.height()-10
        , top = $this.height()+10;
        om.css({'display':'block','top':top}).animate({'top':183}, 'fast');
    }
    , outmenu: function ( e ) {
        var $this = $(this)
        , om = $this.find('.overmenu')
        , top = $this.height()+10;
        om.animate({'top':top}, 'fast');
    }
}

/* OVERMENU PLUGIN DEFINITION */
$.fn.overmenu = function ( option ) {
    return this.each(function () {
        var $this = $(this), data = $this.data('overmenu')
        if (!data) $this.data('overmenu', (data = new Overmenu(this)))
        if (typeof option == 'string') data[option].call($this)
    })
}

$.fn.overmenu.Constructor = Overmenu

/* OVERMENU DATA-API */
    $(function () {
        $('body .overmenu-group').hover(Overmenu.prototype.overmenu, Overmenu.prototype.outmenu);
    })
}( window.jQuery );