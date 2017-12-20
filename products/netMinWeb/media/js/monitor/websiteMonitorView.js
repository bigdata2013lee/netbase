(function ($) {
    var monitorIndex = NB.nameSpace("monitorIndex");
     window.Highcharts.setOptions({
        global : {
            useUTC : false
        },
        lang : {
            shortMonths : ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', 
            '九月', '十月', '十一月', '十二月'],
            weekdays : ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'],
            rangeSelectorFrom:"从",
            rangeSelectorTo:"至",
            rangeSelectorZoom:"缩放"

        }
    }); 
    
     var buttons = [
        {type:'hour',count: 1, text:'1H'},
        {type:'hour',count: 3, text:'3H'},
        {type:'day',count: 1, text:'1D'},
        {type:'day',count: 7, text:'7D'}
    ];
    var series = [
            {
                name:"等待响应",
                data:[
                    [1362547885941,10],
                    [1362634285941,30],
                    [1362720685941,60],
                    [1362807085941,10],
                    [1362893485941,19],
                    [1362979885941,12],
                    [1363066285941,60],
                    [1363152685941,90]
                ],
                type : 'spline',
                marker : {
                    enabled : true,
                    radius : 5
                },
                shadom:true,
                tooltip : {
                    valueDecimals : 2
                }
            },
            {
                name:"接收数据",
                data:[
                    [1362547885941,20],
                    [1362634285941,40],
                    [1362720685941,80],
                    [1362807085941,60],
                    [1362893485941,29],
                    [1362979885941,22],
                    [1363066285941,30],
                    [1363152685941,120]
                ],
                type : 'spline',
                marker : {
                    enabled : true,
                    radius : 5
                },
                shadom:true,
                tooltip : {
                    valueDecimals : 2
                }
            }
    ];
    
    
    var renderWebsite001Weight = function(){
        if($("#container_website_time").size() == 0) return;
        var chart = new Highcharts.StockChart({
            chart : {renderTo : "container_website_time"},
            legend : {
                layout : 'vertical',align : 'right',enabled : true,
                verticalAlign : 'top',x : -10, y : 100, borderWidth : 0
            },
            rangeSelector : {
                 selected : 0,
                 buttons:buttons
            },
            title : {text : "test"},
            exporting : false,
            series : series
        }); 
        
    };
        
    var renderDefault01Weight = function(){
        if($("#container_website_cur").size() == 0) return;
        var chart = new Highcharts.Chart({
            chart: {
                renderTo: 'container_website_cur',
                type: 'column'
            },
            title: {
                text: 'Web Site Reponse-time/ms'
            },
            xAxis: {
                categories: ['max','min','avg']
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'reponse-time/ms'
                }
            },
            tooltip: {
                formatter: function() {
                    return ''+
                        this.x +': '+ this.y +' ms';
                }
            },
            plotOptions: {
                column: {
                    pointPadding: 0.2,
                    borderWidth: 0
                }
            },
                series: [{
                name: '响应时间',
                data: [49.9, 83.6, 48.9]
    
            }]
        });
        
    };
    //------------------------------ready----------------------------------------//
    monitorIndex.TabPageLoador.on('Website_view_ready', function() {
        renderDefault01Weight();
        renderWebsite001Weight();
        

        
        
    }); //end doc ready
})(jQuery);