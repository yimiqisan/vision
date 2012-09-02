(function($){
    $.fn.hoverDelay = function(options){
        var defaults = {
            hoverDuring: 200,
            outDuring: 200,
            hoverEvent: function(){
                $.noop();
            },
            outEvent: function(){
                $.noop();
            }
        };
        var sets = $.extend(defaults,options || {});
        return $(this).each(function(){
            var that = this;
            var hoverTimer, outTimer;
            $(this).hover(
                function(){
                    clearTimeout(outTimer);
                    hoverTimer = setTimeout(function(){sets.hoverEvent.apply(that)}, sets.hoverDuring);
                },
                function(){
                    clearTimeout(hoverTimer);
                    outTimer = setTimeout(function(){sets.outEvent.apply(that)}, sets.outDuring);
                }
            );
        });
    }
})(jQuery);
