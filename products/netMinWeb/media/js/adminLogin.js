/**
 * doc:后台登陆界面的js
 */

(function($){
    

    var logErrorMsg = function(msg){$("#regist_win div.error_message").show().html(msg);};
    logErrorMsg.hide =function(){$("#regist_win div.error_message").hide()};
    var validateUserInfo = function(user){
        
        var exp1 = /^\w{6,18}$/;
        var exp2 = /^\w{6,16}$/;
        nb.xutils.trimObj(user);
        if(!exp1.test(user.userName)){
            logErrorMsg("用户名格式不正确，请重新填写(6-18位数字与字母)");
            return false;
        }
        if(!exp2.test(user.password)){
            logErrorMsg("密码格式不正确，请重新填写(6-16位数字与字母)");
            return false;
        }
       
        return true;
    }
	
	
	

	
	$(document).ready(function(){
		
		$("#login-form").bind("submit", function(){
			var username = $.trim($("#id_username").val());
			var password = $.trim($("#id_password").val());
			
			$("#id_username").val(username);
			$("#id_password").val(password);
			var exp = /^[0-9a-zA-Z]+(?:[\.\!\#\$\%\^\&\*\'\+\-\/\`\_\{\|\}\~]{0,1}[a-zA-Z0-9]+)*@[a-zA-Z0-9\-]+(?:[.][a-zA-Z0-9]+)*\.[0-9a-zA-Z\-]+$/;
			var p = /^\w{4,20}$/;
			if(!(exp.test(username) && p.test(password) )){
				$("#login-form div.error_message").html("请输入正确的用户名或密码...");
				return false;
			}
			
		});
		
		$("#login-form").bind("keyup", function(evt){
		    if(evt.keyCode == 13){ $(this).submit(); }
		});
		
		$("#login-form .logbutton").bind("click", function(){
		    $("#login-form").submit();
		});
		
        
        
		
	});
	
})(jQuery)
