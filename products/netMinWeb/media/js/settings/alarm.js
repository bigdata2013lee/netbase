(function($){
    
    var m = window.alarmIndex = new nb.xutils.Observer();

    m.on("selectAlarmRule", function(rule){
        m.editAlarmRuesWidget.display(true);
        if(rule.alarmModel == "Email"){
            rule["alarmEmail"] = rule.alarmReceive.toString();
            rule["alarmSMS"] = userContactPhone;
        }else if(rule.alarmModel == "SMS"){
            rule["alarmEmail"] =userEmail;
            rule["alarmSMS"] = rule.alarmReceive.toString();
        }else{
        	rule["alarmEmail"] = userEmail;
            rule["alarmSMS"] = userContactPhone;
        }
        m.editAlarmRuesWidget._data = rule;
        m.editAlarmRuesWidget.reload();
    });
    
    m.on("alarmRulesChange", function(){
        m.allAlarmRulesWidget.reload();
        m.allAlarmRulesWidget.display(true);
        m.editAlarmRuesWidget.display(false);
        m.createAlarmRuesWidget.display(false);
    });
    
    m.allAlarmRulesWidget = {
        _panel_id:"#allAlarmRulesWidget",
        __ds:null,
        ds: function(){
            var self = this;
            if(self.__ds) return self.__ds;
            var ds = new kendo.data.DataSource({
                transport : {
                    read : nb.rpc.userApi.rc("getAllAlarmRules", {})
                },
                
                change: function() {
                    
                }
            });
            self.__ds = ds;
            return ds;
        },
        getTemplate: function(){
            
        },
        
        
        __createGrid: function(){
            var onChange=function(arg){
               var dataUid = this.select().attr("data-uid");
               if(!dataUid || dataUid == "") return;
               
               var data = this.dataSource.getByUid(dataUid);
               var _data = data.toJSON();
               data = kendo.observable(data.toJSON());
               m.fireEvent("selectAlarmRule", _data);
            };
            var self = this;
            var _columns = [
                {field : "title", title : "标题", width : 180}, 
                {field : "alarmModel", title : "告警方式", width: 100},
                {field : "description", title : "描述"},
                {field : "enable", title : "启用", width:80, template:"#= nb.Render.zh(enable)#"}
            ];
                
    
            $(self._panel_id + " .box:first").kendoGrid({
                dataSource : self.ds(),
                autoBind: false, height : 260,
                sortable : true,
                //pageable:true,
                selectable: true,
                change: onChange,
                columns: _columns 
            });
        },
        reload:function(){
            this.ds().read();
        },
        display: function(fg){
            var self = this;
            if(fg){ $(self._panel_id).show(); return;}
            $(self._panel_id).hide();
        },
        __init__: function(){
            var self = this;
            self.__createGrid();
        }
    };
    
    /**
     *创建、编辑告警规则 
     */
    editAlarmRuesBaseWidget = {
        _sources:{
            booleans:[{text:"是", val:"true"}, {text:"否", val:"false"}],
            firstTypes:[{text:"主机", val:"device"}, {text:"站点", val:"website"}],
            alarmTypes:[{text:"邮件", val:"Email"}, {text:"短信", val:"SMS"}, {text:"微信", val:"MMS"}],
            changeFirstType:function(e){
                var panel = $(e.target).closest("div.panel");
                var widget = panel.data("nbWidget");
                widget._selectFirstType(this.conditionData.firstType);
                
            },
            
            changeAlarmType:function(e){
               var panel = $(e.target).closest("div.panel");
               var widget = panel.data("nbWidget");
               widget._selectFirstAlarmType(this.alarmModel);
            }
            
        },
        _data:{
            title:"", description:"", enable:true,alarmModel:"Email",alarmReceive:userEmail,
            alarmEmail: userEmail,
            alarmSMS: userContactPhone,
            conditionData:{
                firstType:"device",  deviceIps:"", 
                keyWord:"", last:0, 
                severity:['3','4','5'],   
                device_componentTypes:["Device", "IpInterface", "Process", "IpService", "FileSystem"], 
                website_componentTypes:["Website"]
            }
        },
        _selectFirstType: function(firstType){
            var self = this;
            var box = $(self._panel_id + " div.box");
            box.find(".severity_span.swich").hide();
            box.find(".severity_span." + firstType).show();
            box.find("li.swich").hide();
            box.find("li.swich." + firstType).show();
        },
        
        _selectFirstAlarmType: function(alarmModel){
            var self = this;
            var box = $(self._panel_id + " div.box");
            box.find("li.alarmTypes").hide();
            box.find("li.alarmTypes." + alarmModel).show();
        },
        _render:function(){
            var self = this;
            self._data.enable = nb.xutils.val2booleanStr(self._data.enable);
            self.viewModel = kendo.observable($.extend({}, self._data, self._sources));
            kendo.bind($(self._panel_id + " .box:first"), self.viewModel);
            self._selectFirstAlarmType(self.viewModel.alarmModel);
            self._selectFirstType(self.viewModel.conditionData.firstType);
        },
        save: function(){
            //save method in base.
        },
        _validate:function(params){
            var self = this;
            var errorEl = $(self._panel_id + " div.validateErrorMsg");
            var rules = {
                severity: function(severitys){
                    if(severitys.length >0) return true;
                    return false;
                },
                firstType: function(firstType){
                    if(params.conditionData[firstType+"_componentTypes"].length > 0) return true;
                    return false;
                },
                   
            };
            var rules2 = {title:"required"};
            
            var messages = {"severity":"至少选择一个告警级别", "firstType": "至少选择一个子类型", "title": "规则名为必填项"};
            var validator = new nb.xutils.Validator(errorEl, rules, messages);
            var validator2 = new nb.xutils.Validator(errorEl, rules2, messages);
            
            var vrs1 = validator.validate(params.conditionData);
            if(vrs1 == false) return false;
            return validator2.validate(params);
        },      
        reload:function(){
            var self = this;
            self._render();
        },
        display: function(fg){
            var self = this;
            if(fg){ $(self._panel_id).show(); return;}
            $(self._panel_id).hide();
        },
        __init__:function(){
            var self = this;
            $(self._panel_id).data("nbWidget", this);
            self.reload();
            
            $(self._panel_id + " div.op_bar a[name=save]").bind("click", function(){
                self.save();
            });
            
            $(self._panel_id + " div.op_bar a[name=del]").bind("click", function(){
                self.del();
            });

        }
           
    };
    
    
    m.createAlarmRuesWidget = $.extend({}, editAlarmRuesBaseWidget, {
        _panel_id: "#createAlarmRuesWidget",
        save: function(){
            var self = this;
            var params = self.viewModel.toJSON();
            params.enable = nb.xutils.val2boolean(params.enable);
            if(params.alarmModel == "Email"){
                params.alarmReceive = params.alarmEmail;
            }else if(params.alarmModel == "SMS"){
                params.alarmReceive = params.alarmSMS;
            }else{
            	params.alarmReceive = "MMS";
            }
            nb.xutils.delattrs(params, "firstTypes","booleans", "alarmEmail", "alarmSMS", "alarmTypes");
            params.conditionData.deviceIps = params.conditionData.deviceIps.replace(/\s+/gi, "");
            if(!self._validate(params)) return;
            nb.rpc.userApi.c("addAlarmRule", {ruleMedata:params}).
            success(function(msg){
                nb.AlertTip.auto(msg);
                m.fireEvent("alarmRulesChange");
            })
        }
    });
    
    m.editAlarmRuesWidget = $.extend({}, editAlarmRuesBaseWidget, {
        _panel_id: "#editAlarmRuesWidget",
        save: function(){
            var self = this;
            var params = self.viewModel.toJSON();
            params.enable = nb.xutils.val2boolean(params.enable);
            if(params.alarmModel == "Email"){
                params.alarmReceive = params.alarmEmail;
            }else{
                params.alarmReceive = params.alarmSMS;
            }
            nb.xutils.delattrs(params, "firstTypes","booleans", "ownCompany", "alarmEmail", "alarmSMS", "alarmTypes");   
            params.conditionData.deviceIps = params.conditionData.deviceIps.replace(/\s+/gi, "");
            if(!self._validate(params)) return;
            nb.rpc.userApi.c("editAlarmRule", {ruleMedata:params}).
            success(function(msg){
                nb.AlertTip.auto(msg);
                m.fireEvent("alarmRulesChange");
            })
        },
        
        del: function(){
            var self = this;
            var params = self.viewModel.toJSON();
            nb.rpc.userApi.c("delAlarmRule", {ruleId:params._id}).
            success(function(msg){
                nb.AlertTip.auto(msg);
                m.fireEvent("alarmRulesChange");
            })
        }
    });
    
    $(document).ready(function(){
        
        
        $("#user_left_menus li a").bind("click", function(){
            var actionName = $(this).attr("name");
            $(".panel.swich").hide();
            $(".panel.swich[actionName=" + actionName + "]").show();
        });
        
        
        m.allAlarmRulesWidget.__init__();
        m.createAlarmRuesWidget.__init__();
        m.editAlarmRuesWidget.__init__();
        
        m.allAlarmRulesWidget.reload();
    });
})(jQuery);
