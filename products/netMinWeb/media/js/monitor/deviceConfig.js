(function($){
	
	var m = window.deviceConfig = {};
	var ps = {currentDevId:window.moUid, currentDevClsId:null};
	
    var snmpV3Attrs = ["netSnmpPrivPassword", "netSnmpAuthType", "netSnmpPrivType", "netSnmpAuthPassword", "netSnmpSecurityName"];
	
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

	var displayDevConfigPage = function(fg){
		if(fg){
			$("#tabstrip").show();
			$("#tabstrip2").show();
		}
		else{
			$("#tabstrip").hide();
			$("#tabstrip2").hide();
		}
	};
	
  
	
	var _getUids = function(widget){
		var cUids = [];
		$(widget._panel_id + " table:first input[name=ids]:checked").each(function(){
			cUids.push($(this).val());
		});
		return cUids;
	};
	var DelDevComponentsWidget = {
			delDevComponents: function(){
			var self = this;
			var cUids = _getUids(self);
			if(!cUids || cUids.length == 0){return;}
			var _remote = function(){
    			self.remoteView.c("delDevComponents", {uid: ps.currentDevId, cType:self.cType, cUids:cUids}).
    			success(function(msg){ nb.AlertTip.auto(msg); self.reload(); });
			};
			nb.uiTools.confirm("你确定要删除选择的组件？", _remote);
		}
	};

	
	
	m.interfacesGridWidget = nb.BaseWidgets.extend("BaseListWidget",DelDevComponentsWidget, {
		_panel_id:"#panel_interfaces",
		cType:"IpInterface",
		remoteMethod:"getDevComponents",
		remoteView:nb.rpc.deviceViews,
		getRemoteParams: function(){ return {uid: ps.currentDevId, cType:"IpInterface"};},
        openThresholdConfigWin:function(moUid, moType){
            nb.uiTools.showEditDialogWin(null, "#thresholdConfigWin", {width:1000, height:400, title:"阀值配置..."});
            m.thresholdConfigWinWidget._moUid = moUid;
            m.thresholdConfigWinWidget._moType = moType;
            m.thresholdConfigWinWidget.reload();
        },
        setCustomSpeed: function(){
            var self = this;
            var viewModel = $("#setCustomSpeedWin").data("viewModel");
            var params = {ifaceUid: viewModel._id, customSpeed: viewModel.customSpeed};
            nb.uiTools.closeEditDialogWin("#setCustomSpeedWin");
            nb.rpc.deviceViews.c("setCustomSpeed", params)
            .success(function(msg){
                nb.AlertTip.auto(msg);
                self.reload();
            });

        },
		__init__: function(){
			var self = this;
			$(self._panel_id + " .op_bar a[name=del]").bind("click", function(){
				self.delDevComponents();
			});
			
			$(self._panel_id).delegate("a[name=configThreshold]", "click", function(){
			    var moUid = $(this).attr("moUid");
			    var moType = $(this).attr("moType");
			    self.openThresholdConfigWin(moUid, moType);
			});
			
			$(self._panel_id + " .op_bar a[name=setCustomSpeed]").bind("click", function(){
                var cUids = _getUids(self);
                if(!cUids || cUids.length == 0){ nb.AlertTip.warn("没有选择接口"); return;}
                if(cUids.length>1){nb.AlertTip.warn("请选择一个接口，请勿多选"); return;}
                var dataUid = $(self._panel_id + " table:first input[name=ids]:checked:first").closest("tr").attr("data-uid");
                if(nb.xutils.isEmpty(dataUid)) return;
                
                var rViewModel = self.ds().getByUid(dataUid);
                var viewModel = kendo.observable({cUid:cUids[0], CustomSpeed:100});
                nb.uiTools.showEditDialogWin(kendo.observable(rViewModel.toJSON()), 
                "#setCustomSpeedWin", {width:600, height:250, title:"设定自定义带宽..."});
			});
            
            $("#setCustomSpeedWin .win_opbar button.ok").bind("click", function(){
                self.setCustomSpeed();
            });
		}
	});
	
	m.processesGridWidget = nb.BaseWidgets.extend("BaseListWidget",DelDevComponentsWidget, {
		_panel_id:"#panel_processes",
		cType:"Process",
		remoteMethod:"getDevComponents",
		remoteView:nb.rpc.deviceViews,
		openThresholdConfigWin:function(moUid, moType){
            nb.uiTools.showEditDialogWin(null, "#thresholdConfigWin", {width:1000, height:400, title:"阀值配置..."});
            m.thresholdConfigWinWidget._moUid = moUid;
            m.thresholdConfigWinWidget._moType = moType;
            m.thresholdConfigWinWidget.reload();
        },
		getRemoteParams: function(){ return {uid: ps.currentDevId, cType:"Process"};},
		__init__: function(){
			var self = this;
			$(self._panel_id + " .op_bar a[name=del]").bind("click", function(){
				self.delDevComponents();
			});
			$(self._panel_id).delegate("a[name=configThreshold]", "click", function(){
                var moUid = $(this).attr("moUid");
                var moType = $(this).attr("moType");
                self.openThresholdConfigWin(moUid, moType);
            });
		}
	});
	
	
	m.fileSystemsGridWidget = nb.BaseWidgets.extend("BaseListWidget", DelDevComponentsWidget,{
		_panel_id:"#panel_fileSystems",
		cType:"FileSystem",
		remoteMethod:"getDevComponents",
		remoteView:nb.rpc.deviceViews,
		openThresholdConfigWin:function(moUid, moType){
            nb.uiTools.showEditDialogWin(null, "#thresholdConfigWin", {width:1000, height:400, title:"阀值配置..."});
            m.thresholdConfigWinWidget._moUid = moUid;
            m.thresholdConfigWinWidget._moType = moType;
            m.thresholdConfigWinWidget.reload();
        },
		getRemoteParams: function(){ return {uid: ps.currentDevId, cType:"FileSystem"};},
		__init__: function(){
			var self = this;
			$(self._panel_id + " .op_bar a[name=del]").bind("click", function(){
				self.delDevComponents();
			});
			
			$(self._panel_id).delegate("a[name=configThreshold]", "click", function(){
                var moUid = $(this).attr("moUid");
                var moType = $(this).attr("moType");
                self.openThresholdConfigWin(moUid, moType);
            });
		}
	});	
	
	m.ipServicesGridWidget = nb.BaseWidgets.extend("BaseListWidget", DelDevComponentsWidget, {
		_panel_id:"#panel_ipServices",
		cType:"IpService",
		remoteMethod:"getDevComponents",
		remoteView:nb.rpc.deviceViews,
		getRemoteParams: function(){ return {uid: ps.currentDevId, cType:"IpService"};},
		__init__: function(){
			var self = this;
			$(self._panel_id + " .op_bar a[name=del]").bind("click", function(){
				self.delDevComponents();
			});
		}
	});	
	
	

	
	
	//---------------------------------------------------------------------------------------------------
	
	
	m.baseInfoWidget = {
		_panel_id: "#dev_panel_001",
		_data:null,
		_render: function(){
			var self = this;
			var template = self.getTemplate();
            $(self._panel_id + " .box:first").html(template(self._data));
		},
		
		getTemplate: function(){
	    	var template = kendo.template($(this._panel_id + " script[name=template]").html());
	    	return template;
	    },

	    save:function(){
	        var self = this;
	        var params = {};
	        $(self._panel_id + " div.box").find("input,textarea").each(function(){ params[$(this).attr("name")] = $(this).val(); });
	        nb.rpc.deviceViews.c("saveDevBaseInfo",params)
            .success(function(msg){ nb.AlertTip.auto(msg); self.reload();});
	    },
	    
	    reload: function(){
	    	var self = this;
	    	nb.rpc.deviceViews.c("getDeviceBaseInfo",{"uid": ps.currentDevId}).
	    	success(function(dev){ self._data = dev; self._render() });
	    },
	   __init__: function(){
            var self = this;
            $(self._panel_id + " .op_bar a[name=save]").bind("click", function(){self.save()});
        }
	};
	
	var  _selectHcType=function( panel_id, hcType){
            var box = $(panel_id + " .box:first");
            if(hcType == "port"){
                 box.find("li.hcPorts").show();
            }else{
                box.find("li.hcPorts").hide();
            }
      };
	m.snmpConfigWidget = {
		_panel_id: "#dev_panel_002",
		_data:null,
		_render: function(){
			var self = this;
			$(self._panel_id + " .box:first").show();
			
			self._data.snmpVers=["v2c", "v3", "v1"];
			//修改boolean值的bind方式
			self._data.booleans = [{text:"是", val:"true"}, {text:"否", val:"false"}];
			
			
			self._data.netSnmpMonitorIgnore = nb.xutils.val2booleanStr(self._data.netSnmpMonitorIgnore);
			 
			self.viewModel = kendo.observable(self._data);
			kendo.bind($(self._panel_id + " .box:first"), self.viewModel);
		},
		save:function(){
		    var self = this;
		    if(!self.viewModel) return;
            var config = self.viewModel.toJSON();
            
            nb.xutils.delattrs(config, "booleans", "snmpVers");
            config.netSnmpMonitorIgnore = nb.xutils.val2boolean(config.netSnmpMonitorIgnore);
            
            nb.rpc.deviceViews.c("saveDevSnmpConfig",{"uid": ps.currentDevId, config:config})
            .success(function(msg){ nb.AlertTip.auto(msg); self.reload();});
		},
		reload:function(){
			var self = this;
			nb.rpc.deviceViews.c("getDevSnmpConfig",{"uid": ps.currentDevId}).success(function(conf){
				self._data = conf;
				self._render();
			});
		},
		__init__: function(){
		    var self = this;
		    $(self._panel_id + " .op_bar a[name=save]").bind("click", function(){self.save()});
		    $(self._panel_id + " .box:first select[name=netSnmpVer]").bind("change", function(){
		        //console.info(self._data);
		        //console.info($(this).val());
                if ($(this).val() == "v3"){
                $.each(snmpV3Attrs, function(i, snmpV3Attr){
                    $(self._panel_id + " .box:first").find("input[name=" + snmpV3Attr +"]").prop("disabled",false);
                });
                }else{
                $.each(snmpV3Attrs, function(i, snmpV3Attr){
                    $(self._panel_id + " .box:first").find("input[name=" + snmpV3Attr +"]").prop("disabled", true);
                });
                }    
            });
		}
	};
	
	m.commConfigWidget = {
		_panel_id: "#dev_panel_003",
		_data:null,
		
		_selectHcType :function(hcType){
		    var self = this;
            var widget = $( self._panel_id);
            if(hcType == "port"){
                 widget.find("li.hcPorts").show();
            }else{
                widget.find("li.hcPorts").hide();
            }
        },
    
		_render: function(){
			var self = this;
			$(self._panel_id + " .box:first").show();
			self._data.hcTypes = [{text:"PING",val:"ping"}, {text:"端口",val:"port"}];
			
			self.viewModel = kendo.observable(self._data);
			self.viewModel.changehcType = function(e){
                var widget = $(self._panel_id).data("nbWidget");
                self._selectHcType(widget.viewModel.hcType);
            };
			kendo.bind($(self._panel_id + " .box:first"), self.viewModel);
			self._selectHcType(self.viewModel.hcType);
		},
		
		save: function(){
		    var self = this;
		    if(!self.viewModel) return;
		    var config = self.viewModel.toJSON();
		    nb.xutils.delattrs(config, "hcTypes");
		    if(config.hcType == "ping" && config.hcPorts == ""){
		        config.hcPorts = "80";
		    } 
            if(!testInputPortString(config.hcPorts)){
                alert("端口格式不对！多个端口，请用,号分开,最多只能填写3个端口！"); 
                return;
            }
            nb.rpc.deviceViews.c("saveDevCommConfig",{"uid": ps.currentDevId, config:config})
            .success(function(msg){ nb.AlertTip.auto(msg); });
		},
		
		reload:function(){
			var self = this;
			nb.rpc.deviceViews.c("getDevCommConfig",{"uid": ps.currentDevId}).success(function(conf){
				self._data = conf;
				self._render();
			});
		},
		
        __init__: function(){
            var self = this;
            $(self._panel_id).data("nbWidget", this);
            $(self._panel_id + " .op_bar a[name=save]").bind("click", function(){self.save()});
            
            if(window.devClsUname == "windows"){
                $(self._panel_id + " li.for_linux").hide();
            }
        }		
	};
	
    m.thresholdConfigWidget= nb.BaseWidgets.extend("thresholdConfigWidget",{
        _panel_id: "#dev_panel_005",
        _getMoUid: function(){return ps.currentDevId},
        _moType:"Device"
    });
    
    
    

    
    
    m.templateConfigWidget = nb.BaseWidgets.extend("BaseListWidget", {
		_panel_id:"#templateConfigWidget",
		remoteMethod:"getMoTemplates",
		remoteView:nb.rpc.thresholdViews,
		getRemoteParams: function(){ return {moUid: ps.currentDevId, moType:"Device"};},
		bindTpl:function(tplUid){
			var self = this;
			self.remoteView.c("bindTpl", {moUid:ps.currentDevId, moType:"Device", tplUid:tplUid}).success(function(msg){
				nb.AlertTip.auto(msg);
				self.reload();
			});
		},
		
		unbindTpl:function(tplUid){
			var self = this;
			self.remoteView.c("unbindTpl", {moUid:ps.currentDevId, moType:"Device", tplUid:tplUid}).success(function(msg){
				nb.AlertTip.auto(msg);
				self.reload();
			});
		},
		
        __init__: function(){
            var self = this;
            $(self._panel_id + " .op_bar a[name=add_ext]").bind("click", function(){
            	nb.uiTools.showEditDialogWin(null, "#extendTemplatesListWidget", {title:"bind extend Templates", width:500, height:200});
            	m.extendTemplatesListWidget.reload();
            })
            
            $(self._panel_id).delegate("a[name=unbind]", "click", function(){
            	var tplUid = $(this).attr("tpluid");
            	self.unbindTpl(tplUid);
            })
            
            $(m.extendTemplatesListWidget._panel_id).delegate("a[name=bind]", "click", function(){
            	var tplUid = $(this).attr("tpluid");
            	self.bindTpl(tplUid);
            })
            
        }
	});
	
	//扩展模板选择列表
    m.extendTemplatesListWidget = nb.BaseWidgets.extend("BaseListWidget", {
		_panel_id:"#extendTemplatesListWidget",
		remoteMethod:"getExtendTemplates",
		remoteView:nb.rpc.thresholdViews,
		getRemoteParams: function(){ return {};},
        __init__: function(){
            var self = this;
        }
	});
    
    
    //弹出窗-阀值配置
    m.thresholdConfigWinWidget= nb.BaseWidgets.extend("thresholdConfigWidget",{
        _panel_id: "#thresholdConfigWin",
        _getMoUid: function(){return null},
        _moType:null
    });
    
    

	


    
    

	//---------------------------------------------------------------------------------------------------
	
	$(document).ready(function(){
	
		$("#tabstrip").kendoTabStrip();
		$("#tabstrip2").kendoTabStrip();
		
		
		
		m.interfacesGridWidget.__init__();
		m.ipServicesGridWidget.__init__();
		m.processesGridWidget.__init__();
		m.fileSystemsGridWidget.__init__();
		
		m.baseInfoWidget.__init__();
		m.snmpConfigWidget.__init__();
		m.commConfigWidget.__init__();
		m.thresholdConfigWidget.__init__();
		m.templateConfigWidget.__init__();
		m.extendTemplatesListWidget.__init__();
		
		//---------------------------------------------------------------------------//
		m.interfacesGridWidget.reload();
		m.processesGridWidget.reload();
		m.fileSystemsGridWidget.reload();
		m.ipServicesGridWidget.reload();

		
		m.baseInfoWidget.reload();
		m.snmpConfigWidget.reload();
		m.commConfigWidget.reload();
		m.thresholdConfigWidget.reload();
		m.templateConfigWidget.reload();
		//---------------------------------------------------------------------------//
		
	});
	
	
	$(document).ready(function(){
	    m.thresholdConfigWinWidget.__init__();
	    
	    $("#tree_op_bar div.box.DeviceClass a[name=add]").bind("click", function(){
	        $("#addDevicePage").show();
	    });
	    
	    $("#tree_op_bar div.box.Device a[name=del]").bind("click", function(){
	        nb.uiTools.confirm("你确定要删除此设备吗？<br/>注意：删除后，与此设备相关的性能数据将无法恢复!", function(){
                m.deviceDelWidget.delDevice();
	        });
        });
	    
        $(document).bind("keydown", function(evt){
            if(evt.keyCode == 116){ //116->F5
                m.pageReload();
                return false;
            }    
        });	    
	    
	});

})(jQuery);