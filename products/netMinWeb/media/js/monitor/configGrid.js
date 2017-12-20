(function($){
	
	var ns = nb.nameSpace("devicesConfigGridView");
	var m = new nb.xutils.Observer();
	var ps = {};
	var _ds=null;
	var _queryConditions = {};
	var _columns = [
		{field: "title", sortable: true, title: "名称", width:200},
		{field: "manageIp", width:120, sortable: true, title: "ip地址"},
		{width:120,title: " ", template:'<a href="/monitor/devicesConfigOp/#=_id#">配置</a> <a href="javascript:" name="delDevice" moUid="#=_id#">删除</a>'},
	];
	
	var pageReload=function(){
		window.location.reload();
	};
	
	var testInputPortString = function(val){
                var flag = false;
                var exp = /^([1-9]+[0-9]*(\,)?)+$/;
                if(exp.test(val)){
                    if(val.substr(-1) ==  ","){
                        val = val.slice(0, -1);
                    }
                    var ports = val.split(",");
                    if(ports.length > 3) return false;
                    for(var i=0; i<ports.length; i++){
                        if(ports[i]*1 > 65535 ){
                            flag = false;
                            break;
                        }else{
                            flag = true;
                        }
                    }
                }
                return flag;            
    };	
    
	ns.getSelectMos=function(){
		var rs = []
		$("#data-grid input[name=mo_uid]:checked").each(function(){
			rs.push({uid:$(this).val()})
		});
		
		return rs;
	};
    var parameterMap = function() {
    	return {"orgUid":window.orgUid, "locUid":window.locUid};
    }	

    var getDs = ns.getDs = function(methodName){
        if(_ds) return _ds;
        var ds = new kendo.data.DataSource({
            type : "json",
            pageSize : 200,
    
            transport : {
                read : nb.rpc.monitorViews.rc("listDevicesForConfigGrid", parameterMap)
            }
        });
        _ds = ds;
        return _ds;
    }
    
    

	var createGrid=function(){
		$("#data-grid").kendoGrid({
            dataSource : getDs(),
            height : 500,
            scrollable:true,
            sortable : true,
            //resizable: true,
            pageable:true,
            //columnMenu: true,
            columns: _columns 
        });
		
	}
	
	

        
   var delDevice =  function(moUid){
        nb.uiTools.confirm("你确定要删除此设备吗？<br/>注意：删除后，与此设备相关的性能数据将无法恢复!", function(){
	        nb.rpc.deviceViews.c("delDevice", {uid: moUid}).success(function(msg){
                nb.AlertTip.storeCookie(msg);
                pageReload();
		    });
            
        });
	}
        
	//------------------------------------------------------------------------------//
	
	var  _selectHcType=function( panel_id, hcType){
            var box = $(panel_id + " .box:first");
            if(hcType == "port"){
                 box.find("li.hcPorts").show();
            }else{
                box.find("li.hcPorts").hide();
            }
      };
      
	m.deviceAddWidget = {
	    _panel_id: "#addDevicePage",
	    _defalutSnmpConfig : {
	        "booleans":[{text:"是", val:"true"}, {text:"否", val:"false"}], //附加显示的
	        "snmpVers":["v2c", "v3", "v1"], //附加显示的
            "netSnmpTimeout": 3,
            "netMaxOIDPerRequest": 40,
            "netSnmpPrivPassword": null,
            "netSnmpTries": 2,
            "netSnmpMonitorIgnore": "false",
            "netSnmpAuthType": null,
            "netSnmpPrivType": null,
            "netSnmpCommunity": "public",
            "netSnmpAuthPassword": null,
            "netSnmpVer": "v2c",
            "netSnmpPort": 161,
            "netSnmpSecurityName": null
	    },
	    
	   
	    
	    _defalutCommConfig:{
            "netCommandPassword": "netbase",
            "netCommandCommandTimeout": 15,
            "netCommandLoginTimeout": 10,
            "netCommandPort": 22,
            "netKeyPath": "~/.ssh/id_dsa",
            "netCommandUsername": "root",
            "netSshConcurrentSessions": 10,
            "hcPorts":"80",
            "hcType": "ping"
	    },
	    
	     _source:{
            hcTypes:[{text:"PING",val:"ping"}, {text:"端口",val:"port"}],
            changehcType: function(e){
                var panel = $(e.target).closest("div.panel");
                var widget = panel.data("nbWidget");
                _selectHcType("#add_dev_panel_003", widget.commViewModel.hcType);
            }
        },
	    
	    
	    reload: function(){
	        
	    },
	    
	    _getBaseParams: function(){
	        var self = this;
	        var mainBox = $(self._panel_id);
	        var params = {};
	        params.manageIp = mainBox.find("input[name=manageIp]").val();
	        params.manageIp = $.trim(params.manageIp);
	        params.title = mainBox.find("input[name=title]").val();
	        params.description = mainBox.find("input[name=description]").val();
	        params.deviceCls = window.orgUid;
	        params.location = window.locUid;
	        params.collector = mainBox.find("select[name=collector]").val();
	        return params;
	    },
	        
	    _getSnmpConfigParams:function(){
	        var self = this;
	        var params = self.snmpViewModel.toJSON();
	        nb.xutils.delattrs(params, "booleans", "snmpVers");
	        params.netSnmpMonitorIgnore = nb.xutils.val2boolean(params.netSnmpMonitorIgnore);
	        return params;
	    },
        _getCommConfigParams:function(){
            var self = this;
            var params = self.commViewModel.toJSON();   
            nb.xutils.delattrs(params, "hcTypes");
            return params;
        },
	    
	    
	    
	    save: function(){
	        var self = this;
	        var baseParams = self._getBaseParams();
	        if(!nb.xutils.isValidIp(baseParams.manageIp)){
	            alert("你输入的管理ip不正确，请重新输入...");
	            return;
	        }
	        
	        if($.trim(baseParams.collector) == "" ){
                alert("请选择一个收集器...");
                return;
            }
            
            
            var commParams = self._getCommConfigParams();
            if(commParams.hcType == "ping" && commParams.hcPorts == ""){
                commParams.hcPorts = "80";
            } 
           
            var testport = commParams.hcPorts;
            if(!testInputPortString(testport)){
                alert("端口格式不对！多个端口，请用,号分开,最多只能填写3个端口！"); 
                return;
            }
            

	        var snmpParams = self._getSnmpConfigParams();
	        var params = {baseConfig: baseParams, snmpConfig:snmpParams, commConfig:commParams};
	        
	        var _remote = function(){
	        	var loading = nb.uiTools.commLoading.insertTo("body", "正在添加设备，请稍后...");
                nb.uiTools.closeEditDialogWin(self._panel_id);
    	        nb.rpc.deviceViews.c("addDevice", params).success(function(msg){
	                nb.AlertTip.storeCookie(msg);
	                pageReload();
    	        })
    	        .complete(function(){nb.uiTools.commLoading.cancel("body");});
	        };
	        
             _remote();
	        
	    },
	    
	    __init__:function(){
	        var self = this;
	        $("#add_dev_panel_003").data("nbWidget", this);
	        self.snmpViewModel = kendo.observable(self._defalutSnmpConfig);
	        self.commViewModel = kendo.observable($.extend({}, self._defalutCommConfig, self._source));
	        kendo.bind($("#add_dev_panel_002 .box:first"), self.snmpViewModel);
	        kendo.bind($("#add_dev_panel_003 .box:first"), self.commViewModel);
	        _selectHcType("#add_dev_panel_003", self.commViewModel.hcType);
	        $(self._panel_id + " #addDevicePage_btn button.ok").bind("click", function(){
	            self.save();
	        });
	        
	        
	        $( "#add_dev_panel_002 .box:first select[name=netSnmpVer]").bind("change", function(){

                if ($(this).val() == "v3"){
                    //console.info($(this).val());
                    $.each(snmpV3Attrs, function(i, snmpV3Attr){
                        $("#add_dev_panel_002 .box:first").find("input[name=" + snmpV3Attr +"]").prop("disabled",false);
                    });
                }else{
                    //console.info($(this).val());
                    $.each(snmpV3Attrs, function(i, snmpV3Attr){
                        $("#add_dev_panel_002 .box:first").find("input[name=" + snmpV3Attr +"]").prop("disabled", true);
                    });
                }    
            });
	        
	        
	        
	    }
	};
	
	

    //-----------------------------------------------------------------------------//
    
    
    hostTree.on("selectOrgNode",function(orgUid, uname, path, locUid){
        window.location.href = "/monitor/configGrid/"+orgUid + "/" + locUid;
    });
	
    hostTree.on("changeTreeNodeType", function(nodeType, uname){
        if(nodeType=="DeviceClass"){
            $("a[name=add_device]").removeClass("disable");
            
            if(uname == "devicecls"){
                $("a[name=add_device]").addClass("disable");
            }
        }
        else{
            $("a[name=add_device]").addClass("disable");
        }
        
        
    });	
	
	$(document).ready(function(){
		createGrid();
		m.deviceAddWidget.__init__();
		$("#mright-panel").delegate("a[name=delDevice]","click",function(){
			var moUid = $(this).attr("moUid");
			delDevice(moUid);
		})
		
		$("a[name=add_device]").bind("click", function(){
			if($(this).is(".disable")){return;}
			nb.uiTools.showEditDialogWin(null, "#addDevicePage",{width:880, height:600});
			$("#add_dev_panel_003").hide();
		})
	});
	
	
})(jQuery)
