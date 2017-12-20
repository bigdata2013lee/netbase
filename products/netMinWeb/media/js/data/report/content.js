(function($){
    
    var m = window.description = new nb.xutils.Observer();
    
    m.on("afterCommDeviceWidgetReload", function(){
        //var email = m.viewInfoWidget._data.email;
        //var contactPhone = m.viewInfoWidget._data.contactPhone;
        
        //m.changeEmailAandPhoneWidget.viewModel.set("email",email);
        //m.changeEmailAandPhoneWidget.viewModel.set("contactPhone",contactPhone);
    });
       
       
    m.CommDeviceWidget = {        
        _panel_id: "#panel_0001",
        _data:null,
        _render: function(){
            var self = this;
            var template = self.getTemplate();
            $(self._panel_id + " .box:first").html(template(self._data));            
        },
        getTemplate: function(){
            var template = kendo.template($(this._panel_id + " script[name=template]").html());
            return template;
        },
        reload:function(){
            var self = this; 
            nb.rpc.userApi.c("getUserInfo", {uid:userId}).success(function(user){
                self._data = user;
                self._render();
                m.fireEvent("afterCommDeviceWidgetReload");
            });
        }
    };
    
    m.DevicesPerWidget = {
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
                oldPassword: {method: "regex", exp: /^\w{6,16}$/}, 
                newPassword: {method: "regex", exp: /^\w{6,16}$/},
                confirmPassword:{method:"confirmPassword", eqto: "newPassword"} 
            };
            var messages = {oldPassword:"请输入6~16位的旧密码", newPassword:"请输入6~16位的新密码,只能包涵数字、字母、下划线，并区分大小写"};
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
           
            nb.rpc.userApi.c("changePassword",params).success(function(msg){
                nb.AlertTip.info(msg);
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
    
    $(document).ready(function(){
        $("#report_left_menus li a").bind("click", function(){
            var actionName = $(this).attr("name");
            $(".panel.swich").hide();
            $(".panel.swich[actionName=" + actionName + "]").show();            
        });
        
        m.DevicesPerWidget.__init__();
        m.CommDeviceWidget.reload();
    });
})(jQuery);
