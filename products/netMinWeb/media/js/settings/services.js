(function($){
    var m = window.services = new nb.xutils.Observer();
    
    
    m.on("gridRefresh", function(){
        $(m.servicesDetailWidget._panel_id).hide();
        $(serviceNote.serviceNoteDialogsWidget._panel_id).hide();
    });
    
    
    m.on("selectServiceNote", function(note){              
       serviceNote.serviceNoteDialogsWidget._snUid=note._id;
       serviceNote.serviceNoteDialogsWidget.reload();
       serviceNote.attachmentsWidget._snUid=note._id;
       serviceNote.attachmentsWidget.reload(); 
    });
    
    m.on("selectServiceNote", function(note){
        if(note.status==2){
            serviceNote.serviceNoteDialogsWidget.displayEditor(false);
            serviceNote.attachmentsWidget.displayUploadForm(false);
        }
        else{
            serviceNote.serviceNoteDialogsWidget.displayEditor(true);
            serviceNote.attachmentsWidget.displayUploadForm(true);
        }
    });
    
    var _ds=null;
    var _queryConditions={status:0};    
    var common = []
    
    var setQueryConditions=function(){
        _queryConditions = {};
        $("div.query_tool_bar").find("input[name=title], select[name=status]").each(function(){            
            _queryConditions[$(this).attr("name")] =$(this).val();
        });
        
        _queryConditions["status"] = _queryConditions["status"] != "" ? _queryConditions["status"] * 1 : undefined;
        _queryConditions["title"] = !nb.xutils.isEmpty(_queryConditions["title"]) ? "regex:" + nb.xutils.replaceXletters(_queryConditions["title"]) : undefined;
        
    };
    var getDs =  function(){
        if(_ds) return _ds;
        var ds = new kendo.data.DataSource({
            type : "json",
            serverPaging : true,
            serverSorting : true,
            pageSize : 200,
    
            transport : {
                read : nb.rpc.serviceNoteViews.rc("getServiceNotes"),
                parameterMap : function(data, type) {
                    var pageData = {}
                    pageData.limit = data.pageSize;
                    pageData.skip = data.skip;
                    pageData.sort = {
                        startTime : -1
                    };
    
                    if (data.sort && data.sort.length > 0) {
                        var field = data.sort[0].field;
                        pageData.sort[field] = data.sort[0].dir == "desc" ? -1 : 1;
                    }
    
                    var conditions = _queryConditions;
                    return {
                        params : $.toJSON({
                            userUid: userName,
                            pageData : pageData,
                            conditions : conditions
                        })
                    };
                }
            },
            schema : {
                data : "results",
                total : "total"
            }
    
        });
        _ds = ds;
        return _ds;
    };

    
    m.createGrid = function(){
        var onChange=function(arg){
           var dataUid = this.select().attr("data-uid");
           if(!dataUid || dataUid == "") return;
           
           var data = this.dataSource.getByUid(dataUid);
           var note = data.toJSON();
           
           data = kendo.observable(data.toJSON());
           m.servicesDetailWidget.viewModel = data;
           m.servicesDetailWidget.reload();
           
           m.fireEvent("selectServiceNote", data);
           
        };
        var _columns = [
        //        {field : "status", title : "状态", width : 60, template:"#=nb.Render.serviceNoteStatus(status)#"},
                {field : "eventLabel", sortable : true, title : "名称/设备IP", width : 150},
                {field : "monitorObjName", sortable : true, title : "监控项目", width : 150, template:"#=nb.Render.monitorObjName(monitorObjName)#"},
                {field : "title", sortable : true, title : "事件信息", width : 250, template:'<span title="#=title#">#=nb.Render.ellipsisStr(title, 20)#</span>'},
                {field : "engineer", sortable : true, title : "工程师", width : 100 }, 
        //        {field : "summary", title : "摘要"}, 
                {field : "startTime", sortable : true, title : "开始时间", width : 120, template : "#=nb.xutils.getTimeStr(startTime * 1000)#" }, 
                {field : "endTime", sortable : true, title : "结束时间", width : 120,  template : "#=nb.xutils.getTimeStr(endTime * 1000)#" },
                { command: ["关闭", "重开"], title: "&nbsp;", width: "80px" },
         ];
            

        $("#data-grid").kendoGrid({
            dataSource : getDs(),
            height : 300,
            selectable: true,
            toolbar: kendo.template($("#servicesWidget script[name=tool_bar]").html()),
            change: onChange,
            scrollable : { virtual : true },
            sortable : true,
            //columnMenu: true,
            columns: _columns 
        });
        
        
        return $("#data-grid").data("kendoGrid");
        
    };

    
 
    m.servicesDetailWidget={
        _panel_id:"#servicesDetailWidget",
        viewModel:null,
        _render: function(){
            var self = this;
            
            $(self._panel_id).show();
            self.viewModel.getStartTime = function(){
                return nb.xutils.getTimeStr(this.startTime * 1000);
            };
            self.viewModel.getEndTime = function(){
                return nb.xutils.getTimeStr(this.endTime * 1000);
            };
            self.viewModel.getStatus = function(){
                return nb.Render.serviceNoteStatus(this.status);
            };
            self.viewModel.getSeverity = function(){
                return nb.Render.severitys2zh(this.eventSeverity);
            };
            
            self.viewModel.getMonitorObjName = function(){
                var monitorObjName = this.monitorObjName;
                return nb.Render.monitorObjName(monitorObjName);
            };
            
            //状态为结束时，打开评价信息
            $(self._panel_id + " .serviceNoteAssess:first").hide();
            if(self.viewModel.status == 2){
                $(self._panel_id + " .serviceNoteAssess:first").show();
            }
            
            kendo.bind($(self._panel_id + " .box:first"), self.viewModel);
            
            if(self.viewModel.status == 1){
                self.setDisabled(false);
            }
            else{
                self.setDisabled(true);
            }
        },
        
        setDisabled:function(fg){
            var self = this;
            if(fg){
                $(self._panel_id + " .box:first").find("textarea, input").attr("disabled", true);
                $(self._panel_id + " .op_bar a").hide();
            }
            else{
                $(self._panel_id + " .box:first").find("textarea, input").attr("disabled", false);
                $(self._panel_id + " .op_bar a").show();
            }
        },
        audit:function(){//评分、评价
            var self = this;
            var note = self.viewModel.toJSON();
            var auditWin = $("#auditWin");
            var score = auditWin.find("input[name=score]:checked").val() * 1;
            if(! score){score = 6}
            
            var assess = auditWin.find("textarea[name=assess]").val();
            var params = {snUid: note._id, score: score, assess: assess};
            nb.xutils.trimObj(params);
            nb.rpc.serviceNoteViews.c("audit", params)
            .success(function(msg){
                nb.AlertTip.auto(msg);
                getDs().read();
                m.fireEvent("gridRefresh");
                nb.uiTools.closeEditDialogWin("#auditWin");
            });
            
        },
        
        unaudit:function(){
            var self = this;
            var note = self.viewModel.toJSON();
            var _remote = function(){
                nb.rpc.serviceNoteViews.c("unaudit", {snUid: note._id}).
                success(function(msg){
                    nb.AlertTip.auto(msg);
                    getDs().read();
                    m.fireEvent("gridRefresh");
                });
            };
            nb.uiTools.confirm("你确定回退此服务！，建议回退后在对话内容中说明具体原因！", _remote);
            
        },
        reload:function(){
            var self = this;
            self._render();
        },
        __init__:function(){
            
            var self = this;
            $(self._panel_id).hide();
            $(self._panel_id + " .op_bar a[name=unaudit]").bind("click", function(){self.unaudit()});
            $(self._panel_id + " .op_bar a[name=audit]").bind("click", function(){
                nb.uiTools.showEditDialogWin(null, "#auditWin", {title:"服务审核、评分、评价", width:560, height:200});
            });
            
            $("#auditWin button.ok").bind("click", function(){
                self.audit();
            });
        }
    }, 
    
    
    $(document).ready(function(){
       m.createGrid();
       m.servicesDetailWidget.__init__();

    });
    
    
    $(document).ready(function(){
        $("#servicesWidget .query_tool_bar").delegate("input, select", "change", function(){
            setQueryConditions();
            getDs().read();
            m.fireEvent("gridRefresh");
        });
    });
    
    
})(jQuery);
