(function($){
    var m = new nb.xutils.Observer();
        
    m.recentlyEventsWidget = nb.BaseWidgets.extend("BaseListWidget", {
        _panel_id:"#recentlyEventsWidget",
        remoteMethod:"getWebsiteClsRecentlyEvents",
        remoteView:nb.rpc.websiteViews,
        getRemoteParams: function(){return {}}
    });
    

    m.responseTimeTop5Widget = {
        _panel_id:"#responseTimeTop5Widget",
        remoteMethod:"responseTimeTopN",
        remoteView:nb.rpc.websiteViews,
        getRemoteParams: function(){
            return {}
        },
        chartConf : {},
        afterRemote:function(data){
            var colors = Highcharts.getOptions().colors;
            data.series[0].type = 'column';
            data.series[0].name= "响应时间"
            var  ds = data.series[0].data
            $.each(ds, function(i, val){
                var _i = i + 1 > colors.length ? 0 : i;
                ds[i] = {y:val, color:colors[_i]};
            })
        },
        _render: function(data){
            var series = data.series;
            var categories = data.categories;
            console.info(data);
            var _charts = {
                title: {text: ' '},
                xAxis: { categories: categories, labels:{rotation:30}},
                yAxis: {
                    title: {text: '响应时间/ms'},min:0,
                    plotLines: [{value: 0, width: 1, color: '#808080'}]
                },
                tooltip: {pointFormat: '响应时间:<b>{point.y:.0f} ms.</b>'},
                legend:{enabled: false},
                series: series
            };
            _charts = $.extend(_charts, this.chartConf)
            $(this._panel_id + ' div.box:first').highcharts(_charts);
        },
        reload:function(){
            var self = this;
            nb.uiTools.panelLoading.insertTo(self._panel_id);
            var params = self.getRemoteParams ? self.getRemoteParams() : {};
            self.remoteView.c(self.remoteMethod,params)
            .success(function(data){
                nb.uiTools.panelLoading.cancel(self._panel_id);
                self.afterRemote(data);
                self._render(data);
            });

        },
        __init__: function(){
            var self  = this;
            $(self._panel_id + " .panelActions a[name=refresh_action]").bind("click", function(){self.reload()});
        }
    };
    
    $(document).ready(function(){
        m.recentlyEventsWidget.__init__();
        m.recentlyEventsWidget.reload();
        
        m.responseTimeTop5Widget.__init__();
        m.responseTimeTop5Widget.reload();
        
        $("#data_table_1").delegate("a[action=delWebsite]","click", function(){
            if(!window.confirm("你确定删除此站点?")){return;}
            nb.rpc.websiteViews.c("delWebsite",{uid: $(this).attr("websiteuid")})
            .success(function(msg){
                nb.AlertTip.storeCookie(msg);
                window.location.href="/website/index/";
            })
        });
        
    })
            
})(jQuery)
