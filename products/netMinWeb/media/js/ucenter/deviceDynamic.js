(function($){
	//前台用户中心的运维社区，设备动态页面的js文件 【2014.12.19  jenny】
    var m = new nb.xutils.Observer();

    $(document).ready(function(){
        //数据列表的监控项目字段值的显示
        $(".componentType").each(function(){
            var componentType = $(this).attr("componentType");
            var componentTypeList = {Device:"主机",Website:"站点",Process:"进程",Network:"网络",Firewall:"防火墙",IpInterface:"接口",IpService:"IP服务",FileSystem:"磁盘",Bootpo:"开机",MwApache:"中间件",MwTomcat:"中间件",MwNginx:"中间件",}
            if (!componentTypeList[componentType]) {
            	$(this).html(componentType);
            }else{
            	$(this).html(componentTypeList[componentType]);
            }
        });
    });   
})(jQuery);