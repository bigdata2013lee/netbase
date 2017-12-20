(function($) {

	var m = window.bootpoIndex = new nb.xutils.Observer();
	m.pageReload = function(){
	    m.bootpoViewWidget.reload();
	};
	m.on("datasourceChanged", function(ds){
	    bootpos = ds.data();
	});
    _validate=function(ipmiConfig, flag){
        var self = this;
        var em = $(self._panel_id + " div.validateErrorMsg");
        var messages = "";
        var rules = "";
        if(flag){
        	messages = {netIpmiIp:"ip地址格式不对", netIpmiUserName:"ipmi用户名是必需的", netIpmiPassword:"ipmi密码是必需的"};
        	rules = {netIpmiIp: "ip", netIpmiUserName:"required", netIpmiPassword:"required"};        	
        }else{
        	messages = {netIpmiIp:"ip地址格式不对", netIpmiUserName:"ipmi用户名是必需的"};
        	rules = {netIpmiIp: "ip", netIpmiUserName:"required"};         	
        }
        var validator = new nb.xutils.Validator(em, rules, messages);
        return validator.validate(ipmiConfig);
    };
        
	m.bootpoViewWidget ={
		
		_panel_id: "#panel_0001",
		__ds:null,
		ds: function(){
			var self = this;
			if(self.__ds) return self.__ds;
			var ds = new kendo.data.DataSource({
				transport : {
					read : nb.rpc.bootpoViews.rc("listBootpoObjs")
				},
				
				change: function() {
					var template = self.getTemplate();
					$(self._panel_id + " .box:first").html(kendo.render(template, this.view())); // populate the table
					$(self._panel_id + " .box:first").append($('<br clear="both"/>'));
					m.fireEvent("datasourceChanged", this);
				}
			});
			self.__ds = ds;
			return ds;
		},
		getTemplate: function(){
	    	var template = kendo.template($(this._panel_id + " script[name=template]").html());
	    	return template;
	    },
	    
        
         setBootpoPower:function(bootpoId, opName){
            var self = this;
            var loading = nb.uiTools.commLoading.insertTo("body");
            loading.css({"position":"fixed"});
            loading.find("span:first").css({"margin-top":"105px"});
            loading.find("span:first").html("正在发送远程命令，请稍后...");
            nb.rpc.bootpoViews.c("setBootpoPower", {bootpoId:bootpoId, opName:opName}).
            success(function(msg){
                loading.find("span:first").html("命令已发送...");
                setTimeout(function(){
                    loading.find("span:first").html("命令正在执行...");
                    setTimeout(function(){
                        loading.find("span:first").html("请等待5-10分钟时间才能见效果...");
                        nb.uiTools.commLoading.cancel("body");
                        nb.AlertTip.auto(msg);
                    }, 5000);
                    
                }, 5000);
                
            });
        },    


	    _bindButtons: function(){
	        var self = this;
	        var getBootpo = function(el){
	            var dataUid = $(el).closest("div.bootpo").attr("data-uid");
	            var bootpo = self.ds().getByUid(dataUid);
	            return bootpo;
	        }
	        
	       	$(self._panel_id + " .panelActions a[name=refresh_action]").bind("click", function(){self.reload()});
            
            //开机
            $(self._panel_id).delegate("div.bootpo a[name=powerUpOp]", "click", function(evt){
                var bootpo = getBootpo(this);
                var msg = "你确定要对此设备进行远程开机吗？";
                msg += "<br/>注意:打开或关闭设备，需要一点时间，请耐心等侍几分钟，切勿频繁执行开关机操作！";
                nb.uiTools.confirm(msg, function(){
                    self.setBootpoPower(bootpo._id, "powerUp");
                })   
            });
            
            //关机
            $(self._panel_id).delegate("div.bootpo a[name=softDownOp]", "click", function(evt){
                var bootpo = getBootpo(this);
                var msg = "你确定要对此设备进行远程关机(软关机)吗？";
                msg += "<br/>注意:打开或关闭设备，需要一点时间，请耐心等侍几分钟，切勿频繁执行开关机操作！";
                nb.uiTools.confirm(msg, function(){
                    self.setBootpoPower(bootpo._id, "softDown");
                })
                
            });
            
            //硬关机
            $(self._panel_id).delegate("div.bootpo a[name=powerDownOp]", "click", function(evt){
                var bootpo = getBootpo(this);
                var msg = "你确定要对此设备进行硬关机吗？";
                msg += "<br/>注意:打开或关闭设备，需要一点时间，请耐心等侍几分钟，切勿频繁执行开关机操作！";
                nb.uiTools.confirm(msg, function(){
                    self.setBootpoPower(bootpo._id, "powerDownOp");
                })
            });
            
            //硬重启
            $(self._panel_id).delegate("div.bootpo a[name=powerResetOp]", "click", function(evt){
                var bootpo = getBootpo(this);
                var msg = "你确定要对此设备进行硬重启吗？<br/> 注意:硬重启有可能会造成硬盘的raid丢失或者数据的丢失,所以谨慎使用";
                msg += "<br/>注意:打开或关闭设备，需要一点时间，请耐心等侍几分钟，切勿频繁执行开关机操作！";
                nb.uiTools.confirm(msg, function(){
                    self.setBootpoPower(bootpo._id, "powerResetOp");
                });
            });

            //编辑
            $(self._panel_id).delegate("div.bootpo a[name=editBootpo]", "click", function(evt){
                var bootpo = getBootpo(this);
                 var model = {"bootpoId": bootpo._id, title: bootpo.title, 
                 		startUpIPMI:bootpo.startUpIPMI,ipmiConfig:bootpo.ipmiConfig};
                m.editBootpoWidget.show(model);
            });
            
            //删除
            $(self._panel_id).delegate("div.bootpo a[name=delBootpo]", "click", function(evt){
                var bootpo = getBootpo(this);
                var msg = "确定删除此对象？";
                nb.uiTools.confirm(msg, function(){
                    nb.rpc.bootpoViews.c("delBootpo", {bootpoId:bootpo._id}).
                 	success(function(msg){
                 		nb.AlertTip.auto(msg);
                 		m.pageReload();
                 	});
                });
            });
            
	    },

		reload: function(){
			this.ds().read();
		},
		__initUi__: function(){
			var self = this;
			
            $(self._panel_id + " .op_bar a[name=create]").bind("click", function(){
                m.addBootpoWidget.show();
            });

			self._bindButtons();
            
            $("#ch_ok").bind("click", function(){
                if(!self._viewModel) return;
                var bootpo = self._viewModel.toJSON();
                self.doEdit(bootpo);    
            }); 
		}
	};

    
    m.addBootpoWidget = {
        _panel_id:"#addBootpoWidget",
        
        show:function(){
            var self = this;

            self.viewModel=kendo.observable({
                title:"",
                booleans:[{text:"是", val:"true"}, {text:"否", val:"false"}],
                startUpIPMI: "false",
                ipmiConfig:{
                	"netIpmiIp":"",
            		"netIpmiUserName": "root", 
            		"netIpmiPassword":""
                } 
            });
            nb.uiTools.showEditDialogWin(self.viewModel, self._panel_id, {title:"创建开关机对象", width:600, height:400});
        },
        save:function(){
            var self = this;
            var params = self.viewModel.toJSON();
	        nb.xutils.delattrs(params, "booleans");
            var fg =self._validate(params.ipmiConfig, true);
            if(! fg ) return;
            var _remote = function(){
                nb.rpc.bootpoViews.c("addBootpo", params).success(function(msg){
                   nb.AlertTip.auto(msg);
                   m.pageReload();
                });
            };
            
           nb.uiTools.closeEditDialogWin(self._panel_id);
           _remote();
        },
        _validate:_validate,
        __init__:function(){
            var self = this;
            $(self._panel_id + " .win_opbar button.ok").bind("click", function(){
                self.save();
            });
        }
    };
    
    
    m.editBootpoWidget = {
        _panel_id:"#editBootpoWidget",
        
        show:function(model){
            var self = this;
            var _model = $.extend({booleans:[{text:"是", val:"true"}, {text:"否", val:"false"}]},model)
            self.viewModel=kendo.observable(_model);
            nb.uiTools.showEditDialogWin(self.viewModel, self._panel_id, {title:"编辑开关机对象", width:600, height:400});
        },
        save:function(){
            var self = this;
            var params = self.viewModel.toJSON();
            console.info(params)
            nb.xutils.delattrs(params, "booleans");
            var fg =self._validate(params.ipmiConfig, false);
            if(! fg ) return;
            nb.rpc.bootpoViews.c("editBootpo", params).success(function(msg){
               nb.AlertTip.auto(msg);
               pageLoad();
           });
           nb.uiTools.closeEditDialogWin(self._panel_id);
        },
        _validate:_validate,
        __init__:function(){
            var self = this;
            $(self._panel_id + " .win_opbar button.ok").bind("click", function(){
                self.save();
            });
        }
    };
    
    $(document).ready(function() {

	   //开机视图初始化方法
	   m.bootpoViewWidget.__initUi__();
	   //刷新方法
	   m.bootpoViewWidget.reload()
	   //定时刷新，2分钟刷新一次
	   setInterval(function(){ m.pageReload() }, 1000 * 60 * 2);
		
       m.addBootpoWidget.__init__();
       m.editBootpoWidget.__init__();
       
       
    });

})(jQuery);
