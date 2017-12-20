(function($) {
	//前台用户中心的事件页面的主JS文件 【2014.12.24  jenny】	

    window.eventConsoleFor ? "" : window.eventConsoleFor = "events";  // or "historyEvents", 控制台是用于“事件”还是 “历史事件”功能
    var m = window.eventsConsole = new nb.xutils.Observer();
    var _queryConditions = {};
    var _ds = null;
    
    m.Render = {
        serviceNoteOp : function(snUid, severity, technologicalType, historical){
            if(!severity>=3) return "";
            // if(!snUid && !historical) return '<a href="javascript:" name="createServiceNote" title="生成服务单..."><span class="icon x16 createServiceNote"></span></a>';
            if($("#engineer").html()!="None") return '<a href="javascript:" name="createServiceNote" title="生成服务单..."><span class="icon x16 createServiceNote"></span></a>';
            return "";
        },
        
        label: function(label, deviceIp, title){
            return deviceIp || label || title;
        }
    }
    
    m.getEventStateStr =  function(evtState){
        var evtStates ={0: "未确认", 1:"确认",  2:"禁止"}
        return evtStates[evtState]
    };
    
    var extendAarry = function(a1, a2){
        for(var i=0; i < a2.length; i++){ a1.push(a2[i]); }
        return a1;
    }
    /**
     *初始化日期控件 
     */
    var initDateUi = function(){
        function startChange() {
            var startDate = start.value(), endDate = end.value();

            if (startDate) {
                startDate = new Date(startDate);
                startDate.setDate(startDate.getDate());
                end.min(startDate);
            } else if (endDate) {
                start.max(new Date(endDate));
            } else {
                endDate = new Date();
                start.max(endDate);
                end.min(endDate);
            }
        }

        function endChange() {
            var endDate = end.value(), startDate = start.value();

            if (endDate) {
                endDate = new Date(endDate);
                endDate.setDate(endDate.getDate());
                start.max(endDate);
            } else if (startDate) {
                end.min(new Date(startDate));
            } else {
                endDate = new Date();
                start.max(endDate);
                end.min(endDate);
            }
        }

        var start = $("#start").kendoDatePicker({ change : startChange  }).data("kendoDatePicker");
        var end = $("#end").kendoDatePicker({ change : endChange }).data("kendoDatePicker");
        var _v = 604800000; //7天毫秒数
        
        start.value(new Date(new Date().valueOf() - _v));
        end.value(new Date());
        start.min(new Date(new Date().valueOf() - _v * 4 * 12));
        start.max(end.value());
        end.min(start.value()); 
        end.max(new Date()); 
          
        if(window.eventConsoleFor == "events"){
            start.value(null);
            end.value(null);
        }
    };
    
    /**
     *构建查询事件的开始时间、结束时间两个条件
     * @method getDateQueryConditions
     */
    m.getDateQueryConditions = function(){
        var start = $("#start").data("kendoDatePicker");
        var end = $("#end").data("kendoDatePicker");
        
        var _fixTime = function(dateObj, H, M, S){
            var d = dateObj;
            d.setHours(H);
            d.setMinutes(M);
            d.setSeconds(S);
            d.setMilliseconds(0);
            return d;
        };
        var _conditions = {};
        if(start.value()){
            var d = start.value();
            _fixTime(d, 0, 0, 0);
            _conditions["endTime"] = {"$gte": d.valueOf() / 1000}
        }
        if(end.value()){
            var d = end.value();
            _fixTime(d, 23, 59, 59);
            _conditions["firstTime"] = {"$lte": d.valueOf() / 1000}
        }
        return _conditions;
    };
    
    /**
     *构建事件级别的查询条件 
     * @method getSeverityCondition
     */
    var getSeverityCondition = function(){
        var vals = [];
        $("#query_conditions_table input[name=severity]:checked").each(function(){
            vals.push($(this).val() * 1);
        });
        vals = vals.sort();
        var keys = vals.join("");
        var keysmap = {
            "12345": {severity:{"$gte": 1}}, "2345": {severity:{"$gte": 2}}, "345": {severity:{"$gte": 3}}, "45": {severity:{"$gte": 4}},
            "01234": {severity:{"$lte": 4}}, "0123": {severity:{"$lte": 3}},  "012": {severity:{"$lte": 2}}, "01": {severity:{"$lte": 1}},
            "0":{severity:0}, "1":{severity:1}, "2":{severity:2}, "3":{severity:3}, "4":{severity:4}, "5":{severity:5},
            "1234": {"$and": [{severity: {"$gte":1}}, {severity: {"$lte":4}}]},
            "123": {"$and": [{severity: {"$gte":1}}, {severity: {"$lte":3}}]},
            "234": {"$and": [{severity: {"$gte":2}}, {severity: {"$lte":4}}]},
            "34": {"$and": [{severity: {"$gte":3}}, {severity: {"$lte":4}}]} 
        }
        if(vals.length == 0 || vals.length == 6 ) return;  //不选与全选
        if(keysmap[keys]) return keysmap[keys]; //配置特定keys
        return {severity: {"$in":vals}}; //其它情况使用in查询
    }; 
   
    /**
     *获取事件查询的条件 
     * @method getQueryConditions
     */
    m.getQueryConditions = function() {
        
        var letters = {
                "\\\\" : /\\/,
                "\\." : /\./g,
                "\\+" : /\+/g,
                "\\*" : /\*/g,
                "\\?" : /\?/g,
                "\\-" : /\-/g
            };
        var conditions = {};
        var table = $("#query_conditions_table");

        //时间条件
        $.extend(conditions, m.getDateQueryConditions())

        var componentType_condition = table.find("select[name=componentType]").val();
        if (componentType_condition != "") {
            conditions["componentType"] = componentType_condition;
        }
        
        /** 设置正则条件 */
        var setRegexCondition = function(name){
            var condition = table.find("input[name="+name+"]").val();
            if (condition && $.trim(condition) != "") {
                $.each(letters, function(key, val) {
                    condition = condition.replace(val, key);
                })
                conditions[name] = "regex:" + condition;
            }
        };
        
        setRegexCondition("message");
        setRegexCondition("agent");
        setRegexCondition("title");

        var severity_condition = getSeverityCondition();
        if(severity_condition){ $.extend(conditions, severity_condition); }
        return conditions;
    };

    var __initUi__ = function() {

        _queryConditions = m.getQueryConditions();
        
        //定义查询事件
        var queryTask = function(){
            _queryConditions = m.getQueryConditions();
            getDs().read();
        }
        //定义事件刷新事件
        var refreshTask = function(){
            getDs().read();
        }
        
        //绑定并触发查询按钮事件
        $("#query_button").bind("click", function(event) {
            nb.xutils.delayTask("queryTask", queryTask, 1000);
        });
        
        // 绑定事件刷新事件
        $("#refresh").bind("click", function(event){
            nb.xutils.delayTask("refreshTask", refreshTask, 1000);
        });
        
        //绑定并触发事件查询事件
        $("#query_conditions_table").bind("keyup", function(evt){
            if(evt.keyCode != 13) return;
             nb.xutils.delayTask("queryTask", queryTask, 1000);
        });
        
        //绑定并触发查询条件输入框内容改变事件
        $("#query_conditions_table input").bind("change", function(){
            nb.xutils.delayTask("queryTask", queryTask, 1000);
        });
        
        //绑定并触发查询条件选择框内容改变事件
        $("#query_conditions_table select").bind("change", function(){
            nb.xutils.delayTask("queryTask", queryTask, 1000);
        });
    };


    var getDs = m.getDs = function(methodName){
        if(_ds) return _ds;
        var ds = new kendo.data.DataSource({
            type : "json",
            serverPaging : true,
            serverSorting : true,
            pageSize : 200,
    
            transport : {
                read : nb.rpc.eventViews.rc(methodName),
                parameterMap : function(data, type) {
                    var pageData = {}
                    pageData.limit = data.pageSize;
                    pageData.skip = data.skip;
                    pageData.sort = {
                        endTime : -1
                    };
    
                    if (data.sort && data.sort.length > 0) {
                        pageData.sort = {};
                        var field = data.sort[0].field;
                        pageData.sort[field] = data.sort[0].dir == "desc" ? -1 : 1;
                    }
    
                    var conditions = _queryConditions;
                    return {
                        params : $.toJSON({
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
    }
    
    m.createGrid = function(remoteMethodName, columns){
        var onChange = function(arg){
        };
        var _columns = [];
        if(eventConsoleFor == "historyEvents"){
            extendAarry(_columns, [{
                field : "eventState", title : "状态",
                template : '<span class="eventState-icon-small confirm#=eventState#" title="#=eventsConsole.getEventStateStr(eventState)#"></span>',
                width : 35
            }]);
        }
         extendAarry(_columns, 
             [{
                field : "severity", sortable : true, title : "级别", sortable : true,
                template : '<span class="severity-icon-small #=nb.Render.severitys(severity)#" title="#=nb.Render.severitys2zh(severity)#"></span>',
                width : 35
            }, {
                field : "label", title:"名称", width:100, template:'#=eventsConsole.Render.label(data.label, data.deviceIp, data.title)#'
            },{
                field : "componentType", title : "监控项目", width : 100, sortable : true, template:'#=nb.Render.zh(componentType)#'
            }, {
                field : "message", title : "事件信息", resize:true
            }, {
                field : "firstTime", sortable : true, title : "开始时间",
                template : "#=nb.xutils.getTimeStr(firstTime * 1000)#",
                width : 120
            }, {
                field : "endTime", sortable : true, title : "结束时间",
                template : "#=nb.xutils.getTimeStr(endTime * 1000)#",
                width : 120
            }, {
                field : "count", sortable : true, title : "次数", width : 60
            }, {
                field : "agent", title : "组件", width : 120
            }]
            
         );
         
         if(window.technologyServiceEnable ){
             extendAarry(_columns, [{
                field:"serviceNoteUid", title:"生成服务单",width:85, 
                template:"#=eventsConsole.Render.serviceNoteOp(data.serviceNoteUid, data.severity, data.technologicalType, data.historical)#"
            }]);
         }
         
        var offset = $("#data-grid").offset();
        var height  = $(document).height() - offset.top - 20;
        height < 400 ? height = 400: "";
        
        $("#data-grid").kendoGrid({
            dataSource : getDs(remoteMethodName),
            height : height,
            //scrollable : { virtual : true },
            scrollable:true,
            sortable : true,
            resizable: true,
            pageable:true,
            selectable:"multiple",
            change:onChange,
            //columnMenu: true,
            columns: columns || _columns 
        });
        
        //$("#pager").kendoPager({dataSource: getDs()});
        return $("#data-grid").data("kendoGrid");
    };

    $(document).ready(function() {

        initDateUi();
        __initUi__();
               
       //  每隔2分钟刷新一次 
        setInterval(function(){getDs().read()}, 60*1000*2);
    });

})(jQuery);
