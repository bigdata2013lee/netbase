(function($){
	
	var xutils = nb.nameSpace("xutils");
    
//--------------------------------------------验证器----------------------------------------------------/
    xutils.Validator = nb.Class({
        __init__:function(errorEl, rules, messages){
            var self = this;
            self.errorEl = errorEl;
            self.rules = $.extend({}, rules);
            //self.messages = $.extend({}, messages);
            self.messages = messages||{};
        },
        error: function(msg){
            this.errorEl.html(msg);
            this.errorEl.show();
        },
        clear:function(){
            this.errorEl.html("");
            this.errorEl.hide();
        },
        validate:function(params){
            var self =this;
            var rs = true;
            $.each(self.rules, function(name, method){ //简写内置方法名，单个参数
                var fg = true;
                if(typeof(method) === "string"){
                    var method =  xutils.Validator[method];
                    var param = params[name];
                    fg = method(param);
                }
                
                else if(typeof(method) === "object" && method.method=="confirmPassword" && method.eqto){//confirm_password
                    //{method:"confirmPassword", eqto:"other attr name"}
                    var eqto = method.eqto;  
                    var val = params[name];
                    var other = params[eqto];
                    var method =  xutils.Validator[method.method];
                    fg = method(val, other);
                }
                
                else if(typeof(method) === "object" && method.method=="regex" && method.exp){//regex
                    //{method:"regex", exp:"regex exp"}
                    var exp = method.exp;
                    var method =  xutils.Validator[method.method];
                    var val = params[name];
                    fg = method(val, exp);
                }
                
                else if(typeof(method) === "object" && method.method=="norequired" && method.rule){//regex
                    var rule = method.rule;
                    var method =  xutils.Validator[method.method];
                    var val = params[name];
                    fg = method(val, rule);
                }
                
                else if(typeof(method) == "function"){
                    var val = params[name];
                    fg = method(val);
                }
                
                
                if(fg == false){
                    rs = false;
                    var msg = self.messages[name] || method.message || "No message!";
                     self.error(msg);
                     return false;
                }
                
                
            });
            if(rs){self.clear()}
            return rs;
        }
    });
    
    
    
    /**
     * 无参规则:必填
     * @param {Object} val 
     */
    xutils.Validator.required=function(val){
        return !xutils.isEmpty(val);
    };
    xutils.Validator.required.message = "必填项目，请重新输入";
    
    /**
     * 带参规则:非必填，但填了，必须满足指定的规则
     * @param {Object} reule 指定满足的规则
     * @param {Object} val 
     */
    xutils.Validator.norequired=function(val, rule){
        if(xutils.isEmpty(val)){return true}
        if(typeof rule === "string"){
            return xutils.Validator[rule](val);
        }
        else if(typeof rule === "function"){
            return rule(val);
        }
        return  true;
    };
    xutils.Validator.norequired.message = "非必填项目，可以不填写，如果填写了，须填写正确的数据";
    
    /**
     * 无参规则:邮件验证
     * @param {Object} val 
     */    
    xutils.Validator.email=function(val){
        return xutils.isVaildEmail(val);
    };
    xutils.Validator.email.message = "你输入的邮件地址不正确，请重新输入";
    
    /**
     * 无参规则:IP验证
     * @param {Object} val 
     */    
    xutils.Validator.ip=function(val){
        return xutils.isValidIp(val);
    };
    xutils.Validator.ip.message = "你输入的IP地址不正确，请重新输入";

    /**
     * 无参规则:mac地址验证
     * @param {Object} val 
     */
    xutils.Validator.mac=function(val){
        return xutils.isValidMac(val);
    };
    xutils.Validator.mac.message = "你输入的Mac地址不正确，请重新输入";
    
    /**
     * 无参规则:url验证
     * @param {Object} val 
     */    
    xutils.Validator.url=function(val){
        return xutils.isValidUrl(val);
    };
    xutils.Validator.url.message = "你输入的域名或Url不正确，请重新输入";
    
    /**
     * 无参规则:手机、电话验证
     * @param {Object} val 
     */    
    xutils.Validator.phone= function(val){
        return xutils.isVaildPhone(val);
    }
    xutils.Validator.phone.message = "你输入的电话格式不正确，请重新输入";
    
    /**
     * 无参规则:端口验证
     * @param {Object} val 
     */    
    xutils.Validator.port= function(val){
        var exp = /^\d+$/
        if(!exp.test(val))return false;
        val  = val *1;
        if(val >=1 && val <= 65536) return true;
        return false;
    }
    xutils.Validator.port.message = "你输入的端口不正确（1~65536），请重新输入";
    
    /**
     * 带参规则:正则验证
     * @param {Object} exp 正则表达式
     * @param {Object} val 
     */    
    xutils.Validator.regex= function(val,exp){
        return exp.test(val)
    }
    xutils.Validator.regex.message = "你输入格式不正确，请重新输入";
    
    /**
     * 带参规则:
     * @param {Object} eqto 密码项的key
     * @param {Object} val 
     */    
    xutils.Validator.confirmPassword= function(val, eqto){
        return val == eqto;
    }
    xutils.Validator.confirmPassword.message = "你输入的确认密码不一致";
    
	
	
})(jQuery);
