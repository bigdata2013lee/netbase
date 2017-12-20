(function($){
    var widgets = [];
    var m = window.device_adds = new nb.xutils.Observer();
    m.currentDevId = window.moUid;
    //===初始化标签页===
    var initTabStrip = function () {
        var original = $("#tabstrip").clone(true);
        original.find(".k-state-active").removeClass("k-state-active");
        $("#tabstrip").kendoTabStrip({ animation: { open: { effects: "fadeIn" } } }).css({ marginRight: "0px" });
        $(".configuration input").change(function() {
            var tabStrip = $("#tabstrip"),
                selectedIndex = tabStrip.data("kendoTabStrip").select().index(),
                clone = original.clone(true);
            clone.children("ul")
                .children("li")
                .eq(selectedIndex)
                .addClass("k-state-active")
                .end();
            tabStrip.replaceWith(clone);
            initTabStrip();
        });
    };
    var name = 1;
    function show(){
        var i = $(".name_snmp").length;
        if(i>=2){
            $("#btnAddName").hide();
        }
        else
        {
            $("#btnAddName").show();
        }
    }
    function bindselect(){
        var sel=document.getElementById("collector");
        var sel2=document.getElementById("collector2");

        nb.rpc.deviceViews.c("listCollectors").
            success(function(colls){
                for(var i=0;i<colls.length;i++){
                    sel.options.add(new Option(colls[i].title,colls[i]._id));
                    sel2.options.add(new Option(colls[i].title,colls[i]._id));
                }
        });
    }
    $(document).ready(function() {
        initTabStrip();
        bindselect();

        $("div.op_bar input[name=save]").bind("click", function(){
            var errmsg = $("#addipWidget .validateErrorMsg");
            errmsg.html("");
            errmsg.hide();
            var tips = $("#ips").val();
            tips = tips.replace(/[ ]/g,"");
            if($("#ips").size() == 0){
                errmsg.html("IP网段不能为空");
                errmsg.show();
                return;
            }
            var exp=/^[0-9]{3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[/][0-9]{1,3}$/;
            var reg = tips.match(exp);
            if(reg==null){
                errmsg.html("IP网段格式错误");
                errmsg.show();
                return;
            }
            var tt = tips.split('/');
            if(tt[1]>32){
                errmsg.html("IP网段格式错误，子网掩码不能大于32");
                errmsg.show();
                return;
            }
            var tconllector =  $("#collector").val();
            if(!tconllector||tconllector == "0"){
                errmsg.html("请选择收集器");
                errmsg.show();
                return;
            }
            var ttype=$('input:radio[name="deviceclass1"]:checked').val();
            var snmpname = $("#snmpname").val();
            var obj =  $(".name_snmp");
            for(var i=0;i<obj.length;i++){
                if(obj[i].value&&obj[i].value.length > 0){
                    snmpname = snmpname + "," +  obj[i].value;
                }
            }
            if(snmpname.length == 0||snmpname==","){
                errmsg.html("Snmp团体名不能为空");
                errmsg.show();
                return;
            }
            var loading = nb.uiTools.commLoading.insertTo("body");
            loading.css({"position":"fixed"});
            loading.find("span:first").css({"margin-top":"105px"});
            loading.find("span:first").html("正在批量添加设备，所需时间较长，请不要进行其他操作，耐心等待。");
            nb.rpc.deviceViews.c("batchNetAddDevice",{batchConfig:{ips:tips,deviceclass:ttype,snmpname:snmpname,collector:tconllector}}).error(function(err){
            	nb.uiTools.commLoading.cancel("body");
            }).success(function(data){
                nb.uiTools.commLoading.cancel("body");
                var datas = eval('(' + data + ')');
                $("#div_addip").hide();
                $("#div_addipResult").show();
                $(".info").html(datas.info);
                var html=[];
                if(data.error == "0"){
	                var html=[];
	                for(var i=0;i<datas.detail.length;i++){
	                    html.push("<tr><td class='tb02'>"+datas.detail[i].ip+"</td><td class='tb02'>"+datas.detail[i].message+"</td></tr>");
	                }
	                $(".endtable").before(html.join(''));
                }
                else{
                	$(".tabChart").hide();
                }
            });
        });
        $("#btnAddName").bind("click",function(){
            var html='<div class="divsnmpname" id="name_'+name+'"><input type="text" class="name_snmp" id="snmpname_'+name+'" /> <input type="button" data-id="name_'+name+'" class="delsnmpname" value="删除"/></div> ';
            $(".addname").before(html);
            name = name + 1;
            show();
            $(".delsnmpname").unbind("click");
            $(".delsnmpname").bind("click", function(){
                var id = $(this).attr("data-id");
                $("#"+id).remove();
                show();
            });
        });
        $("#sec_menus_bar li>a").each(function(){
            var link = $(this);
            var href = link.attr("href");

            if(href == "/monitor/devicesConfigOp/"){
                link.parent().addClass("active");
                link.parent().siblings().removeClass("active");
            }
        });
        // hostTree.on("changeTreeNodeType", function(nodeType, uname){
            // if(nodeType=="DeviceClass"){
                // $("#tree_op_bar div.box.DeviceClass").show();
                // $("#tree_op_bar div.box.Device").hide();
// 
                // if(uname == "devicecls"){
                    // $("#tree_op_bar div.box.DeviceClass").hide();
                    // $("#tree_op_bar div.box.Device").hide();
                // }
            // }
            // else{
                // $("#tree_op_bar div.box.DeviceClass").hide();
                // $("#tree_op_bar div.box.Device").show();
            // }
// 
// 
        // });
    });

})(jQuery);








