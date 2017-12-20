(function($){

    var skinDir = "/media/customMap/skins/";
	var getPager = function(){return Ncm.core.paper;}
    var getCanvasContiner = function(){return $("#canvas_continer")}
    Ncm.viewfor = "BrowseMode";
    var m = Ncm.Viewer = new Ncm.Observer();;
    m.loadMap=function(){
    	nb.rpc.customerMapViews.c("map_getMapData", {mcUid:window.mcUid}).success(function(mapData){
        	Ncm.core.loadFromJson(mapData);
        	m.fireEvent("afterLoadMap");
        });
    };
    
        
    /**　更新流量线的滤镱　*/
    m.updateLinesGradient = function(){
    
        var fillLineGradient=function(conn, from_rates, to_rates){
            var finLevel = 6, foutLevel = 6, tinLevel = 6, toutLevel = 6;
            
            finLevel = Ncm.utils.rateLevel(from_rates ? from_rates.inputRate:-1);
            foutLevel = Ncm.utils.rateLevel(from_rates ? from_rates.outputRate : -1);
        
            tinLevel = Ncm.utils.rateLevel(to_rates ? to_rates.inputRate : -1);
            toutLevel = Ncm.utils.rateLevel(to_rates ? to_rates.outputRate : -1);
            
            var g = Ncm.utils._createFlowGradient(finLevel, foutLevel, tinLevel, toutLevel);
        
            if(getPager().raphael.svg){
                var oTransform = conn.line.attr('transform');
                conn.line.attr({'transform': ''});
                conn.line.attr({'fill': g});
                conn.line.attr({'transform': oTransform});
            }
            else{
                conn.line.attr({'fill': g});
            }
        
        }
        for(var i = 0; i < Ncm.core.connections.length; i++){
            var conn = Ncm.core.connections[i];
            //var dir = conn.from.getCenterPonit().x - conn.to.getCenterPonit().x >= 0 ?  '<' : '>'; //方向
            fillLineGradient(conn, conn.from.throughRates, conn.to.throughRates);
            
            
        }
        
    };
        
//---------------------------------------------------------------------------------------------------//
    m.updateDevsStatus = function(){
    	var mos = [];
    	$.each(Ncm.core.components, function(name, cmo){
    		if(cmo && cmo instanceof Ncm.CustomMapObjDev){
    			mos.push({moUid:cmo.cnf.id, moType:cmo.cnf.moType});
    		}
    	});
    	
    	nb.rpc.customerMapViews.c("map_getDevsMainInfo", {mos:mos}).success(function(mosInfos){
    		$.each(mosInfos, function(i, info){
	    		cmo = Ncm.core.components["CustomMapObjDev_" + info.moUid];
	    		if(! cmo){return;}
	    		cmo.setStatus(info.status);
    		}); //end of each
    	});
    		
    };
    
    
    m.updateIfacesStatus = function(){
    	var mos = [];
    	$.each(Ncm.core.components, function(name, cmo){
    		if(cmo && cmo instanceof Ncm.CustomMapObjIf){
    			mos.push({moUid:cmo.cnf.id});
    		}
    	});
    	
    	nb.rpc.customerMapViews.c("map_getIfacesMainInfo", {mos:mos}).success(function(mosInfos){
    		$.each(mosInfos, function(i, info){
	    		cmo = Ncm.core.components["CustomMapObjIf_" + info.moUid];
	    		if(! cmo){return;}
	    		cmo.setStatus(info.status);
	    		cmo.getThroughValues = info.getThroughValues; //流量
	    		cmo.throughRates = info.throughRates; //流量比
    		}); //end of each
    	});
    		
    };
    
    m.pageTo=function(mcObj){
    	console.info(mcObj);
    	var moType = mcObj.cnf.moType;
    	var id = mcObj.cnf.id;
    	var status = mcObj.status;
    	
    	if(!(moType == "Device" || moType == "Network")){return;}
    	if(!(status=="up" || status == "down" || status == "warning")){return;}
    	
    	var _baseUrls = {Device:"/monitor/device/", Network:"/network/network/"} 
    	var url = _baseUrls[moType] + id
    	var detailPage = window.parent.open(url,"monitor_obj_detail_page");
    	console.info(detailPage);
    }


	m.showTip=function(mcObj){
		if(mcObj.cnf.className == "CustomMapObjVir")return;
		var xy = {clientX:mcObj.cnf.p.x + mcObj.cnf.p.w/2-70, clientY:mcObj.cnf.p.y + mcObj.cnf.p.h/2};
		var  pxy = Ncm.utils.mousePoint2pagePoint(xy);
		clearTimeout(m.showTip.timer);
		m.showTip.timer = setTimeout(function(){$("#mo_tips").hide()}, 1000*8);
		$("#mo_tips").show().css({left:pxy.x +'px', top:pxy.y+'px'});
		
		
		
		var cnf = mcObj.cnf;
		var text = "";
		if(cnf.moType == "Device"){
			text += "服务器:" + cnf.label.text + "<br/>";
			text += "状态:" + mcObj.status + "<br/>";
		}
		
		if(cnf.moType == "Network"){
			text += "网络设备:" + cnf.label.text + "<br/>";
			text += "状态:" + mcObj.status + "<br/>";
		}
		if(cnf.className == "CustomMapObjIf"){
			
			text += "接口:" + cnf.label.text + "<br/>";
			text += "状态:" + mcObj.status + "<br/>";
			text += "流入:" + Ncm.utils.byte2readable(mcObj.getThroughValues ? mcObj.getThroughValues.input : null, true, 1024, "NA")  + "<br/>";
			text += "流出:" + Ncm.utils.byte2readable(mcObj.getThroughValues ? mcObj.getThroughValues.output : null, true, 1024, "NA") + "<br/>";
		}
		
		
		$("#mo_tips").html(text);
	}
    
//---------------------------------------------------------------------------------------------------//    
    var autoUpdate=function(){
    	var _f = function(){
	    	m.updateDevsStatus();
	    	m.updateIfacesStatus();
    	}
    	m.on("afterLoadMap", function(){
    		_f();
    	});
    	setInterval(function(){_f()}, 1000*20);
    	
    	setInterval(function(){m.updateLinesGradient()}, 1000*5);
    	
    }
    
    
    
    $(document).ready(function(){
        m.loadMap();
    	autoUpdate();
    });

})(jQuery)