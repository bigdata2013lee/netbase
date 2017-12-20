(function($){
	
	//该JS文件未被使用，可以删除 【2014.12.24  jenny】	
    var m = window.customersIssues = new nb.xutils.Observer();
    
    m.Render = {
        serviceNoteOp : function(snUid){
            if(! snUid) return '<a href="javascript:" name="createServiceNote">生成服务单</a>';
            return "";
        }
    }
    //--------------------------------------------------------------------//
    
    m.on("selectUserNode", function(user){
        var skills = [];
        $.each(user._childrenOptions.data.items, function(i, item){ skills.push(item._id);  });
        
        m.customerIssuesGridWidget._queryParams = {customerUid:user._id, skills:skills};
        m.customerIssuesGridWidget.reload(); 
    });
    
    m.on("selectSkillNode", function(skill){
        m.customerIssuesGridWidget._queryParams = {customerUid:skill.user_id, skills:[skill._id]};
        m.customerIssuesGridWidget.reload();
    });
    
    
    //--------------------------------------------------------------------//
    
    m.customerIssuesTreeWidget = {
        _panel_id:"#customer_issues_tree",
        __ds:null,
        ds: function(){
            var self = this;
            if(self.__ds) return self.__ds;
            ds = new kendo.data.HierarchicalDataSource({
                data: self._data
            });
            
            self.__ds = ds;
            return ds;
        },
        _render: function(){
            var self = this;
            var  dataSource = self.ds();
            $(self._panel_id).kendoTreeView({
                dataSource: dataSource,
                dataTextField: ["title"],
                select: function(evt){
                    var dataUid = $(evt.node).attr("data-uid");
                    var data = this.dataSource.getByUid(dataUid);
                    
                    if(data.type == 'user'){
                        m.fireEvent("selectUserNode", data);
                    }
                    else if(data.type == 'skill'){
                        m.fireEvent("selectSkillNode", data);
                    }
                    
                }
            });
            
           self._selectRootItem();
            
            
            
            
            
        },
        
        _selectRootItem: function(){
            var self = this;
            var treeView =  $(self._panel_id).data("kendoTreeView");
            var firstItem = $(self._panel_id + " li.k-item:first");
            treeView.select(firstItem);
            var dataUid = $(firstItem).attr("data-uid");
            var data = treeView.dataSource.getByUid(dataUid);
            if(data && data.type == 'user'){ m.fireEvent("selectUserNode", data); }
        },
        
        
        getTemplate: function(){
            
        },
        reload: function(){
            var self = this;
            nb.rpc.engineerViews.c("getCustomerIssuesTreeDataSource").
            success(function(data){
                if(data.length>0) data[0].expanded = true;
                self._data = data;
                self._render();
            });

        }
    
    };
    
    m.customerIssuesGridWidget = {
        _panel_id: "#customerIssuesGridWidget",
        __ds:null,
        _queryParams: {},
        ds:function(){
            var self  = this;
            if(self.__ds) return self.__ds;
            
            self.__ds = new kendo.data.DataSource({
                type : "json", pageSize : 100,
                transport : { read : nb.rpc.engineerViews.rc("getCustomerIssues", function(){return self._queryParams})}
                
            });
            
            return self.__ds;
        },
        _render:function(){
            
        },
        reload: function(){
            var self = this;
            self.ds().read();
        },
        
        createServiceNote:function(event){
            var self = this;
            var eventInfo = event.toJSON();
            var serviceNote = {};
            serviceNote.eventSeverity = eventInfo.severity;
            serviceNote.title = eventInfo.message;
            serviceNote.summary = eventInfo.message;
            serviceNote.monitorObjName = eventInfo.componentType+"_"+eventInfo.title;
            serviceNote.eventId = eventInfo._id;
            serviceNote.noteType = eventInfo.technologicalType;
            serviceNote.eventLabel = eventInfo.label;
            
            
            nb.rpc.engineerViews.c("createServiceNote", {serviceNote: serviceNote, customerUid:self._queryParams.customerUid}).
            success(function(msg){
                alert(msg);
                self.ds().read();
            });
            
        },
        __createGrid: function(){
            var self = this;
            var _columns = [{
                    field : "severity", sortable : true, title : "级别",width : 60,
                    template : "<span class='severity-icon-small Critial x#=severity#'></span>"
                    
                },{
                    field : "label", title : "名称/设备IP", width : 120
                }, {
                    field : "title", title : "监控项目", width : 120
                }, {
                    field : "message", title : "事件信息"
                }, {
                    field : "firstTime", sortable : true, title : "开始时间",
                    template : "#=nb.xutils.getTimeStr(firstTime * 1000)#",
                    width : 120
                }, {
                    field : "endTime", sortable : true, title : "结束时间",
                    template : "#=nb.xutils.getTimeStr(endTime * 1000)#",
                    width : 120
                }, {
                    field : "count", sortable : true, title : "计数", width : 60
                }, {
                    field : "agent", title : "代理", width : 120
                },{
                    filed:"serviceNoteUid", title:"生成服务单",sortable : true, width:80, 
                    template:'#=customersIssues.Render.serviceNoteOp(serviceNoteUid)#'
                }];
                
    
            $(self._panel_id + " .data-grid").kendoGrid({
                dataSource : self.ds(),
                autoBind: false,
                height : 400,
                sortable : true,
                pageable:true,
                columns: _columns 
            });
        },
        __init__:function(){
            var self = this;
            self.__createGrid();
            
            $(self._panel_id).delegate("a[name=createServiceNote]", "click", function(){
                if(!window.confirm("你确定要将此事件创建服用单？？")) return;
                var dataUid = $(this).closest("tr").attr("data-uid");
                var event = self.ds().getByUid(dataUid);
                self.createServiceNote(event);
            });
        }
    }
    
    
    
    $(document).ready(function(){
        m.customerIssuesTreeWidget.reload();
        m.customerIssuesGridWidget.__init__();
    });
    
})(jQuery);
