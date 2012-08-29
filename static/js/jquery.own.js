jQuery.postJSON = function(url, type, args, callback) {
    $.ajax({url: url, data: $.param(args), dataType: "text", type: type, async: false,
            success: function(response) {
        if (callback) callback(eval("(" + response + ")"));
    }, error: function(response) {
        console.log("ERROR:", response)
    }});
};

jQuery.fn.formToDict = function() {
    var fields = this.serializeArray();
    var json = {}
    for (var i = 0; i < fields.length; i++) {
        json[fields[i].name] = fields[i].value;
    }
    if (json.next) delete json.next;
    return json;
};

jQuery.fn.disable = function() {
    this.enable(false);
    return this;
};

jQuery.fn.enable = function(opt_enable) {
    if (arguments.length && !opt_enable) {
        this.attr("disabled", "disabled");
    } else {
        this.removeAttr("disabled");
    }
    return this;
};

function delItem(e) {
    var mid = $(e).attr('id').replace('d-', 'm-');
    var $p = $("#"+mid);
    var args = {'id': mid.replace('m-', '')};
    $.ajax({
        url: "/a/reply/remove/", 
        type: "POST", 
        dataType: "text",
        data: $.param(args), 
        beforeSend: function() {
            $p.css("color", "#D6EED8");
        },
        success: function() {
            $p.slideUp(300, function() {$p.remove();})
        }
    });
};

function delconfirm(e) {
    if (!confirm(" 确定删除?")) return false;
};

function backconfirm(e) {
    if (!confirm(" 确定返回?")) return false;
};

var Reply = {
    toggle: function(e) {
        mid = $(e).attr('id').replace('r-', 'm-');
        var isHas = $('#'+mid).hasClass('disp-re');
        if (isHas) {
            $('#'+mid+' .wb_rep_list').toggle();
        }else{
            Reply.list(mid);
            $('#'+mid).addClass('disp-re');
        }
    },
    
    list: function(id) {
        var args = {'id': id.replace("m-","")};
        $.postJSON("/a/reply/", "GET", args, function(response) {
            if (response.error){
                return alert(response.error);
            }
            var $cur = $('#'+id+' .content');
            $cur.find(".wb_rep_list").remove();
            $cur.append('<div class="wb_rep_list"><div class="input clearfix"><form action="/a/reply" method="post" class="replyform"><input name="content" class="reply-content" style="width:85%;margin:0 0 3px 0; padding：4px 4px 0 4px; border: 1px solid rgb(198, 198, 198); font-size: 12px; font-family: Tahoma, 宋体; word-wrap: break-word; line-height: 18px; outline-style: none; outline-width: initial; outline-color: initial; overflow-x: hidden; overflow-y: hidden; height: 22px;"><input class="btn pull-right" type="submit" value="回复"></form><div class="action clearfix"></div></div></div>');
            $cur.find(".wb_rep_list").append("<div class='bottom'><a style='margin-top:10px;display:block;text-align:center;' onclick=Reply.extend('"+id+"');return false;>下拉</a><input type='hidden' value='0'></div>");
            var e = $("#"+id+" .wb_rep_list .bottom");
            $(e).find('a').text('').addClass('loading');
            htmls = response.htmls;
            for (var i=0; i<htmls.length; i++) {
                $(htmls[i]).insertBefore(e);
            }
            if (htmls.length < 10){
                $(e).find('a').text('没有更多的了').removeClass('loading');
                $(e).find('input').val(-1);
            }else{
                $(e).find('a').text('下拉').removeClass('loading');
                $(e).find('input').val(response.cursor);
            }
            Reply.submit(id);
        });
    },
    
    extend: function(id) {
        var e = $(".wb_rep_list .bottom");
        if ($(e).find('input').val()=='-1'){$(e).find('a').text('没有更多的了');return false;}
        var args = {'id': id.replace("m-",""), 'cursor': $(e).find('input').val()};
        $(e).find('a').text('').addClass('loading');
        $.postJSON("/a/reply/", "GET", args, function(response) {
            if (response.error){
                return alert(response.error);
            }
            htmls = response.htmls;
            for (var i=0; i<htmls.length; i++) {
                $(htmls[i]).insertBefore(e);
            }
            if (htmls.length < 10){
                $(e).find('a').text('没有更多的了').removeClass('loading');
                $(e).find('input').val(-1);
            }else{
                if (response.cursor==-1){
                    $(e).find('a').text('没有更多的了').removeClass('loading');
                }else{
                    $(e).find('a').text('下拉').removeClass('loading');
                }
                $(e).find('input').val(response.cursor);
            }
        });
    },
    
    submit: function(id){
/*        if (!$.cookie("uid")) {
            $('#login').modal();
            return false;
        }
*/        var e = $('#'+id+' .replyform');
        e.live("submit", function() {
            Reply.insert(e, id.replace('m-', ''));
            return false;
        });
        e.live("keypress", function() {
            if (e.keyCode == 13) {
                Reply.insert(e, id.replace('m-', ''));
                return false;
            }
        });
        $('#'+id+' .reply-content').select();
    },
    
    insert: function(form, id) {
        if ($('#m-'+id+' .reply-content').val() == ""){return false;}
        var message = form.formToDict();
        message["to"] = id
        var disabled = form.find("input[type=submit]");
        disabled.disable();
        $.postJSON("/a/reply/new", "POST", message, function(response) {
            if (response.error){
                disabled.enable();
                return alert(response.error);
            }
            var existing = $("#r-" + response.id);
            if (existing.length > 0) return;
            var node = $(response.html);
            node.hide();
            $(node).insertAfter($("#m-"+id+" .wb_rep_list .input"));
            node.slideDown();
            form.find(".reply-content").val("").select();
            disabled.enable();
        });
    },
    
    reply: function(e) {
        var mid = 'm-'+$(e).attr('to');
        var nick = $(e).attr('nick');
        $('#'+mid+' .reply-content').val('@'+nick+' ');
    }
}
