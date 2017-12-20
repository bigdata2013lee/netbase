(function($) {
    var m = window.collector_index= new nb.xutils.Observer();
       
    var _ds = null;
    var getDs = m.getDs = function() {
        if(_ds) return _ds;
        var ds = new kendo.data.DataSource({
            type : "json", pageSize : 50,
            transport : {
                read : nb.rpc.userApi.rc("getCollector")
            }
    
        });
        _ds = ds;
        return _ds;
    };

    m.createGrid = function() {
        
    var onChange=function(arg){
        //pass
        };
 
        var _columns = [
            { field : "", title : "选择",  width:30, template: '<input type="checkbox" class="formID"  uid="#=_id#" />'},
            { field : "_id", title : "UID", width: 220 },
            { field : "title", title : "名称", width : 100}, 
            { field : "host", title : "IP地址"},
            { field : "mac", title : "MAC地址", width : 100 },
            { field : "bootpoPort", title : "远程开关机端口", width : 100 },
            { field : "tcpServerPort", title : "TCP服务端口", width : 100 },
            { field : "", title : "操作",  width : 50, template: '<button name="toConfig" uid=#=_id#>配置</button>'}
        ];

        $("#data-grid").kendoGrid({
            dataSource : getDs(),
            change:onChange,
            height : 400,
            pageable:true,
            sortable : true,
            columns : _columns
        });

        return $("#data-grid").data("kendoGrid");
    };
    
    
    m.addCollectorWidget = {
        _panel_id: "#addCollectorWin",
        
        validate:function(params){
            var self = this;
            var em = $(self._panel_id + " div.validateErrorMsg");
            var rules = {title: "required", mac:"mac", tcpServerPort: "port",bootpoPort: "port"};
            var validator = new nb.xutils.Validator(em, rules);
            return validator.validate(params);
        },
      
        save: function(){
            var self = this;
            var params = {};
            var title = $.trim($(self._panel_id + " input[name=title]").val());
            var mac = $.trim($(self._panel_id + " input[name=mac]").val());
            var bootpoPort = $.trim($(self._panel_id + " input[name=bootpoPort]").val());
            var tcpServerPort = $.trim($(self._panel_id + " input[name=tcpServerPort]").val());
            params = {title: title, mac: mac, bootpoPort: bootpoPort, tcpServerPort: tcpServerPort};
            if(!self.validate(params)){
                return;
            }

            nb.rpc.userApi.c("addCollector", params)
            .success(function(msg){
                nb.AlertTip.auto(msg);
                nb.uiTools.closeEditDialogWin("#addCollectorWin");
                getDs().read();
            });
        },
        
        __init__: function(){
            var self = this;
            $(self._panel_id + " div.win_opbar button.ok:first").bind("click", function(){
                self.save();
            });
        }
        
        
        
        
    };
    m.editCollectorWidget = {
         _panel_id: "#editCollectorWin",
         viewModel : null,
         uid: null,
         save: function(){
             var self = this;
             var params = {};
             var title = self.viewModel.title;
             var mac = self.viewModel.mac;
             var bootpoPort = self.viewModel.bootpoPort;
             var tcpServerPort = self.viewModel.tcpServerPort;
             params = {title: title, mac: mac, bootpoPort: bootpoPort, tcpServerPort: tcpServerPort, uid:self.uid};
             if(!self.validate(params)){
                return;
             }
             nb.rpc.userApi.c("editCollector", params)
             .success(function(msg){
                nb.AlertTip.auto(msg);
                nb.uiTools.closeEditDialogWin("#editCollectorWin");
                getDs().read();
             });
         },
         
         validate:function(params){
            var self = this;
            var em = $(self._panel_id + " div.validateErrorMsg");
            var rules = {title: "required", mac:"mac", tcpServerPort: "port",bootpoPort: "port"};
            var validator = new nb.xutils.Validator(em, rules);
            return validator.validate(params);
        },
         
         openEditWin: function(){
             var self = this;
             $("#editCollectorWin").find("div.validateErrorMsg").html("");
             $("#editCollectorWin").find("div.validateErrorMsg").hide();
             nb.uiTools.showEditDialogWin(self.viewModel, "#editCollectorWin", {width:500, height:400, title: "配置收集器"});
         },
         
         __init__: function(){
             var self = this;
             $("#data-grid").delegate("button[name=toConfig]", "click", function(){
                 var dataUid = $(this).parent().parent().attr("data-uid");
                 self.uid = $(this).attr("uid");
                 if(!dataUid || dataUid == "") return;
                 var data = getDs().getByUid(dataUid);
                 var note = data.toJSON();
                 self.viewModel = kendo.observable(note);
                self.openEditWin();
             });
             
             
             $(self._panel_id + " div.win_opbar button.ok:first").bind("click", function(){
                 self.save();
                 
             });
             
         }
    };
       
    var delCollectorMethod = function(){
        var uids = [];
        $("#collectorWidget  input.formID:checked").each(function(){
            uids.push($(this).attr("uid"));
        });
        
        if (uids.length==0){
            confirm("请选择要删除的列！");
            return;
        }
        if(!confirm("确定删除？如果删除这个收集器，与之相联的设备都会删除？， 这是一个很严重的操作！")){
            return;
        }
        nb.rpc.userApi.c("delCollector", {uids: uids})
        .success(function(msg){
            nb.AlertTip.info(msg);
            getDs().read();
        });
    };
        
    
    
        
    $(document).ready(function() {
         m.createGrid();
         
         
         $("#collectorWidget .opForm button[name=addCollector]").bind("click", function(){
         	$("#addCollectorWin").find("li input").each(function(){
         		if ($(this).attr("name") == "bootpoPort"){
         			$(this).val("12305");
         		}else if($(this).attr("name") == "tcpServerPort"){
         			$(this).val("12368");
         		}else{
         			$(this).val("");
         		}
 		
         	});
            nb.uiTools.showEditDialogWin(null, "#addCollectorWin", {width:500, height:400, title: "添加收集器"});
         });
         
         $("#collectorWidget .opForm button[name=delCollector]").bind("click", function(){
             delCollectorMethod();
         });
         m.addCollectorWidget.__init__();
         m.editCollectorWidget.__init__();
       
         
        /*
        $("#collectorWidget input.check-all").click(function(){
            if(this.checked){
                $("#collectorWidget input.formID ").each(function(){
                    $(this).prop("checked", true );
                });
                
            }else{
                $("#collectorWidget input.formID ").each(function(){
                    $(this).prop("checked", false );  
                });
            }
        });
        */
        
        //--------------------------------------------------------------------------------------------
    });

})(jQuery);
