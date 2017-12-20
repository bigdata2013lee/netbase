(function($){
	//回帖或者对话页面用到的显示头像及相关信息的控件 【2014.12.19  jenny】
	//当用户把鼠标放在用户头像上，会显示用户相关的一些信息
    var m = new nb.xutils.Observer();
    var showUserInfo=function(img, userId, userType){
        new $.Zebra_Tooltips($(img), {
            background_color:"#85C8EF",
            content:'<div class="tip_content_box" style="width:300px;height:120px;">loading...</div>',
            'max_width':    300,
            "onBeforeShow":function(v1, v2){
                $.get("/ucenter/showUser/" + userId +"/" + userType + "/", {}, function(html){
                    $(v2).find("div.tip_content_box:first").html(html);
                }, "html")
            },
            "onHide":function(v1, v2){
                //v2.remove();
            }
        });
    };
    
    $(document).ready(function(){
    	//绑定触发显示用户信息的事件
        $("body").delegate("img[name=user_icon]", "mouseover", function(){
            var userId = $(this).attr("user_id");
            var userType = $(this).attr("user_type");
            showUserInfo(this, userId, userType);
        })
    });
    
})(jQuery);