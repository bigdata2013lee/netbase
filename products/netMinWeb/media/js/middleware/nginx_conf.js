(function($){
    var m = window.nginx_add = new nb.xutils.Observer();
    
    m.editNginxWidget={
    	_panel_id:"#editNginxWidget",
    	_validate:function(params){
	        var self = this;
	        var em = $(self._panel_id + " div.validateErrorMsg");
	        var messages = {};
	        var rules = {
	        	port:"port"
	        };
	        var validator = new nb.xutils.Validator(em, rules, messages);
	        return validator.validate(params);
    	},
    	saveConf:function(){
    		var self = this;
    		var params = nb.uiTools.mapFields(self._panel_id + " .fields_div");
    		nb.xutils.trimObj(params);
    		params.ssl = nb.xutils.val2boolean(params.ssl);
    		console.info(params);
    		if(! self._validate(params)){ return; }
    		nb.rpc.middlewareViews.c("editNginx", params)
    		.success(function(msg){
    			nb.AlertTip.auto(msg);
    		})
    	},
    	__init__:function(){
    		var self = this;
    		$(self._panel_id + " .op_bar a").each(function(){
    			$(this).bind("click",function(){ self[$(this).attr("action")](); })
    		}); //end bind  click-->action
    	}
    };
    
    m.thresholdConfigWidget= nb.BaseWidgets.extend("thresholdConfigWidget",{
        _panel_id: "#thresholdConfigWidget",
        _getMoUid: function(){return window.moUid},
        _moType:"MwNginx"
    });
    
    
    
    $(document).ready(function() {
        m.editNginxWidget.__init__();
        m.thresholdConfigWidget.__init__();
        m.thresholdConfigWidget.reload();
    });
 
})(jQuery);
