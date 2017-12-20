(function($){
    window.changeVerifyCode = function(){
        $("#verifyCodeImg").attr('src', "/getVerifyCode?stime=" + (new Date()).valueOf());
    };
    
    var COOKIE_NAME = "username";
    
	var showTip = function(){
	    var em = $("#main02 .dlRegistration input[name=email]");
	    em.val("输入您的邮箱地址");
	    em.bind("focus", function(){
	        var val = em.val();
	        if(val == "输入您的邮箱地址"){
	            em.val("");
	        }
	    });
	   em.bind("blur", function(){
            var val = em.val(); 
            if(val ==""){
                em.val("输入您的邮箱地址");
            }
        });
	};

	
	var showActiveInfo = function(){
        //if(!(active_info == 'ok' || active_info == 'fail')){return;}
        if(active_info == 'ok'){
            $("#right .login02").show();
            nb.uiTools.showEditDialogWin(null, "#active_info_ok_win", {title:"", width:580, height:200});
            
        }
        if(active_info == 'fail'){
            $("#right .login02").show();
            nb.uiTools.showEditDialogWin(null, "#active_info_fail_win", {title:"", width:580, height:200});
        }
    };
    
    var toLogin = function(){
        $.cookie(COOKIE_NAME,  $("#id_username").val(), { path: '/', expires: 10 });
    	var userInfo = {};
    	var username = $.trim($("#id_username").val());
        var password = $.trim($("#id_password").val());
        var verifyCode = $.trim($("#id_verifyCode").val());
        var p = /^\w{4,28}$/;
        if(!(p.test(password) && nb.xutils.isVaildEmail(username))){
        	$(".login02 div.error_message").html("请输入正确的用户名或密码");
            window.changeVerifyCode();
            return false;
        }
        userInfo = {username:username,password:password, verifyCode:verifyCode };
    	$.post("/accounts/login/", {userInfo: $.toJSON(userInfo)}, "json")
    	.error(function(err){ nb.AlertTip.warn("连接服务器出错！");})
        .success(function(msg){
        	if(msg == "0"){
                window.location.href = "/monitor/index/";
                return;
        	}
        	

        	$(".login02 div.error_message").html(msg);
        	window.changeVerifyCode();
        });
    };
	
	$(document).ready(function(){
		$("#right .login_button a[name=login]").bind("click", function(){
		    $("#right .login02").show();
		    window.changeVerifyCode();
		});
		window.changeVerifyCode();
		showTip();
		/**
	   $("#login-form").bind("submit", function(){
            var username = $.trim($("#id_username").val());
            var password = $.trim($("#id_password").val());
            var verifyCode = $.trim($("#id_verifyCode").val());
            $("#id_username").val(username);
            $("#id_password").val(password);
            
            var p = /^\w{4,28}$/;
            if(!(p.test(password) && nb.xutils.isVaildEmail(username))){
                $(".login02 div.error_message").html("请输入正确的用户名或密码");
                window.changeVerifyCode();
                return false;
            }
            
        });
        
     
        $("#login-form").bind("keyup", function(evt){
            if(evt.keyCode == 13){ $(this).submit(); }
        });

        $("#login-form .login_buttom").bind("click", function(){
            $("#login-form").submit();
        });
       **/
        $(".login_buttom input[name=toLogin]").bind("click", function(){
        	toLogin();
        
        });
        
        $("input[name=verifyCode]").bind("keyup", function(evt){
        	if(evt.keyCode == 13){ toLogin();}
        	
        
        });
       var em = $("#main02 .dlRegistration .error_message");
       $("#main02 .dlRegistration input[name=register]").bind("click", function(){
           var email = $.trim($("#main02 .dlRegistration input[name=email]").val());
           if(!nb.xutils.isVaildEmail(email)){
               em.html("你输入的邮件格式不对，请重新输入！");
               window.location.hash = "#registerBox";
               em.show();
               return;
           }
            em.html("");
            em.hide();
            nb.rpc.userApi.c("checkEmail", {email: email})
            .success(function(msg){
                if(!msg){
                    em.html("您注册的邮箱:"+email +"已经被注册，请从新填写新的邮箱！");
                    window.location.hash = "#registerBox";
                    em.show();
                    return;
                }
                window.location.href = "/accounts/toLoginPage/" + email;
            });
        
       });
       //使用cookie记住用户名
       if(COOKIE_NAME){
           $("#id_username").val($.cookie(COOKIE_NAME));
       }
        
       showActiveInfo();
       //showTipInLoginInput();
		
	   	
	
	});
	
})(jQuery)
