(function($){
	
	var ns = nb.nameSpace("networksConfigGridView");
	var m = new nb.xutils.Observer();
	var ps = {};
	var _ds=null;
	
	var pageReload=function(){
		window.location.reload();
	};
	var _columns = [
		{field: "title", sortable: true, title: "名称", width:200},
		{field: "manageIp", width:120, sortable: true, title: "ip地址"},
		{width:120,title: " ", template:'<a href="/network/devicesConfigOp/#=_id#">配置</a> <a href="javascript:" name="delDevice" moUid="#=_id#">删除</a>'},
	];
	

    var parameterMap = function() {
    	return {"orgUid":window.orgUid};
    }	

    var getDs = ns.getDs = function(methodName){
        if(_ds) return _ds;
        var ds = new kendo.data.DataSource({
            type : "json",
            pageSize : 200,
    
            transport : {
                read : nb.rpc.networkViews.rc("listNetworksForConfigGrid", parameterMap)
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
	
	
	//-----------------------------------------------------------------------------------///
	

    
    //产品型号
    m.fillProductIdSelectWidget = {
        _panel_id: "#addNetworkWidget",
        _productIds: [],
        _lastPath:null,
        _render: function(){
            var self = this;                          
            var select = $(self._panel_id + " select[name=productId]");
            select.html('<option value="">请选择产品型号</option>');
            $.each(self._productIds, function(i, group){
                var optgroup = $(nb.xutils.formatStr('<optgroup label="{0}"></optgroup>', group.company));
                optgroup.appendTo(select); 
                $.each(group.productTypes, function(i, pType){
                	var option = $(nb.xutils.formatStr('<option value="{0}" networkClsPath="{2}">{1}</option>',pType, pType, group.path));
                	option.appendTo(optgroup);
                });
            });
 
        },
        
        reload: function(){
            var self = this;
            nb.rpc.networkViews.c("getDevTemplateMaps", function(){
                return {group: self._lastPath}
            }).
            success(function(productIds){
               self._productIds = productIds;
               self._render();
            });
        },
        
        __init__: function(){
            
            var self = this;
            networkTree.on("selectOrgNode", function(id, uname, path){
                var is2thLayer = /^\/\w+\/\w+$/.test(path); //是否为第二目录
                if(!is2thLayer) ;
                self._lastPath = uname;
                ps.group = uname;
                ps.currenttNetworkClsId = id;
                self.reload();
            });
            
        }
        
    };
    
    
    //添加网络设备组件
    m.addNetworkWidget = {
        _panel_id: "#addNetworkWidget",
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
        
        _selectHcType: function(hcType){
            var self = this;
            var widgetEl = $("#add_network_panel_003");
            if(hcType == "port"){
                 widgetEl.find("li.hcPorts").show();
            }else{
                widgetEl.find("li.hcPorts").hide();
            }
            
        },
        
        _source:{
            hcTypes:[{text:"PING",val:"ping"}, {text:"端口",val:"port"}],
            changehcType: function(e){
                widget = $("#addNetworkWidget").data("nbWidget");
                widget._selectHcType(widget.commViewModel.hcType);
            }
        },
        
        _getBaseParams: function(){
            var self = this;
            var mainBox = $(self._panel_id + " fieldset.baseInfoConfig");
            var params = {group:ps.group, parentId:ps.currenttNetworkClsId};
            mainBox.find("input, select").each(function(){
                params[$(this).attr("name")] = $(this).val();
            });
            params.networkClsPath = mainBox.find("select[name=productId] option:selected").attr("networkClsPath");
           
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
        
        validate:function(baseParams, snmpConfigParams, commConfigParams){
            var self = this;
            var em = $(self._panel_id + " div.validateErrorMsg");
            var exp = /^([1-9]+[0-9]*(\,)?)+$/;
            if(!exp.test(commConfigParams.hcPorts)){
                alert("端口格式不对！多个端口，请用,号分开！"); 
                return false;
            }
            var rules = null;
            var messages = null;
            if ("collector" in baseParams){
                rules = {manageIp:"ip", productId:"required", collector:"required"};
                messages = {productId:"请选择一个正确的产品类型", collector:"请选择一个收集器..."};
            }
            else{
                rules = {manageIp:"ip", productId:"required"};
                messages = {productId:"请选择一个正确的产品类型"};
            }
            var validator = new nb.xutils.Validator(em, rules, messages);
            return validator.validate(baseParams);
        },
        _render:function(){
            var self = this;
            self.snmpViewModel = kendo.observable(self._defalutSnmpConfig);
            self.commViewModel = kendo.observable($.extend({}, self._defalutCommConfig, self._source));
            kendo.bind($(self._panel_id + " fieldset.snmpConfig"), self.snmpViewModel);
            kendo.bind($(self._panel_id + " fieldset.commConfig"), self.commViewModel);
            self._selectHcType(self.commViewModel.hcType);
             
        },
        save:function(){
            var self = this;
            var baseParams = self._getBaseParams();
            var snmpConfigParams = self._getSnmpConfigParams();
            var commConfigParams = self._getCommConfigParams();
            var fg = self.validate(baseParams, snmpConfigParams, commConfigParams);
            if(!fg)return;
            var params = {baseConfig: baseParams, snmpConfig:snmpConfigParams, commConfig:commConfigParams};
            nb.rpc.networkViews.c("addNetworkDevice", params).success(function(msg){
                nb.AlertTip.storeCookie(msg);
                nb.uiTools.closeEditDialogWin(self._panel_id)
                pageReload();
            });
            
        },
        __init__: function(){
            var self  = this;
            $(self._panel_id).data("nbWidget", this);
            $(self._panel_id + " #addNetworkWidget_btn button.ok").bind("click", function(){
	            self.save();
	        });
            self._render();
        }
    }

        

    //删除网络设备组件
    m.delNetworkWidget = {
        reload: function(){
            
        },
        delNetwork: function(moUid){
            nb.rpc.networkViews.c("delNetwork", {uid: moUid}).success(function(msg){
            	nb.AlertTip.storeCookie(msg);
                pageReload();
            });
        },
        
        __init__:function(){
            var self = this;
            $("#data-grid").delegate("a[name=delDevice]", "click", function(){
                if(!window.confirm("你确定要删除此设备吗？\n注意：删除后，与此设备相关的性能数据将无法恢复!")){
                    return;
                }
                var moUid = $(this).attr("mouid")
                self.delNetwork(moUid)
            });
        }   
    };
    
    //-----------------------------------------------------------------------------//
    
	window.networkTree.on("selectOrgNode", function(orgUid, uname, path){
		window.orgUid = orgUid;
		getDs().read();
	})
	

    window.networkTree.on("selectOrgNode", function(id, uname, path){
               
        var is3thLayer = /^\/\w+\/\w+$/.test(path); //是否为第二目录
        if(!is3thLayer){
        	$("a[name=add_device]").addClass("disable");
        }
        else{
        	$("a[name=add_device]").removeClass("disable");
        }
      
    });
	
	$(document).ready(function(){
		createGrid();
		m.fillProductIdSelectWidget.__init__();
		m.addNetworkWidget.__init__();
		m.delNetworkWidget .__init__();
		
		$("a[name=add_device]").bind("click", function(){
			if($(this).is(".disable")){return;}
			nb.uiTools.showEditDialogWin(null, "#addNetworkWidget",{width:880, height:600})
		})
		
	});
	
	
})(jQuery)
