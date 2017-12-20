
(function($){
    
    var m =  nb.nameSpace("BaseWidgets");
    
    m.extend=function(name, extObj1, extObj2){
    	return  $.extend({}, m[name], extObj1, extObj2||{});
    }
    
    /**
     * 多线的性能图基类
     */
    m.baseMultiplePerfImgWidget = {
        _data:[],
        afterRemote:function(datas){},
        _legendRight:true,
        _render: function(){
            var self = this;
            var legend ={
                    enabled:true, showInLegend:true, borderWidth:0
            };
            
            if(self._legendRight){
                $.extend(legend,{layout:'vertical', align:'right', verticalAlign:'top', x:-1, y:100});
            }

            var div = $(self._panel_id + " .box:first");
            $(self._panel_id + " .box:first").highcharts('StockChart', {
                rangeSelector : {
                    selected : 0, enabled:false,
                    buttons: [{type: 'day', count: 1, text: '1d'}, {type: 'all',text: 'All'}]   
                },
                scrollbar:{enabled: false},
                title : {text : self.title},
                legend:legend,
                series :  self.series
            });
            

        },
        
        reload: function(){
            var self = this;
            nb.uiTools.panelLoading.insertTo(self._panel_id);
            self.remoteView.c(self.remoteMethod, function(){return self.getRemoteParams()}).
            success(function(datas){
                nb.uiTools.panelLoading.cancel(self._panel_id);
                self.afterRemote(datas);
                self.series = datas;
                self._render();
            });
            
        }
    }; 
    
    
    /**
     * 多线的性能图基类
     */
    m.twoYAxisMultiplePerfImgWidget = {
        _data:[],
        afterRemote:function(datas){},
        _legendRight:true,
        _render: function(){
            var self = this;
            var legend ={
                    enabled:true, showInLegend:true, borderWidth:0
            };
            
            if(self._legendRight){
                $.extend(legend,{layout:'vertical', align:'right', verticalAlign:'top', x:-1, y:100});
            }

            var div = $(self._panel_id + " .box:first");
            $(self._panel_id + " .box:first").highcharts('StockChart', {
                rangeSelector : {
                    selected : 0, enabled:false,
                    buttons: [{type: 'day', count: 1, text: '1d'}, {type: 'all',text: 'All'}]   
                },
                scrollbar:{enabled: false},
                title : {text : self.title},
                legend:legend,
                yAxis: [
                    {title: {text: '' },height: 160, lineWidth: 1}, 
                    {title: { text: '' }, top: 180, offset: 0, height: 160, lineWidth: 1}
                 ],
                series :  self.series
            });
            

        },
        
        reload: function(){
            var self = this;
            nb.uiTools.panelLoading.insertTo(self._panel_id);
            self.remoteView.c(self.remoteMethod, function(){return self.getRemoteParams()}).
            success(function(datas){
                nb.uiTools.panelLoading.cancel(self._panel_id);
                self.afterRemote(datas);
                self.series = datas;
                self._render();
            });
            
        }
    }; 
    
    
    
    //------------------------------------------------------------------------------------------//
    

	m.BaseAvailabilityImageWidget = {
		timeRange: 3600,
		chartConf : {},
		_render: function(data){
			var series = data.series;
			var categories = data.categories;
			$.each(series, function(i, item){
				$.each(item.data, function(j, val){
					val = nb.Render.percent(val);
					item.data[j] = val;
				});
			});
			var _charts = {
				title: {text: ' '},
				xAxis: { categories: categories, labels:{rotation:30}},
				yAxis: {
					title: {text: '可用性 (%)'},min:0, max:100,
					plotLines: [{value: 0, width: 1, color: '#808080'}]
				},
				tooltip: { valueSuffix: '%' },
				legend: {
					layout: 'vertical', align: 'right', 
					verticalAlign: 'middle', borderWidth:0

				},
				series: series
			};
			_charts = $.extend(_charts, this.chartConf)
			$(this._panel_id + ' div.box:first').highcharts(_charts);
		},
		reload:function(){
			var self = this;
			nb.uiTools.panelLoading.insertTo(self._panel_id);
			var params = self.getRemoteParams ? self.getRemoteParams() : {};
			self.remoteView.c(self.remoteMethod,params)
			.success(function(data){
			    nb.uiTools.panelLoading.cancel(self._panel_id);
				self._render(data);
			});
		}	
	};


    m.BaseListWidget = {
        _panel_id:null,
        __ds:null,
        __pageSize:null,
        __body:null,
        remoteView:null,
        remoteMethod:null,
        getRemoteParams: function(){return {}},
        afterChange:function(){},
        ds: function(){
            var self = this;
            if(self.__ds) return self.__ds;
            var params = self.getRemoteParams ? function(){return self.getRemoteParams()} : {};
            var ds = new kendo.data.DataSource({
                transport : {
                    read : self.remoteView.rc(self.remoteMethod, params)
                },
                
                change: function() {
                    nb.uiTools.panelLoading.cancel(self._panel_id);
                    var template = self.getTemplate();
                    $(self._panel_id + " " + (self.__body || "tbody:first")).html(kendo.render(template, this.view()));
                    $(self._panel_id + " tbody:first>tr:not(.nested_tr):odd").each(function(){ $(this).addClass("odd"); });
                    self.afterChange();
                },
                pageSize:self.__pageSize
            });
            self.__ds = ds;
            return ds;
        },

        getTemplate: function(){
            var template = kendo.template($(this._panel_id + " script[name=template]").html());
            return template;
        },
        reload: function(){
            var self = this;
            if(self.ableReload === false) return;
            nb.uiTools.panelLoading.insertTo(self._panel_id);
            this.ds().read();

            if(self.onLoad) self.onLoad();

            if(self.__pageSize){
                var messages = { display:"{0} - {1} 共 {2} 条数据",empty : "无数据显示" }
                $(self._panel_id +  " .pager:first").kendoPager({ dataSource: self.ds(), messages:messages});
            }
        },
        
        __init__: function(){
            var self = this;
            $(self._panel_id + " .panelActions a[name=refresh_action]").bind("click", function(){self.reload()});
            if(self.afterInit){self.afterInit();}
        }
    };
    
	
	//表格式列表
	m.BaseGridListWidget = $.extend({}, {
		_panel_id: null, //--->rewrite
		_ds: null,
		remoteMethod: null,  //--->rewrite
		remoteView: null, //--->rewrite
		pageSize: 20,
		afterInit: function(){},
		_columns: [],//--->rewrite
		_gridConf:{},//--->rewrite
		getRemoteParams: function(){return {}},
		ds: function(){
			var self = this;
			if(self._ds) return self._ds;
			var params = self.getRemoteParams ? function(){return self.getRemoteParams()} : {};
		    var ds = new kendo.data.DataSource({
		        type : "json",
		        pageSize : self.pageSize,
		        transport : {
		            read : self.remoteView.rc(self.remoteMethod, params)

		        },
		        change: function() {}
		    });
		    self._ds = ds;
		    return self._ds;
		},
		
		reload: function(){
			var self = this;
			self.ds().read();
		},
			
		
		_render: function(){
			var self = this;
			
			var gridConf = {
				dataSource : self.ds(),
	            columns : self._columns,
	            
	            height : 200,
	            pageable:true,
	            selectable : false,
	            sortable : true
			};
			
			$.extend(gridConf, self._gridConf);
			$(self._panel_id + " div.data_grid").kendoGrid(gridConf);
	    	
	    	return $(self._panel_id + " div.data_grid").data("kendoGrid");
		},
		__init__: function(){
            var self = this;
            self._render();
            $(self._panel_id + " .panelActions a[name=refresh_action]").bind("click", function(){self.reload();});
            if(self.afterInit){
            	self.afterInit();
            }
        }
		
	});
    
    
    
    	

	/**
	 *列出设备（网络设备）组件列表，通过命令或snmp方式得到原始的组件信息 
	 */
	
	var _getKeysMap = function(key){
        var keysMap = {
            interfaces:deviceConfig.interfacesGridWidget, processes:deviceConfig.processesGridWidget, 
            fileSystems:deviceConfig.fileSystemsGridWidget, ipServices:deviceConfig.ipServicesGridWidget
        };
        if(key){
            return keysMap[key];
        }
        return keysMap;
    };
	
	m.ListDevComponentsWidget = {
		__ds:null,
		_remoteView:null,
		getRemoteParams:function(){return{}},
		ds: function(){
			var self = this;
			if(self.__ds) return self.__ds;
			var ds = new kendo.data.DataSource({
				transport : {
					read : self._remoteView.rc(self.remoteMethod, function(){
						return self.getRemoteParams();
					})
				},
				schema: {
					data: function(response) {
						if(!$.isEmptyObject(response.message)){
							nb.AlertTip.warn(response.message);
						}
						return response.data; // twitter's response is { "results": [ /* results */ ] }
					}
				},
				change: function() {
				    nb.uiTools.panelLoading.cancel(self._panel_id);
					var template = self.getTemplate();
					$(self._panel_id + " tbody:first").html(kendo.render(template, this.view()));
					$(self._panel_id + " tbody:first>tr:odd").each(function(){ $(this).addClass("odd"); });
					if(self.afterChange){self.afterChange();}
				}
			});
			
			self.__ds = ds;
			return ds;
		},
	    getTemplate: function(){
	    	var template = kendo.template($(this._panel_id + " script[name=template]").html());
	    	return template;
	    },
	    reload: function(){
	        var self = this;
	        nb.uiTools.panelLoading.insertTo(self._panel_id);
	    	this.ds().read();
	    },
	    /**
	     *显示完后，标记已添加的组件 
	     */
        _afterChangeFixExist:function(){
            var self = this;
            var trs = $(self._panel_id + " tbody:first tr");
            var existEscapeUnames = [];
            $.each(_getKeysMap(self._ckeyName).ds().data(), function(i, d){
                existEscapeUnames.push(escape(d.uname));
            });
            
            trs.each(function(){
                if($.inArray($(this).attr("uname"), existEscapeUnames) >=0){
                    $(this).addClass("exist");
                }
            });
        }	    
	};
	

    m.baseInfoWidget = {
        _panel_id:null,
        _data:null,
        remoteView:null,
        remoteMethod:"",
        getRemoteParams:function(){return {}},
        _render: function(){
            var self = this;
            var template = self.getTemplate();
            $(self._panel_id + " .box:first").html(template(self._data));
        },
        getTemplate: function(){
            var template = kendo.template($(this._panel_id + " script[name=template]").html());
            return template;
        },
        
        reload: function(){
            var self = this;
            nb.uiTools.panelLoading.insertTo(self._panel_id);
            self.remoteView.c(self.remoteMethod,self.getRemoteParams()).
            success(function(obj){
                nb.uiTools.panelLoading.cancel(self._panel_id);
                self._data = obj; 
                self._render() 
                if(self.onLoad){self.onLoad();}
            });
        },
        __init__: function(){
            var self = this;
            $(self._panel_id + " .panelActions a[name=refresh_action]").bind("click", function(){self.reload()});
        }
    };

    
    m.thresholdConfigWidget={
        _panel_id: null,
        _moUid:null,
        _getMoUid:function(){return null},
        _moType:null,
        _render: function(){
            var self = this;
            $(self._panel_id + " .box:first").show();
        },
        reload:function(){
            var self = this;
            nb.uiTools.panelLoading.insertTo(self._panel_id);
            var listUrl = nb.xutils.formatStr("/template/thresholdList/{0}/{1}/", self._moUid||self._getMoUid(), self._moType);
            $(self._panel_id + " .box.thresholdConfig").load(listUrl,{},function(){
                self._render();
                nb.uiTools.panelLoading.cancel(self._panel_id);
            });
        },
        _validate:function(){
            return false;
        },
        _dealThresholdVal:function(type, threshold, tr){
            var setNumVal = function(name){
                var v = tr.find("input[name=" + name + "]").val();
                if($.isNumeric(v)){ threshold[name] = v*1; }
            };
            
            var setStrVal = function(name){
                var v = $.trim(tr.find("input[name="+name+"]").val());
                if(!$.isEmptyObject(v)){ threshold[name] = v; }
            };
            
            if(type=="MinThreshold"){//数字处理
                 setNumVal("min");
            }
            else if(type=="MaxThreshold"){//数字处理
                 setNumVal("max");
            }
            
            else if(type=="RangeThreshold"){//数字处理
                 setNumVal("min");
                 setNumVal("max");
            }
            
            else if(type=="StatusThreshold"){//如果状态填写的是数字，则当数字处理，否则当字符处理
                 var v = tr.find("input[name=status]").val();
                 v = $.trim(v);
                 if($.isNumeric(v)){
                     setNumVal("status");
                 }
                 else{
                     setStrVal("status");
                 }
            }
            
            else if(type=="KeyThreshold"){//字符处理
                 setStrVal("key");
            }
 
        },
        save:function(){
            var self  = this;
            var thresholds = {};
            $(self._panel_id + " .box.thresholdConfig tr").each(function(){
                var tr = $(this);
                var key = tr.attr("key"), type=tr.attr("type");
                
                if($.isEmptyObject(key) || $.isEmptyObject(type)){return;}
                var threshold = thresholds[key] = {};
                threshold.severity = tr.find("select[name=severity]").val() * 1;
                threshold.monitored = nb.xutils.val2boolean(tr.find("select[name=monitored]").val());
                self._dealThresholdVal(type, threshold, tr);
            });
            var params = {"uid": self._moUid||self._getMoUid(), "cType":self._moType, "thresholds":thresholds};
            nb.rpc.thresholdViews.c("setMoThresholds",params).success(function(msg){
                nb.AlertTip.auto(msg);
                self.reload();
            });
        },
        __init__:function(){
            var self = this;
            $(self._panel_id + " .op_bar a[name=save]").bind("click", function(){self.save()});
        }
    };


    

    /**
    *多性能图组件
    */
    m.multiPerfImgWidget = $.extend({},{
        _panel_id:"", //->rewrite
        _currentMoUids:[], //->rewrite
        _max:2, //->rewrite
        cookieName:"", //->rewrite
        timeUnit:"day",
        remoteView:null, //->rewrite
        perfsRemoteMethod:"", //读取对象性能图数据的方法 //->rewrite
        getPerfsRemoteMethodParams: function(moUid){return {}},
        moListRemoteMethod:"", //读取对象列表的方法 //->rewrite
        getMoListRemoteMethodParams: function(){return {}},  //->rewrite
        _stockChartConf:function(item){return {}},
        afterInit:function(){},
        
        loadmoLabels:function(){
        	var self = this;
        	nb.rpc.deviceViews.c(self.moListRemoteMethod, 
                    function(){return self.getMoListRemoteMethodParams()})
            .success(function(mos){
        		var moLabels = $(self._panel_id + " .mo_labels");
        		self.moList = mos;
        		$.each(mos, function(i, mo){
        			moLabels.append($(nb.xutils.formatStr('<span moUid="{0}">{1}</span>', mo._id, kendo.htmlEncode(nb.Render.ellipsisStr(mo.uname || mo.title, 50)))));
        		});
                moLabels.append("<br clear='both'/>");
        		self.afterLoadMoLabels();
        	});
        },
        
        afterLoadMoLabels:function(){
        	var self = this;
            var _uids = self._restoreCurrentMoUidsFromCookie();
            var uids = $.isEmptyObject(self._currentMoUids) ? _uids : self._currentMoUids;
            self._currentMoUids = [];
        	
        	$.each(uids, function(i, moUid){
        		self._appendPerf(moUid);
        	});
        },
        _isExistMoUid:function(moUid){
        	return $.inArray(moUid, this._currentMoUids) > -1;
        },
        _shiftPerf:function(){
            var self = this;
            var shiftMoUid = self._currentMoUids.shift();
            $(self._panel_id + " .box>.chart_div[mo_uid="+shiftMoUid+"]").remove();
            $(self._panel_id + " span[moUid="+shiftMoUid+"]").removeClass("selected");
        },
        _appendPerf:function(moUid){
            
            var  self = this;
            if(self._currentMoUids.length >= self._max){
                self._shiftPerf();
            };
            self._currentMoUids.push(moUid);
            self._loadMoPerf(moUid);
            self._storeCurrentMoUidsToCookie();
            $(self._panel_id + " span[moUid="+moUid+"]").addClass("selected");
        },
        _restoreCurrentMoUidsFromCookie:function(){
            var self = this;
            var ck = $.evalJSON($.cookie(self.cookieName)|| "[]");
            
            var rs = [];
            var allmap = {};
            
            $.each(self.moList, function(i,mo){allmap[mo._id]=1});
            $.each(ck, function(i,key){if(key in allmap){rs.push(key);} });
            
            $.each(self.moList, function(i,mo){
                if($.inArray(mo._id,rs) == -1){rs.push(mo._id)}
            });
            return rs.slice(0, self._max);

        },
        _storeCurrentMoUidsToCookie:function(){
            var self = this;
            $.cookie(self.cookieName, $.toJSON(self._currentMoUids), {expires:3});
        },
        _loadMoPerf:function(moUid){
            var self = this;
            
            var legend ={enabled:true, showInLegend:true, borderWidth:0 };
            
            if(self._legendRight){
                $.extend(legend,{layout:'vertical', align:'right', verticalAlign:'top', x:-1, y:100});
            }
            var boxDiv = $(self._panel_id + " div.box:first");
            var div = $(nb.xutils.formatStr("<div mo_uid='{0}' class='chart_div'></div>", moUid));
            boxDiv.prepend(div);
            nb.rpc.deviceViews.c(self.perfsRemoteMethod, 
                    function(){return self.getPerfsRemoteMethodParams(moUid)})
            .success(function(item){
	            div.highcharts('StockChart', $.extend({
	                rangeSelector : { selected : 0, enabled:false},
	                scrollbar:{enabled: false},
	                title : {text : nb.Render.ellipsisStr(item.title, 34), style:{fontSize: '12px', color:"#730000"}},
	                legend:legend,
	                tooltip:{
	                    formatter:function(tooltip){
	                        var items = this.points || splat(this);
	                        var series = items[0].series; var s=[];
	                
	                        // build the header
	                        s = [series.tooltipHeaderFormatter(items[0])];
	                
	                        // build the values
	                        $.each(items, function (i,item) {
	                            var point = item.point;
	                            series = item.series;
	                               var pointFormat = '<span style="color:{0}">{1}</span>: <b>{2}</b><br/>';
	                               var x = nb.xutils.formatStr(pointFormat, series.color, series.name, nb.Render.byte2readable(point.y, true));
	                               s.push(x);
	                        });
	                
	                        // footer
	                        s.push(tooltip.options.footerFormat || '');
	                
	                        return s.join('');
	                    }
	                },
	                
	                series :  item.series
	            }, self._stockChartConf(item)));
           
            });//end remote.
        	
        },
        _legendRight:true,
        _render: function(){
        	var self = this;
        	$(self._panel_id + " .mo_labels").html("");
        	$(self._panel_id + " div.box:first").html("");
			self.loadmoLabels();
        },
        
        reload: function(){
            var self = this;
            self._render();
            
        },
        __init__: function(){
            var self = this;
            if($(self._panel_id + " .mo_labels").size() == 0){
        		var box = $(self._panel_id + " div.box:first");
        		$('<div class="mo_labels"></div>').insertBefore(box);
        	}
            new nb.uiTools.TimeUnitBar(self);
            $(self._panel_id + " .panelActions a[name=refresh_action]").bind("click", function(){self.reload()});
            $(self._panel_id).delegate(".mo_labels>span", "click", function(){
            	var moUid = $(this).attr("moUid");
                //console.info("exist:",self._isExistMoUid(moUid));
                if(self._isExistMoUid(moUid)){return;}
            	self._appendPerf(moUid);
            });
            self.afterInit();
        }
    });
    

    //下拉列表选择控件
    m.autoComplateWidget={
      _panel_id:"#autoComplateWidget", //rewrite
      _data:[],
      _max:3,
      delItem:function(em){
          
      },
      filter:function(chars){
          var self = this;
          var match_list = [];
          var exist_list = self.getSelectedItems();
          filedsDict = technologyFiledsSearch(chars, exist_list);
          $(self._panel_id + "  ul.item_list").html("");
          for(pLabel in filedsDict){
              $(self._panel_id + "  ul.item_list").append("<li class='pLabel'>"+pLabel+"</li>");
              $.each(filedsDict[pLabel], function(i, item){
                  $(self._panel_id + "  ul.item_list").append("<li class='cLabel'>"+item.label+"</li>");
              })
          }
      },
      getSelectedItems:function(){
          var self = this;
          var slectedList=[];
          $(self._panel_id + " .input_box span").each(function(){
              slectedList.push($(this).attr("value"));
          });
          return slectedList;
      },
      select:function(li){
          var self = this;
          var item_select = $(li).text();
          var span = $("<span value='" +item_select+ "'>" +item_select+ " <em>x</em></span>");
          
          span.insertBefore($(self._panel_id + " input.input_cls"));
          $(self._panel_id + "  ul.item_list").html("").hide();
          $(self._panel_id + " .input_box input.input_cls").val("");
      },
      __init__:function(){
          var self = this;
          self._data=window.technologyFileds||[];
          $(self._panel_id + " .input_box input.input_cls").bind("keyup",function(evt){
              var item_input = $(this).val();
              self.filter(item_input);
              $(self._panel_id + "  ul.item_list").show();
          });
          $("body").bind("click", function(evt){
              if($(evt.target).closest(self._panel_id).size()==0){
                  $(self._panel_id + "  ul.item_list").html("").hide();
                  $(self._panel_id + " .input_box input.input_cls").val("");
              }
          });
          $(self._panel_id + "  ul.item_list").delegate("li.cLabel", "click",function(evt){
              if($(self._panel_id + " .input_box span").size()>=self._max){
                  $(self._panel_id + "  ul.item_list").html("").hide();
                  $(self._panel_id + " .input_box input.input_cls").val("");
                  alert("对不起，您不能选择太多的标签");
                  return;
              }
              self.select(this);
          })
          $(self._panel_id).delegate(".input_box span em","click",function(){
              $(this).parent().remove();
          })
      }  
    };

    //服务地域选择列表控件
    m.areaAutoComplateWidget={
      _panel_id:"#areaAutoComplateWidget", //rewrite
      _data:[],
      _max:3,
      delItem:function(em){
          
      },
      filter:function(chars){
          var self = this;
          var match_list = [];
          var exist_list = self.getSelectedItems();
          
          filedsDict = nb_areasSearch(chars, exist_list);

          
          $(self._panel_id + "  ul.item_list").html("");
          for(pLabel in filedsDict){
              $(self._panel_id + "  ul.item_list").append("<li class='pLabel'>"+pLabel+"</li>");
              $.each(filedsDict[pLabel], function(i, item){
                  $(self._panel_id + "  ul.item_list").append("<li class='cLabel'>"+item+"</li>");
              })
          }
          
      },
      
      getSelectedItems:function(){
          var self = this;
          var slectedList=[];
          $(self._panel_id + " .input_box span").each(function(){
              slectedList.push($(this).attr("value"));
          });
          
          return slectedList;
      },
      
      select:function(li){
          var self = this;
          var item_select = $(li).text();
          var span = $("<span value='" +item_select+ "'>" +item_select+ " <em>x</em></span>");
          
          span.insertBefore($(self._panel_id + " input.input_cls"));
          $(self._panel_id + "  ul.item_list").html("").hide();
          $(self._panel_id + " .input_box input.input_cls").val("");
      },
      __init__:function(){
          var self = this;
          self._data=window.nb_areas||[];
          $(self._panel_id + " .input_box input.input_cls").bind("keyup",function(evt){
              var item_input = $(this).val();
              self.filter(item_input);
              $(self._panel_id + "  ul.item_list").show();
          });
          
          $("body").bind("click", function(evt){
              if($(evt.target).closest(self._panel_id).size()==0){
                  $(self._panel_id + "  ul.item_list").html("").hide();
                  $(self._panel_id + " .input_box input.input_cls").val("");
              }
          });
          
          $(self._panel_id + "  ul.item_list").delegate("li.cLabel", "click",function(evt){
              if($(self._panel_id + " .input_box span").size()>=self._max){
                  $(self._panel_id + "  ul.item_list").html("").hide();
                  $(self._panel_id + " .input_box input.input_cls").val("");
                  alert("对不起，您不能选择太多的标签");
                  return;
              }
              self.select(this);
          })
          $(self._panel_id).delegate(".input_box span em","click",function(){
              $(this).parent().remove();
          })
      }  
    };


    
})(jQuery);
    