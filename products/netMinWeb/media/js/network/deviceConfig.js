(function($){
    
    
    var m = window.networkManager = new nb.xutils.Observer();
    var ps = {currentNetworkId:moUid};
    
    var  pageReload=function(){
    	window.location.reload();
    };
    
    

    
    
    //网络设备编辑与保存组件
    m.editNetworkWidget = {
        
        _panel_id: "#editNetworkWidget",
        validate:function(baseParams, snmpConfigParams, commConfigParams){
            var self = this;
            var em = $(self._panel_id + " div.validateErrorMsg");
            var exp = /^([1-9]+[0-9]*(\,)?)+$/;
            if(!exp.test(commConfigParams.hcPorts)){
                alert("端口格式不对！多个端口，请用,号分开！"); 
                return false;
            }
            var rules = {manageIp:"ip"};
            var validator = new nb.xutils.Validator(em, rules);
            return validator.validate(baseParams);
        },
        
        _selectHcType: function(hcType){
            var self = this;
            var widgetEl = $("#network_panel_003");
            if(hcType == "port"){
                 widgetEl.find("li.hcPorts").show();
            }else{
                widgetEl.find("li.hcPorts").hide();
            }
            
        },
        
        _getBaseParams: function(){
            var self = this;
            var mainBox = $(self._panel_id + " fieldset.baseInfoConfig");
            var params = {networkId: ps.currentNetworkId};
            mainBox.find("input").each(function(){
                params[$(this).attr("name")] = $(this).val();
            });
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
        
        openThresholdConfigWin:function(moUid, moType){
            nb.uiTools.showEditDialogWin(null, "#thresholdConfigWin", {width:1000, height:400, title:"阀值配置..."});
            m.thresholdConfigWinWidget._moUid = moUid;
            m.thresholdConfigWinWidget._moType = moType;
            m.thresholdConfigWinWidget.reload();
        },
        
        
        save:function(){
            var self = this;
            var baseParams = self._getBaseParams();
            var snmpConfigParams = self._getSnmpConfigParams();
            var commConfigParams = self._getCommConfigParams();
            
            var fg = self.validate(baseParams, snmpConfigParams, commConfigParams);
            if(!fg)return;
            var params = {baseConfig: baseParams, snmpConfig:snmpConfigParams, commConfig:commConfigParams};
            nb.rpc.networkViews.c("saveNetworkDevice", params).success(function(msg){
                nb.AlertTip.storeCookie(msg);
	            pageReload();
            }); 
        },
        
        _render: function(){
            
            var self = this;
            kendo.bind($(self._panel_id + " fieldset.baseInfoConfig"), self.baseInfoViewModel);
            kendo.bind($(self._panel_id + " fieldset.snmpConfig"), self.snmpViewModel);
            kendo.bind($(self._panel_id + " fieldset.commConfig"), self.commViewModel);  
            self._selectHcType(self.commViewModel.hcType);
        },
        
        /**
         * 绑定多个ViewModel， 
         * baseInfoViewModel
         * snmpViewModel
         * commViewModel
         */
        _bindViewModels : function(network){
            var self = this;
            var baseInfo = {
                manageIp:network.manageIp,
                title: network.title, description: network.description, productId: network.productId, collector: network.collector
             };
             
            var _sources = {
                "booleans":[{text:"是", val:"true"}, {text:"否", val:"false"}], //附加显示的
                "snmpVers":["v2c", "v3", "v1"] //附加显示的
            };
            var snmpConifg = $.extend({},network.snmpConfig,_sources);
            snmpConifg.netSnmpMonitorIgnore = nb.xutils.val2booleanStr(snmpConifg.netSnmpMonitorIgnore)

            self.baseInfoViewModel = kendo.observable(baseInfo);    
            self.snmpViewModel = kendo.observable(snmpConifg);
            var _source = {
                hcTypes:[{text:"PING",val:"ping"}, {text:"端口",val:"port"}],
                changehcType: function(e){
                    var widget = $(self._panel_id).data("nbWidget");
                    widget._selectHcType(widget.commViewModel.hcType);
                }
            }
            self.commViewModel = kendo.observable($.extend({}, network.commConfig,  _source));       
        },
        
        reload:function(){
            var self = this;
            nb.rpc.networkViews.c("getNetworkById", {uid: ps.currentNetworkId}).success(function(network){
                self._bindViewModels(network);
                self._render();
            });    
        
        },
        __init__: function(){
            var self  = this;
            $(self._panel_id).data("nbWidget", this);
            $(self._panel_id + " div.op_bar a[name=save]").bind("click", function(){self.save()});
            $(self._panel_id).delegate("a[name=configThreshold]", "click", function(){
                var moUid = ps.currentNetworkId;
                var moType = "Network";
                self.openThresholdConfigWin(moUid, moType);
            });
            
            $("#addIpInterfaceWin button.ok:first").bind("click", function(){
            nb.xutils.delayTask("updateNetworkIpInterfaces", function(){m.listIpInterfacesWiget.updateNetworkIpInterfaces();});
            });
            self.reload();
        }
               
    };
    
    var _getUids = function(widget){
        var cUids = [];
        $(widget._panel_id + " table:first input[name=ids]:checked").each(function(){
            cUids.push($(this).val());
        });
        return cUids;
    };
    var DelNetworkComponentsWidget = {
            delNetworkComponents: function(){
            var self = this;
            var cUids = _getUids(self);
            if(!cUids || cUids.length == 0){return;}
            if(! window.confirm("你确定要删除选择的组件？？")){return;}
            self.remoteView.c("delNetworkComponents", {uid: ps.currentNetworkId, cType:self.cType, cUids:cUids}).
            success(function(msg){ nb.AlertTip.auto(msg); self.reload(); });
        }
    };    
    
    
      m.on("updateNetworkComponts", function(compontKey){
        var keysMap = {
            interfaces:m.interfacesGridWidget
        };
        
        keysMap[compontKey].reload();
    });
    
    
    var updateNetworkComponents = function(widget, componentsParamName){
            var components = [];
            var remoteMethods = {interfaces: "updateNetworkIpInterfaces", processes:"updateDeviceProcesses", fileSystems:"updateDeviceFileSystems"}
            $(widget._panel_id + " input[name=data-uids]:checked").each(function(){
                var inter = widget.ds().getByUid($(this).val());
                components.push(inter.toJSON());
            });
            
            nb.rpc.networkViews.c(remoteMethods[componentsParamName],function(){
                var params = {netUid: ps.currentNetworkId};
                params[componentsParamName] = components;
                return params;
            }).
            success(function(msg){
                nb.AlertTip.auto(msg);
                nb.uiTools.closeEditDialogWin(widget._panel_id);
                m.fireEvent("updateNetworkComponts", componentsParamName);
            });

    };
    
    
    m.listIpInterfacesWiget =  nb.BaseWidgets.extend("ListDevComponentsWidget", {
        _panel_id:"#addIpInterfaceWin",
        _remoteView:nb.rpc.networkViews,
        remoteMethod:"listNetworkIpInterfaces",
        getRemoteParams:function(){return {"netUid": ps.currentNetworkId}},
        updateNetworkIpInterfaces: function(){
            updateNetworkComponents(this, "interfaces");
        }
        
    });
    
    m.interfacesGridWidget = nb.BaseWidgets.extend("BaseListWidget",DelNetworkComponentsWidget, {
        _panel_id:"#panel_interfaces",
        cType:"IpInterface",
        remoteMethod:"getNetworkComponents",
        remoteView:nb.rpc.networkViews,
        getRemoteParams: function(){ return {uid: ps.currentNetworkId, cType:"IpInterface"};},
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
            nb.rpc.networkViews.c("setCustomSpeed", params)
            .success(function(msg){
                nb.AlertTip.auto(msg);
                self.reload();
            });

        },
        __init__: function(){
            var self = this;
            $(self._panel_id + " .op_bar a[name=del]").bind("click", function(){
                self.delNetworkComponents();
            });
            
            $(self._panel_id + " .op_bar a[name=setCustomSpeed]").bind("click", function(){
                var cUids = _getUids(self);
                if(!cUids || cUids.length == 0){ nb.AlertTip.warn("没有选择接口"); return;}
                if(cUids.length>1){nb.AlertTip.warn("请选择一个接口，请勿多选"); return;}
                var dataUid = $(self._panel_id + " table:first input[name=ids]:checked:first").closest("tr").attr("data-uid");
                if(nb.xutils.isEmpty(dataUid)) return;
                
                var rViewModel = self.ds().getByUid(dataUid);
                var viewModel = kendo.observable({cUid:cUids[0], CustomSpeed:0});
                nb.uiTools.showEditDialogWin(kendo.observable(rViewModel.toJSON()), 
                "#setCustomSpeedWin", {width:600, height:250, title:"设定自定义带宽..."});
            });
            
            $(self._panel_id).delegate("a[name=configThreshold]", "click", function(){
                var moUid = $(this).attr("moUid");
                var moType = $(this).attr("moType");
                self.openThresholdConfigWin(moUid, moType);
            });
            
            
            $("#setCustomSpeedWin .win_opbar button.ok").bind("click", function(){
                self.setCustomSpeed();
            });
            
            $(self._panel_id + " .op_bar a[name=addInterfaces]").bind("click", function(){
                var self = this;
                if(!ps.currentNetworkId) return;
                m.listIpInterfacesWiget.reload();
                nb.uiTools.showEditDialogWin(null, "#addIpInterfaceWin", {width:600, height:250, title:"请选择添加的接口"});
            });
        }
    });
    
    


    
    
    //弹出窗-阀值配置
    m.thresholdConfigWinWidget= nb.BaseWidgets.extend("thresholdConfigWidget",{
        _panel_id: "#thresholdConfigWin",
        _getMoUid: function(){return null},
        _moType:null
    });
    
    $(document).ready(function(){
        m.thresholdConfigWinWidget.__init__();
        m.editNetworkWidget.__init__();
        m.interfacesGridWidget.__init__();
        m.interfacesGridWidget.reload();
        
    });
    
    $(document).ready(function(){
        $("#tree_op_bar div.box.NetworkClass a[name=add]").bind("click", function(){
            $("#addNetworkWidget").show();
        });        
    });   
})(jQuery);
