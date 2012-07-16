//star-group

!function( $ ){
    
    "use strict"

/* STAR CLASS DEFINITION */
var star = '.star-group'
,Star = function ( el ) {
    $(el).on('click', star, this.star)
}

Star.prototype = {
    constructor: Star
    , bright: function (elem, limit) {
        elem.find('.star:lt('+limit+')').each(function(idx, el){
            $(el).removeClass('icon-star-empty').addClass('icon-star');
        })
    }
    , dark: function (elem, limit) {
        elem.find('.star:lt('+limit+')').each(function(idx, el){
            $(el).removeClass('icon-star').addClass('icon-star-empty');
        })
    }
    , set: function ( group, value ) {
        var star_value = group.next('.star-value')
        , tmp = star_value.val();
        this.dark(group, value);
        star_value.val(value);
    }
    , reset: function ( group ) {
        var value = group.next('.star-value').val();
        this.bright(group, value);
    }
    , over: function ( index, group ) {
        var i = index + 1
        , len = group.find('.star').length;
        this.dark(group, len);
        this.bright(group, i);
        return false;
    }
    , out: function ( index, group ) {
        var i = index + 1;
        this.dark(group, i);
        this.reset(group);
        return false;
    }
    , click: function ( index, group ) {
        var i = index + 1;
        this.bright(group, i);
        this.set(group, i);
        this.reset(group);
        return false;
    }
}

/* STAR PLUGIN DEFINITION */
$.fn.star = function ( option ) {
    return this.each(function (index, elem) {
        var $this = $(this), data = $this.data('star')
        if (!data) $this.data('star', (data = new Star(this)))
        if (typeof option == 'string') data[option].call($this)
    })
}

$.fn.star.Constructor = Star

/* STAR DATA-API */
    $(function () {
        $(star).each(function(){
            var $group = $(this);
            Star.prototype.reset($group);
            $group.find('.star').each(function(index, elem){
                var $this = $(this);
                $this.hover(function(){
                    Star.prototype.over(index, $group);
                },function(){
                    Star.prototype.out(index, $group);
                })
                $this.click(function(){
                    Star.prototype.click(index, $group);
                })
            })
        })
    })
}( window.jQuery );


