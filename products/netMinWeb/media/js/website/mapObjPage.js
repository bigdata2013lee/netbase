   var mapObj = {};
    var mapObjPage={
        max:2,
        __init__:function(){
            var self = this;
        
            $("#coll_point_select_div :checkbox").bind("click", function(evt){
            
                var checked = $(this).prop("checked");
                if(checked){
                    if($("#coll_point_select_div :checkbox:checked").size() > self.max){
                        nb.AlertTip.auto("warn:最多允许选择"+self.max+"个收集点.");
                        return false;
                    }
                }
                var ssName=$(this).attr("ss");
                console.info(mapObj[ssName]);
                mapObj[ssName].attr({fill: checked ? '#feb41c':"#AAD5FF"});
            });
            
            $("#coll_point_select_div :checkbox").each(function(){
                var checked = $(this).prop("checked");
                var ssName=$(this).attr("ss");
                mapObj[ssName].attr({fill: checked ? '#feb41c':"#AAD5FF"});
            });
            
        },
        getSelectCollPoints:function(){
            var points=[];
            $("#coll_point_select_div :checkbox").each(function(){
                var checked = $(this).prop("checked");
                if(!checked)return;
                var _p = {
                    pid:$(this).val(),
                    ss:$(this).attr("ss"),
                    title:$(this).parent().text()
                };
                points.push(_p);
            });
            return points;
        },
        
        setSelectCollPoints:function(collPoints){
            $.each(collPoints, function(i, p){
                $("#coll_point_select_div :checkbox[value="+p.pid+"]").prop("checked", true);
                mapObj[p.ss].attr({fill: '#feb41c'});
            })
        }
        
    };
    var _stateData={
    
        heilongjiang: {'diabled':true},
        jilin: {'diabled':true}, 
        liaoning: {'diabled':true}, 
        hebei: {'diabled':true}, 
        shandong: {'diabled':true}, 
        jiangsu: {'diabled':true}, 
        zhejiang: {'diabled':true}, 
        anhui: {'diabled':true}, 
        henan: {'diabled':true}, 
        shanxi: {'diabled':true}, 
        shaanxi: {'diabled':true}, 
        gansu: {'diabled':true}, 
        jiangxi: {'diabled':true}, 
        fujian: {'diabled':true}, 
        hunan: {'diabled':true}, 
        guizhou: {'diabled':true}, 
        sichuan: {'diabled':true}, 
        yunnan: {'diabled':true}, 
        qinghai: {'diabled':true}, 
        hainan: {'diabled':true}, 
        chongqing: {'diabled':true}, 
        tianjin: {'diabled':true}, 
        beijing: {'diabled':true}, 
        ningxia: {'diabled':true}, 
        neimongol: {'diabled':true}, 
        guangxi: {'diabled':true}, 
        xinjiang: {'diabled':true}, 
        xizang: {'diabled':true}, 
        taiwan: {'diabled':true}, 
        macau: {'diabled':true},
        hubei: {}, 
        shanghai: {}, 
        guangdong: {}, 
        hongkong: {}
    }
    $(document).ready(function(){
        $('#my_china_map_box').SVGMap({
            external: mapObj,
            mapName: 'china',
            showTip: true,
            mapWidth: 500,
            mapHeight: 320,
            stateInitColor: 'AAD5FF',
            stateHoverColor: 'feb41c',
            stateSelectedColor: 'AAD5FF',

            stateData:_stateData,
            clickCallback: function (stateData, obj) {
                console.info(obj);
            }
        });
        
        
        mapObjPage.__init__();

    })