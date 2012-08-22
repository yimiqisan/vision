!function( $ ){
    
    "use strict"

/* LOGIN CLASS DEFINITION */
var login = '.login'
,Login = function ( el ) {
    $(el).on('click', login, this.login)
}

Login.prototype = {
    constructor: Login

    , login: function ( e ) {
        var $this = $(this)
        , form = $this.closest('form')
        , email = form.find('[name=email]')
        , reg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/
        , password = form.find('[name=password]')
        , be = true
        , email_str = email.val();
        
        if (!email_str) {
            alert('请填写邮箱');
            email.select();
            be = false;
            return false;
        }
        
        if (email_str!='admin' && !reg.test(email_str)) {
            alert('邮箱格式不正确');
            email.select();
            be = false;
            return false;
        }        
        
        if (!password.val()) {
            alert('请填写密码');
            password.select();
            be = false;
            return false;
        }
        
        if (be) {
            $this.trigger('loginn');
        }
        return false;
    }
    
    , cemail: function ( e ) {
        var $this = $(this),
        email_str = $this.val(),
        reg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/;
        if (!reg.test(email_str)) {
            alert('邮箱格式不正确');
        }        
    }
    
    , cpassword: function ( e ) {
        //alert(e);
    }
    
}

/* CHECK PLUGIN DEFINITION */
$.fn.login = function ( option ) {
    return this.each(function () {
        var $this = $(this), data = $this.data('login')
        if (!data) $this.data('login', (data = new Login(this)))
        if (typeof option == 'string') data[option].call($this)
    })
}

$.fn.login.Constructor = Login

/* CHECK DATA-API */
    $(function () {
        $('body').on('click.login.data-api', '.login [type=submit]', Login.prototype.login)
        //$('body').on('blur.login.data-api', '.login [name=email]', Login.prototype.cemail)
        //$('body').on('blur.login.data-api', '.login [name=password]', Login.prototype.cpassword)
    })

}( window.jQuery );


