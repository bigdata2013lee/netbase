(function($){
	//运维商用户中心的工程师管理界面的主JS【2014.12.18  jenny】
    var m = new nb.xutils.Observer();
    
    /**
	 * 验证修改工程师密码的数据，
	 * @method _validatePassword
	 * @param {string} password 工程师账号的密码
	 * @param {string} confirmPassword 工程师账号的确认密码
	 * @return {bool} 判断密码是否符合规范，两次输入是否一致
	 */
    var _validatePassword=function(params){
        var em = $("#modifyPwdWin div.validateErrorMsg");
        var rules = {
            password: {method: "regex", exp: /^\w{6,16}$/},
            confirmPassword:{method:"confirmPassword", eqto: "password"} 
        };
        var messages = {password:"请输入6~16位的新密码,只能包涵数字、字母、下划线，并区分大小写"};
        var validator = new nb.xutils.Validator(em, rules, messages);
        
        return validator.validate(params);            
    };
    
    /**
	 * 验证创建工程师提交的数据
	 * @method _validateEngineerParams
	 * @param {string} originalName 工程师姓名
	 * @param {string} username 工程师账号
	 * @param {string} password 工程师账号的密码
	 * @param {string} confirmPassword 工程师账号的确认密码
	 * @param {string} email 工程师的联系邮箱
	 * @return {bool} 判断所输入的值是否符合规范，以及不为空
	 */
    var _validateEngineerParams=function(params){
        var em = $("#creatEngineerWin div.validateErrorMsg");
        var rules = {
            originalName:"required",
            username:"email",
            password: {method: "regex", exp: /^\w{6,16}$/},
            confirmPassword:{method:"confirmPassword", eqto: "password"},
            email:"email"
        };
        var messages = {
            originalName:"姓名是必填项，请输入",
            username:"用户名请使用正确的邮箱格式",
            password:"请输入6~16位的新密码,只能包涵数字、字母、下划线，并区分大小写",
            email:"请填写有效联系邮箱！"
        };
        var validator = new nb.xutils.Validator(em, rules, messages);
        
        return validator.validate(params);            
    };
    
    /**
	 * 提交修改工程师密码的数据，
	 * @method modifyPwd
	 * @return {string} 返回数据提交成功与否的字符串
	 */
    var modifyPwd = function(){
        var params=nb.uiTools.mapFields("#modifyPwdWin");
        if(!_validatePassword(params)){return;}
        delete params.confirmPassword;
        nb.rpc.operationView.c("modifyEngineerPWD", params)
        .success(function(msg){
            nb.AlertTip.auto(msg);
            nb.uiTools.closeEditDialogWin("#modifyPwdWin");
        });
    }

    /**
	 * 提交创建工程师账号的数据，
	 * @method creatEngineer
	 * @return {string} 返回数据提交成功与否的字符串
	 */
    var creatEngineer = function(){
        var params=nb.uiTools.mapFields("#creatEngineerWin");
        if(!_validateEngineerParams(params)){return;}
        delete params.confirmPassword;
        nb.rpc.operationView.c("addEngineer", params)
        .success(function(msg){
            nb.AlertTip.storeCookie(msg);
            nb.uiTools.closeEditDialogWin("#creatEngineerWin");
            location.reload();
        });
    }
    
	//定义一个显示服务客户功能的组件  
	//通过Ajax的方式，传一个工程师ID【engineerId】到后台，返回一个服务客户资料的HTML
	//把HTML加载到显示服务客户的窗体中
    var showServiceCustomerWidget={      
        showServiceCustomer:function(engineerId){
            var self = this;
            $.post("/operation/showServiceCustomers/" + engineerId + "/",{}, function(html){
                $("#listEngServiceCustomers div.box").html(html);
            });
        },      
        __init__:function(){
            var self = this;
            $(".data_table tbody a[action=viewServiceCustomers]").bind("click",function(){
                var engineerId = $(this).parent().attr("engineer_id");
                self.showServiceCustomer(engineerId);
                nb.uiTools.showEditDialogWin(null, "#listEngServiceCustomers", {width:500, height:200});    
            })            
        }
    };
    
    
    $(document).ready(function(){
        
        //触发修改工程师账号密码的事件并显示编辑窗体
        $(".data_table tbody a[action=modifyEngineerPWD]").bind("click",function(){
            var engineerId = $(this).parent().attr("engineer_id");
            $("#modifyPwdWin input[name=engineerId]").val(engineerId);
            nb.uiTools.showEditDialogWin(null, "#modifyPwdWin", {width:500, height:200});        
        })
        
        //触发提交修改工程师密码的事件
        $("#modifyPwdWin .win_opbar button.ok").bind("click",function(){
			modifyPwd();
        });
        
        //触发删除工程师的事件并提交被删除的工程师的ID
        $(".data_table tbody a[action=remove]").bind("click",function(){
            var engineerId = $(this).parent().attr("engineer_id");
			nb.uiTools.confirm("您确定要删除此工程师吗？",function(){
				var params = {}
				params.engineerId = engineerId;
				nb.rpc.operationView.c("deleteEngineer", params)
				.success(function(msg){
					nb.AlertTip.storeCookie(msg);
				    window.location.reload();
				})           
			})
        })
        
        //触发显示创建工程师的窗口的事件
        $(".query_tool_bar li  a[action=creatEngineer]").bind("click",function(){
            nb.uiTools.showEditDialogWin(null, "#creatEngineerWin", {width:600, height:280});               
        })
        
        //触发提交创建工程师的数据的事件
        $("#creatEngineerWin .win_opbar button.ok").bind("click",function(){
                creatEngineer();
        });

		//初始化一个显示服务客户功能的组件  
    	showServiceCustomerWidget.__init__();
        
    });
    
})(jQuery);
