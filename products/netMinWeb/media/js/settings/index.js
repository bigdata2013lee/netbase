(function($){
    
    var m = window.settingsIndex = new nb.xutils.Observer();
    

    
    m.on("afterViewInfoWidgetReload", function(){
        var email = m.viewInfoWidget._data.email;
        var contactPhone = m.viewInfoWidget._data.contactPhone;
        
        m.changeEmailAandPhoneWidget.viewModel.set("email",email);
        m.changeEmailAandPhoneWidget.viewModel.set("contactPhone",contactPhone);
    });
    
    m.on("afterChangeEmailAandPhoneWidgetSave", function(){
        m.viewInfoWidget.reload();
    });
    
    m.viewInfoWidget = {
        
        _panel_id: "#panel_0001",
        _data:null,
        _render: function(){
            var self = this;
            var template = self.getTemplate();
            $(self._panel_id + " .box:first").html(template(self._data));            
        },
        getTemplate: function(){
            var template = kendo.template($(this._panel_id + " ul[name=template]").html());
            return template;
        },
        reload:function(){
            var self = this; 
            nb.rpc.userApi.c("getUserInfo", {uid:userId}).success(function(user){
                self._data = user;
                self._render();
                m.fireEvent("afterViewInfoWidgetReload");
            });
        }
        
        
    };
    
    
    
    m.changePasswordWidget = {
        _panel_id: "#panel_0002",
        viewModel: kendo.observable({ oldPassword:"", newPassword:"", confirmPassword:"" }),
        _render: function(){
            var self = this;
            kendo.bind($(self._panel_id + " .box:first"), self.viewModel);
        },
        
        _validatePassword: function(passwords){
            var self = this;
            var em = $(self._panel_id + " div.validateErrorMsg");
            var rules = {
                oldPassword: {method: "regex", exp: /^\w{4,16}$/}, 
                newPassword: {method: "regex", exp: /^\w{4,16}$/},
                confirmPassword:{method:"confirmPassword", eqto: "newPassword"} 
            };
            var messages = {oldPassword:"请输入4~16位的旧密码", newPassword:"请输入4~16位的新密码,只能包涵数字、字母、下划线，并区分大小写"};
            var validator = new nb.xutils.Validator(em, rules, messages);
            var params = {oldPassword: passwords.oldPassword, newPassword: passwords.newPassword, 
               confirmPassword: passwords.confirmPassword
            }
            return validator.validate(params);
            
        },
        
        save: function(){
            var self = this;
            var params = {uid:userId};
            $.extend(params, self.viewModel.toJSON());
            nb.xutils.trimObj(params);
            var fg = self._validatePassword(params);
            if(! fg ) return;
           
           params.oldPassword = $.md5(params.oldPassword);
           params.newPassword = $.md5(params.newPassword);
           params.confirmPassword = $.md5(params.confirmPassword);
           
            nb.rpc.userApi.c("changePassword",params).success(function(msg){
                nb.AlertTip.auto(msg);
            });
            
        },
        __init__:function(){
            var self = this;
            $(self._panel_id + " .op_bar a[name=save]").bind("click", function(){
                self.save();
            });
            
            self._render();
        }
    };
    
    m.changeEmailAandPhoneWidget = {
        _panel_id: "#panel_0003",
        viewModel: kendo.observable({ contactPhone:"", email:""}),
        _render: function(){
            var self = this;
            kendo.bind($(self._panel_id + " .box:first"), self.viewModel);
        },
        _validate: function(email, contactPhone){
            var self = this;
            var em = $(self._panel_id + " div.validateErrorMsg");
            var rules = { email: "email", contactPhone: "phone"};
            var validator = new nb.xutils.Validator(em, rules);
            var params = {email:email, contactPhone:contactPhone}
            return validator.validate(params);
            
        },
        save: function(){
            var self = this;
            var params = {uid:userId};
            $.extend(params, self.viewModel.toJSON());
            nb.xutils.trimObj(params);
            var fg = self._validate(params.email, params.contactPhone);
            if(! fg ) return;
           
             var _remote = function(){
                nb.rpc.userApi.c("changeEmailAandPhone",params).success(function(msg){
                	nb.AlertTip.auto(msg);
                    m.fireEvent("afterChangeEmailAandPhoneWidgetSave");
                });
            };
            nb.uiTools.validatePassword("",  _remote);
            
        },
        __init__:function(){
            var self = this;
            $(self._panel_id + " .op_bar a[name=save]").bind("click", function(){
                self.save();
               
            });
            
            self._render();
        }
    };
    
    
    m.changeUsernameWidget = {
        _panel_id: "#panel_0004",
        viewModel: kendo.observable({ username:""}),
        _render: function(){
            var self = this;
            kendo.bind($(self._panel_id + " .box:first"), self.viewModel);
        },
        _validate: function(username){
            var self = this;
            var em = $(self._panel_id + " div.validateErrorMsg");
            var rules = {username: {method:"regex", exp:/^\w{6,28}$/}};
            var messages = {username:"登陆名输入错误，6~28位字母或数字或_组成"};
            var validator = new nb.xutils.Validator(em, rules, messages);
            var params = {username:username};
            return validator.validate(params);
            
        },
        _checkUsernameValid:function(username){
            var self = this;
            username = $.trim(username);
            if($.isEmptyObject(username)){
                nb.AlertTip.warn("检测前，请填写用户名！");
                return;
            }
            if(!/^\w{6,28}$/.test(username)){
                nb.AlertTip.warn("用户名格式不正确，无法申请此用户名！(6~28位字母或数字或_组成)");
                return;
            }
            nb.rpc.userApi.c("checkUsernameValid",{username:username}).success(function(valid){
                    if(!valid){
                        nb.AlertTip.warn("无法申请此用户名，可能已经被使用！");
                    }
                    else{
                        nb.AlertTip.info("可申请此用户名");
                    }
            });
        },
        save: function(){
            var self = this;
            var params = {uid:userId};
            $.extend(params, self.viewModel.toJSON());
            nb.xutils.trimObj(params);
            var fg = self._validate(params.username);
            if(! fg ) return;
           
            nb.rpc.userApi.c("changeUsername",params).success(function(msg){
                m.fireEvent("afterChangeUsernameWidgetSave");
                nb.AlertTip.auto(msg);
            });
            
        },
        __init__:function(){
            var self = this;
            $(self._panel_id + " .op_bar a[name=save]").bind("click", function(){
                self.save();
            });
             $(self._panel_id + " a[name=checkUsernameValid]").bind("click", function(){
                 var username = self.viewModel.username;
                 self._checkUsernameValid(username);
             });
            self._render();
        }
    };
    
    
    var _validateBaseInfoParams=function(params){
        var em = $("#editInfosWin div.validateErrorMsg");
        var rules = {
            originalName:"required",
            companyName:"required"
        };
        var messages = {
            companyName:"公司名称必填项",
            originalName:"姓名为必填项"
        };
        var validator = new nb.xutils.Validator(em, rules, messages);
        return validator.validate(params);            
    };
        
    var editInfos = function(){
        var params=nb.uiTools.mapFields("#editInfosWin");
        params.icon = $("#editInfosWin img").attr("src");
        
        if(!_validateBaseInfoParams(params)){return;}
        nb.rpc.userApi.c("editInfos", params)
        .success(function(msg){
            nb.AlertTip.storeCookie(msg);
            nb.uiTools.closeEditDialogWin("#editInfosWin");
            location.reload();
        });
    }
    
    $(document).ready(function(){
        
        
        $("#user_left_menus li a").bind("click", function(){
            var actionName = $(this).attr("name");
            $("#user_left_menus li a").each(function(){$(this).removeClass("selectedMenu");})
            $(".panel.swich").hide();
            if(actionName == "addBilling"){
            	var _types=["Device","Network","Website","Bootpo","ShortcutCmd"];
            	$.each(_types, function(i, name){
            		var numBox = $("#addBillingWidget input.number[name="+name+"]").data("kendoNumericTextBox");
            		numBox.value(0);
            	});
            }
            $(".panel.swich[actionName=" + actionName + "]").show();
            $(this).addClass("selectedMenu");
        });
        
        $("div.panelContent div.op_bar a[action=edit_infos]").bind("click",function(){       
            nb.uiTools.showEditDialogWin(null, "#editInfosWin", {width:600, height:300, title:"用户资料修改"});         
        })
        
        $("#editInfosWin a[action=selectIcon]").bind("click",function(){
            nb.uiTools.showEditDialogWin(null, "#user_icons_select_div_win", {width:640, height:300, title:"选择头像"});         
        })
        
        $("#user_icons_select_div_win img").bind("click",function(){
             var src = $(this).attr("src");
             $("#editInfosWin img").attr("src",src);
             nb.uiTools.closeEditDialogWin("#user_icons_select_div_win");
        })
        
         $("#editInfosWin .win_opbar button.ok").bind("click",function(){
                editInfos();
        });
        

        $("#editInfosWin").bind("keypress",function(e){
            if(e.keyCode == 13){
                editInfos();
            }
        })

        
        m.changePasswordWidget.__init__();
        m.changeEmailAandPhoneWidget.__init__();
        m.changeUsernameWidget.__init__();
        m.viewInfoWidget.reload();
        
        
    });
    
    
})(jQuery);
