(function($){
    var m = new nb.xutils.Observer();


    m.responseTimePerfsWidget = nb.BaseWidgets.extend("baseMultiplePerfImgWidget",{
        title:"监测点响应时间性能趋势图",
        timeUnit:"day",
        _panel_id:"#responseTimePerfsWidget",
        remoteView:nb.rpc.websiteViews,
        remoteMethod:"getCptsResponseTimePerfs",
        getRemoteParams: function(){
            var self = this;
            return {websiteUid: window.moUid, timeUnit:self.timeUnit};
        },
        
        afterRemote: function(datas){
            $.each(datas, function(i, item){
                item.tooltip={ valueDecimals: 0,valueSuffix:' ms' };
            });
        },
        __init__: function(){
            var self = this;
            self.reload(); 
        }
    });

    $(document).ready(function(){
        m.responseTimePerfsWidget.__init__();
        
        var zt = new $.Zebra_Tooltips($('.noteInfo1'), {
            'position':     'right',
            default_position:"below",
            color:"#333",
            background_color:"#DDEEF5",
            'max_width':    300,
            content:"Lorem ipsum dolor sit amet consectetuer facilisis lacinia sapien ac et. Quis hendrerit neque congue pretium iaculis \
                justo laoreet orci elit left. Eros natoque Curabitur accumsan eget quis "
        });
        
        zt.show($('.noteInfo1'), false);
    
    
    })
            
})(jQuery)
