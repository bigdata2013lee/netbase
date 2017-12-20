(function($){
    //页面设置js文件  【2014.12.23  jenny】
        
    /**
	 * 设置被选中一级菜单的背景图片色
	 * @method selectNavMenu
	 * 
	 */
    var selectNavMenu = function(){
    	
    	if(window.nb_firstNav != undefined){
    	    $("#top-panel div.navigation li:eq("+nb_firstNav+")").addClass("selected");
    	    return;
    	}
    	var pathname = window.location.pathname;
    	$("#top-panel div.navigation li>a").each(function(){
    		var link = $(this); 
    		var href = link.attr("href");
    		var prefix = link.attr("prefix");
    		if(!prefix || prefix == ''){
    		    /^(\/\w+).*/.test(href);
    		    prefix = RegExp.$1;
    		}
    		if(pathname.indexOf("/location")==0 || pathname.indexOf("/website") == 0 ||pathname.indexOf("/network") == 0 ||pathname.indexOf("/middleware") == 0 ){
	    		if(prefix == "/monitor"){
	    			link.parent().addClass("selected");
	    		}
	    	}
    		if(pathname.indexOf(prefix) == 0){link.parent().addClass("selected")}
    	});
    };
    
    /**
	 * 设置被选中二级菜单的背景图片色
	 * @method selectSecNavMenu
	 * 
	 */
    var selectSecNavMenu = function(){
    	var pathname = window.location.pathname;
    	$("#sec_menus_bar li>a").each(function(){
    		var link = $(this); 
    		var href = link.attr("href");
    		
    		if(href == pathname){
    			link.parent().addClass("active");
	    		link.parent().siblings().removeClass("active");
    		}
    	});
    };
        
    /**
	 * 设置前台用户中心监控专家web服务器二级菜单样式
	 * @method selectedMiddlewareMenu
	 * 
	 */
    var selectedMiddlewareMenu = function(){
    	var pathname = window.location.pathname;
    	var middleWareLisrt = ["apache","tomcat","nginx"]
    	for(i=0;i<= middleWareLisrt.length;i++){
    		if(pathname.indexOf(middleWareLisrt[i])>0){
    			$("ul.left-menus li a").each(function(){
    				if($(this).attr("href").indexOf(middleWareLisrt[i]) > 0){
    					$(this).parent().addClass("selected");
    				}
    			})
    		}
    	}
    }
    
    /**
	 * 显示帮助信息小工具的定义函数
	 * @method netbaseTooltips
	 * 
	 */
    var netbaseTooltips = function(){
       $('a.tool_tip.help[name=help_action]').each(function(){
          var tipId = $(this).attr("tipId");
          new $.Zebra_Tooltips($(this), {
            'position':     'left',
            'min_width':    360, 
            'max_width':    600,
            content:window.NbHelpTips[tipId],
            background_color:"#DFEFFF", color:"#000"

          });
          
       });
       $('a.help[name=help_action]').each(function(){
            var tipId = $(this).attr("tipId");
            
            new $.Zebra_Tooltips($(this), {
            'position':     'left',
            content:window.NbHelpTips[tipId],
            background_color:"#DFEFFF", color:"#000"

          });
       });
       
    }

    $(document).ready(function(){
		//获取当前浏览器窗口大小，并调整弹出层位置
        var fixPage = function(){
             var mh = $("#middle-panel").height();
             $("#user_status_expired_overlayer").height(mh);
        };
        
        var pathname = window.location.pathname;
        if(pathname.indexOf("middleware")>0){
        	selectedMiddlewareMenu();
        }
        
        fixPage();
        setInterval(function(){fixPage()}, 1000);
        
        selectNavMenu();
        selectSecNavMenu();
        
        netbaseTooltips();

        if(/MSIE\s*7/.test(navigator.appVersion)){
            //修复IE7问题
            $(".panel_min.psbar").bind("mouseover", function(){
                $(this).find(".ps-scrollbar-y-rail").show();
                $(this).find(".ps-scrollbar-y").show();
            })
        };
        $(".panel_min.psbar").each(function(){
            $(this).css({"overflow":"hidden"});
            $(this).perfectScrollbar();
        });
        $("#user_status_expired_overlayer .op_bar").delegate("a[name=close]","click", function(){
            $("#user_status_expired_overlayer .msg_box").hide();
        })
    });
    
})(jQuery);
