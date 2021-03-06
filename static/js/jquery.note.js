(function(b) {
    var a = window.yhui || {};
    a.log = function(c) {
        if (typeof(console) != "undefined" && typeof(console.log) == "function") {
            console.log(c)
        }
    };
    a.iNote = (function() {
        var c = {
            id: 'note',
            eclass: 'span3',
            placeholderText: '输入后按 < Enter > 键',
            removeConfirmation: true,
            tagSource:function() {},
            onTagRemoved: function(evt, tag) {},
            onTagClicked: function(evt, tag) {},
            onTagAdded: function(evt, tag) {},
        },
        d = {
            panelControl: false,
        },
        g = b.extend(c, d);
        function h() {
            if (!b("#note_title").val()) {
                alert('请您填写题目');
                b("#note_title").select();
                return false;
            }
            if (!b("#note_text").val()) {
                alert('请在正文中说点什么吧');
                b("#note_text").select();
                return false;
            }
            return true
        };
        function i(u) {
            if (u) {
                $.postJSON("/a/item/"+u+"/?r="+Math.random(), 'GET', {}, function(response) {
                    if (response.error){
                        alert(response.error);
                        return ;
                    }
                    var j = 1;
                    for (w in response.works) {
                        if (response.works[w][0] == response.logo) {j=parseInt(w)+1}
                        n('PIC', response.works[w][0], response.works[w][1]);
                    }
                    $('input[name="cover"]').eq(j-1).attr('checked', 'checked');
                    dragsort.makeListSortable(document.getElementById("thumbnails"), setHandle);
                });
                KindEditor.create('.inplace', {
					resizeType : 0,
					allowPreviewEmoticons : false,
					allowImageUpload : false,
					items : [
						'fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', 'bold', 'italic', 'underline',
						'removeformat', '|', 'justifyleft', 'justifycenter', 'justifyright', 'insertorderedlist',
						'insertunorderedlist']//, '|', 'emoticons', 'image', 'link']
				});
            }
        };
        function j(x, z) {
            var u = b('#note_title').val(),
            v = k(),
            w = b('input[name=noteTags]').val();
            var message = {'note_title': u, 'note_text': v, 'note_tag': w};
            if (x) {
                if (z == 'append') {
                    message.pid = x;
                } else {
                    message.nid = x;
                }
            }
            $.postJSON("/a/note/?r="+Math.random(), 'POST', message, function(response) {
                if (response.error){
                    alert(response.error);
                    return ;
                }
            });
        };
        function k() {
            var u = b('#note_text').val();
            var tlength = b("#thumbnails li").length;
            b("#thumbnails li").each(function(index, object){
                var i = tlength - index;
                var pic = "图:"+i,
                reg = new RegExp(pic,"g"),
                pid = "pic"+i,
                pos = "pos"+i,
                dtl = b('#'+pid).find('textarea').val() || pic;
                var src = b("#"+pid+" img").attr('src');
                var img = '<img src='+src+' alt='+dtl+' title='+dtl+'>';
                img=img+'<div>'+dtl+'</div>';
                u = u.replace(reg, img);
            });
            return u;
        };
        function l(u) {
            var v = b(u).attr("rel");
            var li = b('#pic'+v);
            reg = "\/image\/attach\/(.*)";
            var args = {};
            args.pid = li.find('img').attr('src').match(reg)[1];
            $.postJSON("/a/image/delete/?r="+Math.random(), 'POST', args, function(response) {
                if (response.error){
                    alert(response.error);
                }
                var w = b('#note_text')
                b('#pic'+v).fadeOut().remove();
                b('#'+v+'Edit').remove();
                return false;
            });
            return false;
        };
        function m(u, z) {
            if (z == 'append') { return false; }
            args = {'nid': u}
            $.postJSON("/a/note/?r="+Math.random(), 'GET', args, function(response) {
                if (response.error){
                    alert(response.error);
                    return ;
                }
                b('#note_title').val(response.info.title);
                var reg = new RegExp('<div class="([A-Z]{3,4})"><img src=/image/attach/(.{32}) alt=.*? title=.*?><div>(.*?)</div></div>',"g");
                var vc = response.info.content;
                for (var i=0; i<response.info.tags.length; i++) {
                    $("#noteTags").tagit('createTag', response.info.tags[i][1], '', response.info.tags[i][0]);
                }
                do {
                    var result = reg.exec(response.info.content);
                    if (!result) {break;}
                    r = n(result[1], result[2], result[3]);
                    var regc = new RegExp(result[0],"g");
                    vc = vc.replace(regc, r)
                } while (result)
                
                b('#note_text').val(vc);
                return false;
            });
        };
        function n(u, v, w) {
            var pic_num = $("#thumbnails li").length+1;
            var pic_name = "图:"+pic_num;
            z = b('<li id="pic'+pic_num+'" itemid="pic'+pic_num+'" class="span8 box" style="cursor:move;width:720px;padding:5px;"><div class="thumbnail" style="min-height:200px;"><div style="float:left;width:30px;"><input type="radio" name="cover" value="'+pic_num+'" onclick="yhui.iNote.cover(this);" style="float:left;margin:5px;"><p class="pname">'+pic_name+'</p></div><div style="float:left; clear:right;margin-right:10px;width:200px;height:200px;position:relative;overflow:hidden;display:block;"><img src="/image/attach/'+v+'_crop" onload="yhui.iNote.imgload(this);" alt="" title="" style="display:block;width:200px;margin:0 auto;margin-bottom:5px;"><input name="'+pic_num+'PIC" class="pic" type="hidden" value="'+v+'" /></div><div id="'+pic_num+'View" class="view" style="display:none;"></div><textarea id="'+pic_num+'Edit" name="'+pic_num+'Edit" class="inplace" style="width:454px;height:90px;">'+w+'</textarea><a class="close" rel="'+pic_num+'" href="#" onclick="yhui.iNote.delPic(this);return false;">×</a></div></li>');
            b('#thumbnails').append(z);
            drag_join(pic_num);
            return pic_name;
        };
        function o(u) {
            $("#thumbnails input[type=radio]").removeAttr("checked");
            $(u).attr("checked", true);
            return false;
        };
        function p(e){
            if ((parseFloat($(e).width())/$(e).height()) > 1.0){
                $(e).css("height", "200").css("width", "auto")
            };
        };
        function q(){
            var tlength = $("#thumbnails li").length;
            $("#thumbnails li").each(function(index, object){
                var i = tlength - index;
                pid = "pic"+i,
                pname = "图"+i,
                pic = i+"PIC",
                view = i+"View",
                edit = i+"Edit";
                $(this).attr('id', pid);
                $(this).attr('itemid', pid);
                $(this).find('[name=cover]', i);
                $(this).find('.pname').text(pname);
                $(this).find('.pic').attr('name', pic);
                $(this).find('.view').attr('id', view);
                $(this).find('.inplace').attr('id', edit);
                $(this).find('.inplace').attr('name', edit);
                $(this).find('.close').attr('rel', i);
            });
        }

        return {
            check: function() {
                return h();
            },
            init:function(u) {
                return i(u);
            },
            insertPic: function(u, v, w) {
                return n(u, v, w);
            },
            delPic: function(u) {
                return l(u);
            },
            cover:function(u) {
                return o(u);
            },
            imgload:function(u) {
                return p(u);
            },
            alignment:function() {
                return q();
            }
        }
    })();
    window.yhui = a
})(jQuery);
