(function($){
    window.changeVerifyCode = function(){
        $("#verifyCodeImg").attr('src', "/getVerifyCode?stime=" + (new Date()).valueOf());
    };
    var logErrorMsg = function(msg){$("#regist_win div.error_message").show().html(msg);};
    logErrorMsg.hide =function(){$("#regist_win div.error_message").hide()};
    var validateUserInfo = function(user){
        
        var exp1 = /^\w{6,28}$/;
        var exp2 = /^\w{6,16}$/;
        nb.xutils.trimObj(user);
        if(!exp1.test(user.userName)){
            logErrorMsg("用户名格式不正确，请重新填写(6-28位数字、字母、下划线)");
            return false;
        }
        if(!exp2.test(user.password)){
            logErrorMsg("密码格式不正确，请重新填写(6-16位数字、字母、下划线)");
            return false;
        }
        if(user.password != user.confirmPassword){
            logErrorMsg("确认密码与原密码不一致，请重新填写");
            return false;
        }
        if(!nb.xutils.isVaildEmail(user.email)){
            logErrorMsg("邮件格式不正确，请重新填写(如:xxx@163.com)");
            return false;
        }
        if(!nb.xutils.isVaildPhone(user.contactPhone)){
            logErrorMsg("电话号码格式不正确，请重新填写(如:020-xxxxxxx, 138xxxxxxxx)");
            return false;
        }
        
        
        if(nb.xutils.isEmpty(user.companyName) || (user.companyName.length<2) ||  (user.companyName.length>20)){
            logErrorMsg("公司名称为必填项，请重新填写(2-20位字符)");
            return false;
        }
        if(!user.agreement){
            logErrorMsg("您尚未同意《网脊监控管理平台用户注册协议》");
            return false;
        }
        return true;
    }
	var regirst = function(){
	    var userInfo = {};
	   $("#regist_win .content-left input, #regist_win .content-left select").each(function(){
	       userInfo[$(this).attr("name")] = $(this).val();
	       if($(this).attr("name") == "agreement"){
	           userInfo['agreement'] = $(this).prop("checked");
	       }
	   });
	   
	   
	   if(!validateUserInfo(userInfo)) return;
	   logErrorMsg.hide();
	   $.post("/accounts/register", {userInfo: $.toJSON(userInfo)}, "json")
	   .success(function(msg){
	       if(/^(success:)(.+)/.test(msg)){
	           //alert(RegExp.$2);
	           nb.uiTools.closeEditDialogWin("#regist_win");
	           $("#regist_success_win span.reg_name").html(userInfo.userName);
	           nb.uiTools.showEditDialogWin(null, "#regist_success_win", {title:"", width:580, height:200});
	           return;
	       }
	       logErrorMsg(msg);
	       window.changeVerifyCode();
	   });
	};
	
	
	var showActiveInfo = function(){
	    //if(!(active_info == 'ok' || active_info == 'fail')){return;}
	    if(active_info == 'ok'){
    	    nb.uiTools.showEditDialogWin(null, "#active_info_ok_win", {title:"", width:580, height:200});
	    }
	    if(active_info == 'fail'){
            nb.uiTools.showEditDialogWin(null, "#active_info_fail_win", {title:"", width:580, height:200});
        }
	};
	
	$(document).ready(function(){

		$("#login-form").bind("submit", function(){
			var username = $.trim($("#id_username").val());
			var password = $.trim($("#id_password").val());
			
			$("#id_username").val(username);
			$("#id_password").val(password);
			
			var p = /^\w{4,28}$/;
			if(!(p.test(username) && p.test(password) )){
				$("#login-form div.error_message").html("请输入正确的用户名或密码");
				return false;
			}
			
		});
		
		$("#login-form").bind("keyup", function(evt){
		    if(evt.keyCode == 13){ $(this).submit(); }
		});

		$("#login-form .logbutton").bind("click", function(){
		    $("#login-form").submit();
		});
		
		
		$("#login-form .reg_btn").bind("click", function(){
		    $("input[name=agreement]").prop("checked", false);
		    window.changeVerifyCode();
            nb.uiTools.showEditDialogWin(null, "#regist_win", {title:"", width:1000, height:480});
        });
        
        $("#regist_win .content-left button:first").bind("click", function(){
            regirst();
        });
        
        $("ul.uljiexao>li:odd").addClass("item_odd");
        
        
        showActiveInfo();
        
        //setInterval(function(){window.changeVerifyCode()}, 1000*60*1);
		
	});
	
})(jQuery)
