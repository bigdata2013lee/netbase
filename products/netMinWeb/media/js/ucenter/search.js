(function($){
	//查询分享或提问的组件【2014.12.19  jenny】
	//包含标题、服务区域、技术领域 三个查询条件
    var m = new nb.xutils.Observer();

    var autoComplateWidget = nb.BaseWidgets.extend("autoComplateWidget",{},{});
    var searchWidget={
        searchConditions:{},
        _searchBoxId:"#search_box",
        _searchResultId:"#search_results",
        
        makeConditions:function(){
            var self = this;
            self.searchConditions.keywords=$(self._searchBoxId+ " input[name=search_txt]").val();
            self.searchConditions["search_field"]=$(self._searchBoxId+ " input[name=search_field]:checked").val();
            self.searchConditions["d0"]=$(self._searchBoxId+ " select[name=province]").val();
            self.searchConditions["d1"]=$(self._searchBoxId+ " select[name=city]").val();
            self.searchConditions["fields"]=autoComplateWidget.getSelectedItems().join(",");
        },
        search:function(pageNum){
            var self = this;
            var search_info={};
            $.extend(search_info, self.searchConditions);
            search_info["pageNum"] =pageNum;
            
            if(search_info.search_field == "question"){
                $.post((window.prefixName || "/ucenter") + "/searchQuestions/",search_info, function(html){
                    $(self._searchResultId).html(html);
                });
            }
            if(search_info.search_field == "share"){
                $.post((window.prefixName || "/ucenter") + "/searchShares/",search_info, function(html){
                    $(self._searchResultId).html(html);
                });
            }
        },      
        __init__:function(){
            var self = this;
            $("#search_btn").bind("click",function(){
                self.makeConditions();
                self.search();
            });
            
            $(self._searchResultId).delegate("div.pages_tools a", "click",function(evt){
                var pagenum = $(this).attr("page_num");
                self.search(pagenum);
            });
        }
    }
    
        
    $(document).ready(function(){
        nb.uiTools.setAreaSelect();
        searchWidget.__init__();
        autoComplateWidget.__init__();
    });
    
})(jQuery);