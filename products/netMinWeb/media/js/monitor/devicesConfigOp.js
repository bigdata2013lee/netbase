(function($){
	           
	var m = window.devicesConfigOp = new nb.xutils.Observer();
	
	m.selectedDevUid = window.moUid;
	
	var _getKeysMap = function(key){
        var keysMap = {
            interfaces:deviceConfig.interfacesGridWidget, processes:deviceConfig.processesGridWidget, 
            fileSystems:deviceConfig.fileSystemsGridWidget, ipServices:deviceConfig.ipServicesGridWidget
        };
        if(key){
            return keysMap[key];
        }
	    return keysMap;
	}

	 //更新组件后，刷新相应组件列表
    m.on("updateDevComponts", function(compontKey){
        _getKeysMap()[compontKey].reload();
    });
	
	var updateDeviceComponents = function(widget, componentsParamName){
			var components = [];
			var remoteMethods = {interfaces: "updateDeviceIpInterfaces", processes:"updateDeviceProcesses", fileSystems:"updateDeviceFileSystems"}
			$(widget._panel_id + " input[name=data-uids]:checked").each(function(){
				var inter = widget.ds().getByUid($(this).val());
				components.push(inter.toJSON());
			});
			if(components.length == 0)return;
            var _remote = function(){
    			nb.rpc.monitorViews.c(remoteMethods[componentsParamName],function(){
    				var params = {devUid: m.selectedDevUid};
    				params[componentsParamName] = components;
    				return params;
    			}).
    			success(function(msg){
    				nb.AlertTip.auto(msg);
    				nb.uiTools.closeEditDialogWin(widget._panel_id);
    				m.fireEvent("updateDevComponts", componentsParamName);
    			});
            };			
			_remote();

	};
	
	var ListDevComponentsWidget = {
		__ds:null,
		ds: function(){
			var self = this;
			if(self.__ds) return self.__ds;
			var ds = new kendo.data.DataSource({
				transport : {
					read : nb.rpc.monitorViews.rc(self.remoteMethod, function(){
						return {"devUid": m.selectedDevUid}
					})
				},
				
				change: function() {
				    nb.uiTools.commLoading.cancel(self._panel_id);
					var template = self.getTemplate();
					$(self._panel_id + " tbody:first").html(kendo.render(template, this.view()));
					$(self._panel_id + " tbody:first>tr:odd").each(function(){ $(this).addClass("odd"); });
					if(self.afterChange){self.afterChange();}
				}
			});
			
			self.__ds = ds;
			return ds;
		},
	    getTemplate: function(){
	    	var template = kendo.template($(this._panel_id + " script[name=template]").html());
	    	return template;
	    },
	    reload: function(){
	        var self = this;
	        //$(self._panel_id + " tbody:first").html('<tr><td colspan="10" style="text-align: center">正在加载.....</td></tr');
	        nb.uiTools.commLoading.insertTo(self._panel_id);
	    	this.ds().read();
	    },
	    /**
	     *显示完后，标记已添加的组件 
	     */
        _afterChangeFixExist:function(){
            var self = this;
            var trs = $(self._panel_id + " tbody:first tr");
            var existEscapeUnames = [];
            $.each(_getKeysMap(self._ckeyName).ds().data(), function(i, d){
                existEscapeUnames.push(escape(d.uname));
            });
            
            trs.each(function(){
                if($.inArray($(this).attr("uname"), existEscapeUnames) >=0){
                    $(this).addClass("exist");
                }
            });
        }	    
	};
	

	
	m.listIpInterfacesWiget =  nb.BaseWidgets.extend("ListDevComponentsWidget", {
		_panel_id:"#addIpInterfaceWin",
		_ckeyName:"interfaces",
		_remoteView:nb.rpc.monitorViews,
		remoteMethod:"listDeviceIpInterfaces",
		getRemoteParams:function(){return {"devUid": m.selectedDevUid}},
	    updateDeviceIpInterfaces: function(){
			updateDeviceComponents(this, "interfaces");
	    },
	    afterChange:function(){
	        var self = this;
            self._afterChangeFixExist();
	    }
	    
		
	});
	
	
	m.listProcessesWiget =  nb.BaseWidgets.extend("ListDevComponentsWidget", {
		_panel_id:"#addProcessWin",
		_ckeyName:"processes",
		_remoteView:nb.rpc.monitorViews,
		remoteMethod:"listDeviceProcesses",
		getRemoteParams:function(){return {"devUid": m.selectedDevUid}},
	    updateDeviceProcesses: function(){
	    	updateDeviceComponents(this, "processes")
	    },
        afterChange:function(){
            var self = this;
            self._afterChangeFixExist();
        }
		
	});
	
	
	
	m.listFileSystemsWiget = nb.BaseWidgets.extend("ListDevComponentsWidget",{
		_panel_id:"#addFileSystemWin",
		_ckeyName:"fileSystems",
		_remoteView:nb.rpc.monitorViews,
		remoteMethod:"listDeviceFileSystems",
		getRemoteParams:function(){return {"devUid": m.selectedDevUid}},
	    updateDeviceFileSystems: function(){
	    	updateDeviceComponents(this, "fileSystems");
		},
        afterChange:function(){
            var self = this;
            self._afterChangeFixExist();
        }
		
	});
	

    
	m.listIpServicesWiget = nb.BaseWidgets.extend("ListDevComponentsWidget",{
		_panel_id:"#addIpServiceWin",
		_ckeyName:"ipServices",
		_remoteView:nb.rpc.monitorViews,
		getRemoteParams:function(){return {"devUid": m.selectedDevUid}},
	    updateDeviceIpServices: function(){
	    	var self = this;
	    	var getParams = function(){
				var params = {devUid: m.selectedDevUid};
				params.ipServices = [];
				var model = m.ipServiceModel;
				model.set('uname', model.protocol + "_" + model.port);
				model.set("port", model.port * 1);
				var jsonObj = model.toJSON();
				delete jsonObj.protocols;
				params.ipServices.push(jsonObj);
				
				return params;
	    	};
	    	var _remote = function(){
    			nb.rpc.monitorViews.c("updateDeviceIpServices",getParams()).
    			success(function(msg){
    				nb.AlertTip.auto(msg);
    				nb.uiTools.closeEditDialogWin(self._panel_id);
    				m.fireEvent("updateDevComponts", "ipServices");
    			});
	    	};
	    	_remote();
		},
		reload: function(){}
		
	});
	
	
	m.opBar = {
		
		__initUi__: function(){
			
			$("#panel_interfaces .op_bar a[name=addInterfaces]").bind("click", function(){
				if(!m.selectedDevUid) return;
				m.listIpInterfacesWiget.reload();
				nb.uiTools.showEditDialogWin(null, "#addIpInterfaceWin", {width:600, height:250});
			});
			
			$("#panel_processes .op_bar a[name=addProcesses]").bind("click", function(){
				if(!m.selectedDevUid) return;
				m.listProcessesWiget.reload();
				nb.uiTools.showEditDialogWin(null, "#addProcessWin",{width:600, height:350});
			});
			
			$("#panel_fileSystems .op_bar a[name=addFileSystems]").bind("click", function(){
				if(!m.selectedDevUid) return;
				m.listFileSystemsWiget.reload();
				nb.uiTools.showEditDialogWin(null, "#addFileSystemWin",{width:600, height:250});
			});
			
			$("#panel_ipServices .op_bar a[name=addIpServices]").bind("click", function(){
				if(!m.selectedDevUid) return;
				m.ipServiceModel = kendo.observable({port:0, protocol:'tcp', uname:"tcp_0"});
				nb.uiTools.showEditDialogWin(m.ipServiceModel, "#addIpServiceWin",{width:500, height:140});
			});
			
			
            
            
			
		}
		
	};
	
//--------------------------------------------------------------------------------
	$(document).ready(function(){
		
		$("#addIpInterfaceWin button.ok:first").bind("click", function(){
			nb.xutils.delayTask("updateDeviceIpInterfaces", function(){m.listIpInterfacesWiget.updateDeviceIpInterfaces();});
		});
		
		$("#addProcessWin button.ok:first").bind("click", function(){
		    nb.xutils.delayTask("updateDeviceProcesses", function(){m.listProcessesWiget.updateDeviceProcesses();});
		});
		
		$("#addFileSystemWin button.ok:first").bind("click", function(){
			nb.xutils.delayTask("updateDeviceFileSystems", function(){m.listFileSystemsWiget.updateDeviceFileSystems();});
		});
		
		$("#addIpServiceWin button.ok:first").bind("click", function(){
			nb.xutils.delayTask("updateDeviceIpServices", function(){m.listIpServicesWiget.updateDeviceIpServices();});
		});
		
		
		m.opBar.__initUi__();
	});
	
	
	
})(jQuery);
