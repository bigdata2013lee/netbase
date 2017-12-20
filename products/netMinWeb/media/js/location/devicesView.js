(function($){
	//前台用户中心的监控专家   自定义分组页面主JS文件。【2014.12.24  jenny】	
	var ns = nb.nameSpace("devicesView");
	var m = new nb.xutils.Observer();
	
	var _ds=null;
	var _queryConditions = {};

	//定义页面列表组件的列参数
	var _columns = [
		{title:"<input id='mo_uid_checkbox'  type='checkbox' />",width:50, template:'<input name="mo_uid" type="checkbox" value="#=_id#" mo_type="#=moType#"/>'},
		{field: "moType", sortable: true, title: "类型", width:50, template:'#=nb.Render.zh(moType)#'},
		{field: "title", sortable: true, title: "名称"},
		{field: "manageIp", width:120, sortable: true, title: "ip地址"},
		{field: "cpu", sortable: true, width:120, title: "Cpu", template:'#=nb.Render.toNum2(cpu.CPU, "%")#'},
		{field: "mem", sortable: true, width:120, title: "Mem", template:'#=nb.Render.toNum2(mem.Mem, "%")#'},
		{field: "status", sortable: true, width:120, title: "状态", template:'<span class="status-icon-small #=status#"></span>'}
	];
	
	ns.getSelectMos = function(){
		var rs = []
		$("#data-grid input[name=mo_uid]:checked").each(function(){
			rs.push({uid:$(this).val(), moType:$(this).attr("mo_type")})
		});
		return rs;
	};
	
    var parameterMap = function() {
    	return{orgUid:window.orgUid};
    }	

	//获取列表数据
    var getDs = ns.getDs = function(methodName){
        if(_ds) return _ds;
        var ds = new kendo.data.DataSource({
            type : "json",
            pageSize : 200,
            transport : {
                read : nb.rpc.locationViews.rc("listMos", parameterMap),
            }
        });
        _ds = ds;
        return _ds;
    }
    
    //过滤查询条件中，为空条件，返回不为空的查询调价列表
    var filter = function(){
    	var filters = [];
    	var fields = nb.uiTools.mapFields("#grid_tool_bar>div.query");
    	$.each(fields, function(key, val){
    		
    	});
    	$("#grid_tool_bar>div.query>input").each(function(){
    		var field = $(this).attr("name");
    		var value = $.trim($(this).val());
    		if(value == "") return;
    		filters.push({field:field, operator: "contains", value:value});
    	})
    	getDs().filter(filters);
    }
    
    //定义页面列表组件
	var createGrid=function(){
		$("#data-grid").kendoGrid({
            dataSource : getDs(),
            toolbar: kendo.template($("#grid_tool_bar_template").html()),
            height : 600,
            scrollable:true,
            sortable : true,
            //resizable: true,
            pageable:true,
            //columnMenu: true,
            columns: _columns 
        });
	}
	
	$(document).ready(function(){
		createGrid();

		$("#panel_data_grid").delegate("#grid_tool_bar>div.query>input","change", function(evt){
				filter();
		});
		
		$("#panel_data_grid").delegate("#mo_uid_checkbox","click", function(evt){
				var checked = $(this).prop("checked");
				$("#panel_data_grid :checkbox[name=mo_uid]").prop("checked",checked);
		});
	});
	
	
})(jQuery)
