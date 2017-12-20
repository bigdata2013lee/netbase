(function($){
    var m = new nb.xutils.Observer();
    m.connPerfsWidget = nb.BaseWidgets.extend("baseMultiplePerfImgWidget",{
        title:"连接数性能趋势图",
        timeUnit:"day",
        _panel_id:"#connPerfsWidget",
        remoteView:nb.rpc.middlewareViews,
        remoteMethod:"getTomcatConnPerfs",
        getRemoteParams: function(){
            var self = this;
            return {uid: window.moUid, timeUnit:self.timeUnit};
        },
        
        afterRemote: function(datas){

        },
        __init__: function(){
            var self = this;
            self.reload(); 
        }
    });
    

    
    
    $(document).ready(function() {
        m.connPerfsWidget.__init__();
    });
 
})(jQuery);
