(function($){
	//运维商用户中心的运维通用户求助 和我的分享 、前台用户中心的问题详情、分享详情页面的主JS文件 【2014.12.19  jenny】	
    var m = new nb.xutils.Observer();
    
    /**
	 * 提交问题或者分享的回复内容
	 * @method commentTopic
	 * @param {string} content 回复内容
	 * @param {string} topicId 提问或分享的ID
	 * @param {string} topicType 被回复的信息的类型：提问/分享
	 * @return {string} 判断参数是否符合条件，返回一个提示信息并关闭窗口，刷新页面
	 */
    var commentTopic = function(){
        var params = {};
        var content = $("#createComment_win textarea[name=content]").data("kendoEditor").value();
        var topicId = $("#createComment_win input[name=topicId]").val();
        var topicType = window.topicType;
            
        if(content.replace(/\s/ig,'').split("<p></p>").join("").length > 1000 || content.replace(/\s/ig,'').split("<p></p>").join("").length <=0){
        	nb.AlertTip.auto("请输入1000字符以内的内容");
        	return;
        }
        params.content = content;
        params.topicId = topicId;
        params.topicType = topicType;
        nb.rpc.topicViews.c("commentTopic",params)
        .success(function(msg){
            nb.AlertTip.storeCookie(msg);
            location.reload();
        });        
        nb.uiTools.closeEditDialogWin("#createComment_win");
        $("#createComment_win textarea[name=content]").val("");
    }
    
    /**
	 * 提交运维商用户中心的运维通用户求助详情页面被收藏客户ID
	 * @method addFavoriteCustomer
	 * @param {string} customerId 被收藏客户的ID
	 * @return {string} 判断参数是否成功，返回一个提示信息
	 */
    var addFavoriteCustomer = function(customerId){
        var params = {customerId:customerId};
        nb.rpc.operationView.c("addFavoriteCustomer",params)
        .success(function(msg){
            nb.AlertTip.auto(msg);
        });        
    }
    
    /**
	 * 提交用户给力操作的数据
	 * @method approve
	 * @param {obj} elA 被点击的控件对象
	 * @param {string} topicType 被的点赞的回复的信息的类型：提问/分享
	 * @return {string} 提交信息如果成功，返回该回复的点赞数并显示在被点击的空间对象上，失败返回一个提示信息
	 */
    var approve = function(elA,topicType){
        var commentId = $(elA).attr("comment_id");
        var params = {commentId:commentId,topicType:topicType};
        nb.rpc.topicViews.c("approveTopicComment",params)
        .success(function(num){
            if($.isNumeric(num)){
                $(elA).text(num + " 给力");
            }
            else{
                nb.AlertTip.auto(num);
            }
        });        
    }
    
    /**
	 * 前台用户在问题详情页面提交用户采纳操作的数据
	 * @method accept
	 * @param {obj} elA 被点击的控件对象
	 * @return {string} 返回信息成功与否的提示信息
	 */
    var accept = function(elA){
        var commentId = $(elA).attr("comment_id");
        var qid = $(elA).attr("qid");
        var params = {commentId:commentId,questionId:qid};
        nb.rpc.topicViews.c("setAcceptComment",params)
        .success(function(msg){
            nb.AlertTip.auto(msg);
        })  
    }
    
    /**
	 * 提交用户举报操作的数
	 * @method report
	 * @param {obj} elA 被点击的控件对象
	 * @param {string} topicType 被的点赞的回复的信息的类型：提问/分享
	 * @return {string} 返回信息成功与否的提示信息
	 */
    var report = function(elA,topicType){
        var commentId = $(elA).attr("comment_id");
        var params = {commentId:commentId,topicType:topicType};
        nb.rpc.topicViews.c("setReportComment",params)
        .success(function(msg){
            nb.AlertTip.auto(msg);
        })
    }
    
    /**
	 * 检查用户是否登录
	 * @method checkLogin
	 * @return {bool} 返回布尔值
	 */
    var checkLogin = function(){
        var visiter = $("a[action=openCommentWin]").attr("visiter_id");
        if(visiter != "None") {
            return false;
        }else{
            return true;
        }        
    }
   
    $(document).ready(function(){
    	//触发用户评论窗体的显示
    	//1、检查用户是否登录
    	//2、登录了显示编辑内容窗体，未登录显示登录窗体
        $("a[action=openCommentWin]").bind("click", function(){
            if (checkLogin()) {
                nb.uiTools.showEditDialogWin(null, "#login_dilog", {width:700, height:400,title:"登陆系统"});
            }else{
                nb.uiTools.showEditDialogWin(null, "#createComment_win", {width:833, height:400});
            }
        });
       
        //触发提交收藏用户信息的事件
        $("a[action=addFavoriteCustomer]").bind("click", function(){
            var customerId = $(this).attr("customer_id");
            addFavoriteCustomer(customerId);
        });
        
        //触发提交用户点赞事件
    	//1、检查用户是否登录
    	//2、登录了提交点赞信息，未登录显示登录窗体
        $("a[action=approve]").bind("click", function(){
            var topicType=window.topicType;

            if (checkLogin()) {
                nb.uiTools.showEditDialogWin(null, "#login_dilog", {width:700, height:400,title:"登陆系统"});
                return
            }
            approve(this,topicType);
        });
        
        //触发提交用户采纳事件
    	//1、检查用户是否登录
    	//2、登录了提交采纳信息，未登录显示登录窗体
         $("a[action=accept]").bind("click", function(){
             if (checkLogin()) {
                nb.uiTools.showEditDialogWin(null, "#login_dilog", {width:700, height:400,title:"登陆系统"});
                return
            }
           accept(this);
        });
        
        //触发提交用户举报事件
    	//1、检查用户是否登录
    	//2、登录了提交举报信息，未登录显示登录窗体
        $("a[action=report]").bind("click", function(){
           var topicType=window.topicType;
            if (checkLogin()) {
                nb.uiTools.showEditDialogWin(null, "#login_dilog", {width:800, height:400});
                return
            }
           report(this,topicType);
        });
        
        //触发用户提交回复内容事件
        $("#createComment_win .win_opbar button.ok").bind("click",function(){
            commentTopic();
        });
        
        //点击搜索按钮，移除列表DIV，显示查询结果div
        $("div.search_box #search_btn").bind("click", function(){
            $("#question_detail_panel").remove();
            $("#search_results_panel").show();
        });
		
		//初始化回复内容编辑器
        $("#createComment_win textarea[name=content]").kendoEditor({});
    });
    
})(jQuery);