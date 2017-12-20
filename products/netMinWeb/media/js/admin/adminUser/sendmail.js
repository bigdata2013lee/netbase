(function($){  
    var m = new nb.xutils.Observer();
    /**
     *发送邮件：
     */
    m.sendEmail=function(){
        var conditionType = $("#conditionTypeDiv :radio:checked").val();
        var emailContext=$("#email_editor").data("kendoEditor").value();
        var subject=$("#subject").val();
        
        if(conditionType=="filter"){
            /**
             * 根据选择的条件发送邮件
             */
            var filterConditions = m._getFilterConditions();
            var loginTime2 =filterConditions['loginTime2'];
            var loginTime1 =filterConditions['loginTime1'];
            var registTime2 =filterConditions['registTime2'];
            var registTime1 =filterConditions['registTime1'];
            var username =filterConditions['username'];
            nb.rpc.adminUserViews.c("sendMailToUsersForFilter",{
                emailContext:emailContext,subject:subject, 
                loginTime2:loginTime2, loginTime1:loginTime1,
                registTime2:registTime2,registTime1:registTime1,
                username:username}
             )
            .success(function(msg){
                nb.AlertTip.auto(msg);
            })
        }else{
            /**
             * 根据指定的邮箱发送邮件 
             */
            var emailArr=m._getSpecifiedConditions();
            if($.isEmptyObject(emailArr)){
                nb.AlertTip.auto("warn:没有输入收件人");
                return;
            }
            nb.rpc.adminUserViews.c("sendMailToUsersForSpecified", {emailContext:emailContext, subject:subject, emails:emailArr})
            .success(function(mgs){
                nb.AlertTip.auto(mgs);
            })
        }
        
    };
    
    /**
     *过滤查询条件 
     */
    m._getFilterConditions=function(){
        
        var  _getTime = function(name){
            var xTime = $("#" + name).data("kendoDatePicker").value();
            xTime=xTime?parseInt(xTime.valueOf()/1000): null;
            return xTime;
        }        
        return {
            loginTime1: _getTime("loginTime1"),
            loginTime2: _getTime("loginTime2"),
            registTime1: _getTime("registTime1"),
            registTime2: _getTime("registTime2"),
            username: $("#username").val()
        };
    };
    
    /**
     *过滤输入的邮箱 
     */
    m._getSpecifiedConditions=function(){
        var specified=$("#specified").val();
        
        specifiedArr = specified.split("\n");
        var emailArr=[];
        for (var i=0;i<specifiedArr.length;i++) {
            var email=specifiedArr[i];
            email = email.replace(/\s+/gi, "");
            if(email == '') continue;
            if(!nb.xutils.isVaildEmail(email)){
                nb.AlertTip.auto("warn:" + email+"不符合邮箱格式，请输入正确的邮箱");
                return[];
            }else{
                emailArr.push(email);
            }
        }     
        return emailArr;
    }
    
    /**
     *测试查询条件，获得查询结果包含的用户数目 
     */
    m.testFilter=function(){
        var filterConditions = m._getFilterConditions();
        var loginTime2 =filterConditions['loginTime2'];
        var loginTime1 =filterConditions['loginTime1'];
        var registTime2 =filterConditions['registTime2'];
        var registTime1 =filterConditions['registTime1'];
        var username =filterConditions['username'];
        nb.rpc.adminUserViews.c("testFilter",{
                loginTime1:loginTime1, loginTime2:loginTime2,
                registTime1:registTime1,registTime2:registTime2,
                username:username}
             )
       .success(function(msg){
          nb.AlertTip.auto(msg);
       })    
       
    };
    
    /**
     *把日期条件转换为日期类型 
     */
    var initDatePick=function(){
      
        $("#loginTime2").kendoDatePicker();
        $("#loginTime1").kendoDatePicker();
        $("#registTime2").kendoDatePicker();
        $("#registTime1").kendoDatePicker();  
    };
    
    /**
     *主函数 
     */ 
    $(document).ready(function() {
        $("#conditionTypeDiv :radio").bind("click", function(){
            var val = $(this).val();
            $("div.pos").hide();
            $("div.pos_" + val).show();
        });       
        $("#conditionTypeDiv :radio:first").click();
        $("div.pos_filter a[action=testFilter]").bind("click", function(){
            m.testFilter();
        });   
        initDatePick();
        $("#email_editor").kendoEditor({
             tools: [
                "bold",
                "italic",
                "underline",
                "strikethrough",
                "justifyLeft",
                "justifyCenter",
                "justifyRight",
                "justifyFull",
                "insertUnorderedList",
                "insertOrderedList",
                "indent",
                "outdent",
                "createLink",
                "unlink",
                "insertImage",
                "insertFile",
                "subscript",
                "superscript",
                "createTable",
                "addRowAbove",
                "addRowBelow",
                "addColumnLeft",
                "addColumnRight",
                "deleteRow",
                "deleteColumn",
                "viewHtml",
                "formatting",
                "cleanFormatting",
                "fontName",
                "fontSize",
                "foreColor",
                "backColor"
            ]
        }); 
        $("#send_email_btn").bind("click", function(){m.sendEmail();}) 
    });     
})(jQuery);
