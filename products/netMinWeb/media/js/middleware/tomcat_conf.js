(function($){
    var m = new nb.xutils.Observer();
    
    m.editTomcatWidget={
    	_panel_id:"#editTomcatWidget",
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
    		nb.rpc.middlewareViews.c("editTomcat", params)
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
        _moType:"MwTomcat"
    });
    
    
    
    $(document).ready(function() {
        m.editTomcatWidget.__init__();
        m.thresholdConfigWidget.__init__();
        m.thresholdConfigWidget.reload();
    });
 
})(jQuery);
