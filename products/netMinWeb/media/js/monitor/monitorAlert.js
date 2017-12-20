(function($){
    var m = NB.nameSpace("monitorAlert");
    var monitorIndex = NB.nameSpace("monitorIndex");
    
    /**--------------------------------------------------------------*/

    m._trans = {
        _serveritys:{ 5 : 'critical', 4 : 'error', 3 : 'warning', 2 : 'info', 1 : 'debug', 0 : 'clear' },
        tranSeverity : function(sev) {
            
            return this._serveritys[sev];
        },

        tranSeveritys : function(sevs) {
            var ret = [];
            var self = this;
            $.each(sevs, function(index, sev) {
                ret.push(self._serveritys[sev]);
            });
            return ret.join(",");
        },

        tranSendInfo : function(sendType, sendTo) {
            return sendType + "->" + sendTo;
        }
    }; 

    /**--------------------------------------------------------------*/
   
   var showRuleEditWin = function(e){
       console.info(e);
       var dataUid = $(e.target || e.curentTarget).closest('tr').attr('data-uid');
       var grid =   $("#alert_rules_grid").data('kendoGrid');
       var data = grid.dataSource.getByUid(dataUid).toJSON();
       
       data.save = function(){
           //todo...
           alert('save me');
           var self = this;
           var _data = self.toJSON()
           $.each(_data.severitys, function(i, v){
               _data.severitys[i] = v * 1;
           });
           console.info(_data);
       }
       $.each(data.severitys, function(i, v){
           data.severitys[i] = v + '';
       });
       data = kendo.observable(data);
       
       nb.uiTools.showEditDialogWin(data,"#rule_edit_win",{width:500, height:260});
       
   };
   
    var renderAulerRuleGrid = function(){
        var dataSource = new kendo.data.DataSource({
            transport : {
                
                read : {
                    dataType:'json',
                    url: "/media/js/data/alert_rules.json"
                    }
            },
            pageSize: 10,
            schema : {
                
            }
        }); 
        
        
        
        $("#alert_rules_grid").kendoGrid({
            dataSource: dataSource,
            sortable: true,
            pageable: true,
            height:200,
            columns: [
                 {title:"标题", field: "title"},
                 {title:"描述", field: "description"},
                 {title:"级别", field:'severitys', width:150, template:'#=NB.monitorAlert._trans.tranSeveritys(severitys)#'},
                 {title:"消息键", field: "messageKey"},
                 {title:"连续告警时间",field:"continueAlarm"},
                 {title:"发送", width:150,template:'#=NB.monitorAlert._trans.tranSendInfo(sendType,sendTo)#'},
                 {title:"是否启用", field: "isStart", width: 60, template:'<div class="mo_state_#=isStart?\'up\':\'down\'#"></div>'},
                 {command: [ {text:'编辑',click:function(e){showRuleEditWin(e);}}],title:'操作', width:80}
            ]
        });  
        
        m._test_grid = $("#alert_rules_grid").data("kendoGrid");         
        
    };
    var renderAlertGrid = function(){
        var dataSource = new kendo.data.DataSource({
            transport : {
                
                read : {
                    dataType:'json',
                    url: "/media/js/data/alerts.json"
                    }
            },
            pageSize: 30,
            schema : {
                
            }
        }); 
        
        
        
        $("#alertGrid").kendoGrid({
            dataSource: dataSource,
            sortable: true,
            pageable: {
                refresh: true,
                pageSizes: [30,50, 100]
            },
            height:400,
            columns: [
                 {title:"级别", field:'severity', width:50,template:'<div class="evt-severitys #=NB.monitorAlert._trans.tranSeverity(severity)#"></div>' },
                 {title:"消息", field: "message"},
                 {title:"时间", field:"alertTime", width:150}
            ]
        });        
    };
    
    
    monitorIndex.TabPageLoador.on('Website_alert_ready', function() {
        renderAlertGrid();
        renderAulerRuleGrid();
    });
    
    monitorIndex.TabPageLoador.on('Device_alert_ready', function() {
        renderAlertGrid();
        renderAulerRuleGrid();
    });
    
})(jQuery);
