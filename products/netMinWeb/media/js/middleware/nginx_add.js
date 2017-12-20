(function($){
    var m = window.nginx_add = new nb.xutils.Observer();
    
    m.addNginxWidget={
    	_panel_id:"#addNginxWidget",
    	_validate:function(params){
	        var self = this;
	        var em = $(self._panel_id + " div.validateErrorMsg");
	        var messages = {"host":"请填写正确的域名/IP",collector:"请选择收集器"};
	        var rules = {
	        	host:function(val){
	        		var v1 = nb.xutils.isValidUrl(val);
	        		var v2 = nb.xutils.isValidIp(val);
	        		return  v1 || v2;
	        	},
	        	port:"port",
	        	collector:"required"
	        };
	        var validator = new nb.xutils.Validator(em, rules, messages);
	        return validator.validate(params);
    	},
    	saveConf:function(){
    		var self = this;
    		var params = nb.uiTools.mapFields(self._panel_id + " .fields_div")
    		nb.xutils.trimObj(params);
    		params.ssl = nb.xutils.val2boolean(params.ssl);
    		console.info(params);
    		if(! self._validate(params)){ return; }
    		nb.rpc.middlewareViews.c("addNginx", params)
    		.success(function(msg){
    			nb.AlertTip.storeCookie(msg);
    			window.location.href = "/middleware/nginx_list/";
    		})
    	},
    	__init__:function(){
    		var self = this;
    		$(self._panel_id + " .op_bar a").each(function(){
    			$(this).bind("click",function(){ self[$(this).attr("action")](); })
    		}); //end bind  click-->action
    	}
    }
    
    
    
    $(document).ready(function() {
        m.addNginxWidget.__init__();
        
    });
 
})(jQuery);
