(function($){
    var m = window.customers = {};
    
    
    
    
    m.customersWidget = nb.BaseWidgets.extend("BaseListWidget",{
        _panel_id: "#customersWidget",
        remoteView:nb.rpc.idcViews,
        remoteMethod:"getUsers",
        
    })
    
    
    
    
    
    
    $(document).ready(function(){
        m.customersWidget.reload();
    });
    
    
})(jQuery);
