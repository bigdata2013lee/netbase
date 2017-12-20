(function($){
    $(document).ready(function(){
        $("#publisherUsernameSpan").hide();
        $("#publisherEmailSpan").hide();
        $("#submitContent").kendoEditor({});
        $("#submitOpinion").bind("click",function(){
            var publisherUsername=$("#publisherUsernameSpan").text();
            var publisherEmail=$("#publisherEmailSpan").text();
            var title=$("#submintTitle").val();
            if(title=="") {
                nb.AlertTip.auto("请输入标题");
                return;
            }
            var content=$("#submitContent").data("kendoEditor").value();
            if(content=="") {
                nb.AlertTip.auto("请输入反馈的内容");
                return;
            }
            var params={title:title,content:content,publisherUsername:publisherUsername,publisherEmail:publisherEmail};
            nb.rpc.topicViews.c("showOpinon",params)
            .success(function(msg){
                $("#submitContent").data("kendoEditor").value("");
                $("#submintTitle").val("");
                nb.AlertTip.auto(msg);
            })
        });
    });
})(jQuery);