(function($){
	
	var  m = {};
    
    m.listAvailableBillingsWidget =  nb.BaseWidgets.extend("BaseListWidget", {
		_panel_id:"#listAvailableBillingsWidget",
		_btype:"", //主组件类型
		remoteMethod:"listAvailableBillings",
		remoteView:nb.rpc.billingViews,
		getRemoteParams: function(){var self=this; return {btype: self._btype};},
		getSelectBillingUid:function(){
			var self = this;
			return $(self._panel_id + " input[name=billingUid]:checked").val();	
		},
        __init__: function(){
            var self = this;
            var btype = $("#apply_billing_btn").attr("btype");
            self._btype = btype;
            
            //打开购买单窗口
            $("#apply_billing_btn").bind("click", function(){
            	nb.uiTools.showEditDialogWin(null, self._panel_id, {title:"可用的购买单...", width:700});
            	self.reload();
            });
            
            $(self._panel_id + " .win_opbar button.ok").bind("click", function(){
            	var  selectBillingUid = self.getSelectBillingUid();
            	$("#billingUid_text").text(selectBillingUid);
            	$("#billingUid_val").val(selectBillingUid);
            	nb.uiTools.closeEditDialogWin(self._panel_id);
            })
        }
	});
	
	
	$(document).ready(function(){
		m.listAvailableBillingsWidget.__init__();
	});

})(jQuery);