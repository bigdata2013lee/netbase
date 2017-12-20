(function(){
    
	
	var $ = jQuery;
	var skinDir = "/media/customMap/skins/";
	var getPager = function(){return Ncm.core.paper;}
    var getCanvasContiner = function(){return $("#canvas_continer")}

    /**
     * 画线事件集
     */
    var drawLineHandles = {

        start: function(p, evt){
            drawLineHandles.clearEvents();
            var p = p || Ncm.utils.getMousePoint(evt);
            var mypath = getPager().path([['M', p.x, p.y],['L', p.x, p.y]]);
            mypath.attr({'stroke-width': 2, stroke: '#1F5CF6'});

            mypath.insertBefore(Ncm.core.__firstFgPath);

            return mypath;
        },
        move: function(evt){
            var p = Ncm.utils.getMousePoint(evt);
            var pathObj = evt.data;
            var path = pathObj.attr('path');

            path[1][1] = p.x-2;
            path[1][2] = p.y-2;
            pathObj.attr('path', path);
        },
        end: function(evt){
            //console.info('end',evt);
            drawLineHandles.clearEvents();
            var pathObj = evt.data;
            pathObj.animate({stroke:'#000'}, 500);
        },
        ok: function(evt){
            //console.info('ok',evt);
            var oPath = evt.data.path;
            var cmo = evt.data.cmo;
            var targetCmo = evt.target._cmo;
            var conn = null;
            Ncm.fireEvent('beforeChange','linkTo', function(){ return conn; });
            conn = cmo.conn2(targetCmo);

            if(conn) {
                conn.line.attr({'fill': '#1F5CF6'})
                .animate({'fill': '#000000'}, 1000);
            }
            oPath.remove();
            if(conn) Ncm.fireEvent('afterChange');
        },
        clearEvents : function(){
            getCanvasContiner().unbind('mousemove', drawLineHandles.move);
            getCanvasContiner().unbind('mouseup', drawLineHandles.ok);
            getCanvasContiner().unbind('mouseup', drawLineHandles.end);
        }

    }

    //------------------------------------------------------------


	
    /**
     * 菜单功能
     */
    Ncm.Menus = {
        _cmo: null,   //当前操作对象
        
        /**
         * 弹出对象菜单
         */
        popupCmoMenu : function(cmo,evt){
            var pageXY = Ncm.utils.getPageXY(evt);
            //console.info(pageXY, evt);

            var p = {left:  pageXY.x + 10, top:  pageXY.y + 10};
            Ncm.Menus.hide();
            var mainMenuItem =  $('#custom_map_menus .mainMenu.cmodev');
            mainMenuItem.show().css(p);
            if(cmo && cmo instanceof Ncm.CustomMapObjIf){
                mainMenuItem.find('li.setSize').hide();
                mainMenuItem.find('li.setIcon').hide();

            }
            else{
                mainMenuItem.find('li.setSize').show();
                mainMenuItem.find('li.setIcon').show();

            }

            if(cmo && cmo instanceof Ncm.CustomMapObjDev){
                mainMenuItem.find('li.addInterface').show();
            }
            else{
                mainMenuItem.find('li.addInterface').hide();
            }

            Ncm.Menus._cmo = cmo;
        },
        
        /**
         * 弹出画布菜单
         */
        popupCanvasMenu : function(evt){
            var pageXY = Ncm.utils.getPageXY(evt);
            var p = {left:  pageXY.x + 10, top:  pageXY.y + 10};
            var mp = Ncm.utils.getMousePoint(evt);
            Ncm.Menus._mp = mp;
            Ncm.Menus.hide();
            var mainMenuItem =  $('#custom_map_menus .mainMenu.canvas');
            mainMenuItem.show().css(p);

        },
        hideIconsPanel : function(){
            $('#custom_map_cmo_icons').find('>div').hide();
            $('#custom_map_cmo_icons').hide();
        },
        hide: function(){
            Ncm.Menus.hideIconsPanel();
            $('#custom_map_menus .mainMenu').hide();
        },
        linkTo: function(evt){
            var cmo = Ncm.Menus._cmo;
            var path = drawLineHandles.start(cmo.getCenterPonit(), evt);
            getCanvasContiner().bind('mousemove', path,  drawLineHandles.move);
            getCanvasContiner().bind('mouseup', path,  drawLineHandles.end);
            getCanvasContiner().bind('mouseup', {path: path, cmo: cmo},  drawLineHandles.ok);
        },
        removeLines: function(){
            Ncm.fireEvent('beforeChange');
            var cmo = Ncm.Menus._cmo;
            cmo.removeLines();
            Ncm.fireEvent('afterChange');
        },

        removeCmo: function(){
            Ncm.fireEvent('beforeChange');
            var cmo = Ncm.Menus._cmo;
            cmo.remove();
            Ncm.fireEvent('afterChange');
        },

        setLableDir: function(dirName){
            var cmo = Ncm.Menus._cmo;
            Ncm.fireEvent('beforeChange', cmo.cnf.uid + 'setLableDir');
            var textUI = cmo.labelTextUI;
            var oxyf = {x: textUI.attr('x'), y: textUI.attr('y'), fill: textUI.attr('fill')};
            cmo.setLabel(null, dirName);
            textUI.hide();
            var nxyf = {x: textUI.attr('x'), y: textUI.attr('y'), fill:'blue'};

            textUI.attr(oxyf);
            textUI.show();

            textUI.animate(nxyf, 500, 'backOut', function(){
                textUI.animate({fill: '#000'}, 500, 'elastic');
            });
            Ncm.fireEvent('afterChange');
        },
        setSize: function(size){
            var cmo = Ncm.Menus._cmo;
            Ncm.fireEvent('beforeChange');
            var conns = Ncm.core.connections;
            var anCallback = function(){
                for(var i = conns.length - 1; i >= 0; i--){
                    Ncm.utils.connection2(conns[i]);
                }
            };
            cmo.setSize(size, true, anCallback);
            Ncm.fireEvent('afterChange');
        },
        setLabelSize: function(size){
            var cmo = Ncm.Menus._cmo;
            Ncm.fireEvent('beforeChange', cmo.cnf.uid + 'setLabelSize');
            cmo.setLabel(null, null, size);
            Ncm.fireEvent('afterChange');
        },
        setLabelText: function(text){
            var cmo = Ncm.Menus._cmo;
            Ncm.fireEvent('beforeChange');
            cmo.setLabel(text);
            Ncm.fireEvent('afterChange');
        },

        setIcon: function(icon){
            Ncm.fireEvent('beforeChange');
            var cmo = Ncm.Menus._cmo;
            cmo.setIcon(icon);
            Ncm.fireEvent('afterChange');
        },

        addDevice: function(options){
            Ncm.fireEvent('beforeChange');
            var cmo1 = new Ncm.CustomMapObjDev(options);
            cmo1.createUI();
            Ncm.fireEvent('afterChange');
        },

        addLocation: function(options){
            Ncm.fireEvent('beforeChange');
            var cmo1 = new Ncm.CustomMapObjLoc(options);
            cmo1.createUI();
            Ncm.fireEvent('afterChange');
        },

        addVirtualNode: function(options){
            Ncm.fireEvent('beforeChange');
            var cmo1 = new Ncm.CustomMapObjVir(options);
            cmo1.createUI();
            Ncm.fireEvent('afterChange');
        },

        addInterface : function(options){
            Ncm.fireEvent('beforeChange');
            var cmo = Ncm.Menus._cmo;
            cmo.addInterface(options);
            Ncm.fireEvent('afterChange');
        },
        setCanvasSize: function(size){
            Ncm.fireEvent('beforeChange');
            Ncm.core.setSize(size.w, size.h);
            Ncm.fireEvent('afterChange');
        },
        
        setBgImg: function(img){
            Ncm.fireEvent('beforeChange');
            Ncm.setBgImg(img);
            Ncm.fireEvent('afterChange');
        },

        /**
         * 初始化对象菜单
         * 主要是绑定菜单联系的功能行为
         */
        _initCmoMenuItems: function(){
            var mainMenuItem =  $('#custom_map_menus .mainMenu.cmodev');
            mainMenuItem.find('>li.linkTo').bind('click', function(evt){
                Ncm.Menus.hide();
                Ncm.Menus.linkTo(evt);
            });

            mainMenuItem.find('>li.removeLines').bind('click', function(evt){
                Ncm.Menus.hide();
                Ncm.Menus.removeLines(evt);
            });

            mainMenuItem.find('>li.remove').bind('click', function(evt){
                Ncm.Menus.hide();
                Ncm.Menus.removeCmo(evt);
            });

            mainMenuItem.find('>li.setIcon').bind('click', function(evt){
                Ncm.Menus.hide();
                
                //var offset = getCanvasContiner().offset();
                var offset = {left: "450px", top: "10px"};
                
                $('#custom_map_cmo_icons').show().css(offset);
                
                offset.left=($(document).width() - $('#custom_map_cmo_icons').width())/2 + "px";
                offset.top="200px";
                $('#custom_map_cmo_icons').css(offset);
                if(Ncm.Menus._cmo instanceof Ncm.CustomMapObjDev){
                    $('#custom_map_cmo_icons').find('>.device').show();
                }
                else if(Ncm.Menus._cmo instanceof Ncm.CustomMapObjLoc){
                    $('#custom_map_cmo_icons').find('>.location').show();
                }
                else if(Ncm.Menus._cmo instanceof Ncm.CustomMapObjVir){
                    $('#custom_map_cmo_icons').find('>.virtual').show();
                }
            });

            mainMenuItem.find('>li.setLableDir').delegate('td','click', function(evt){
                //Ncm.Menus.hide();
                var dirName = $(this).attr('dirName');
                Ncm.Menus.setLableDir(dirName);
            });

            mainMenuItem.find('>li.setLabelSize').delegate('li','click', function(evt){
                //Ncm.Menus.hide();
                var size = $(this).attr('labelSize');
                Ncm.Menus.setLabelSize(size);
            });

            mainMenuItem.find('>li.setLabelText').bind('click', function(evt){
                Ncm.Menus.hide();
                var cmo = Ncm.Menus._cmo;
                var newLabel = prompt('重命名标签...',  cmo.cnf.label.text);
                if(!newLabel) return;
                Ncm.Menus.setLabelText($.trim(newLabel));
            });

            mainMenuItem.find('>li.addInterface').bind('mouseover', function(evt){
                if(evt.target != this){clearTimeout(this._loadInterfaceListTimer); return;}
                clearTimeout(this._loadInterfaceListTimer);
                var addInterfaceLi = this;
                var getExistIfIds = function(){
                    var rs = [];
                    for(var uid in Ncm.core.components){
                        var cmo = Ncm.core.components[uid];
                        if(! (cmo instanceof Ncm.CustomMapObjIf))  continue;
                        if(cmo.cnf.id) rs.push(cmo.cnf.id);
                        
                    }
                    
                    return rs;
                };
                
                var loadInterfaceList = function(){
                    var moUid = Ncm.Menus._cmo.cnf.id;
                    var moType = Ncm.Menus._cmo.cnf.moType;
                    var interfaceListUl = $(addInterfaceLi).children('ul:first').html('loading...');
                    //var  url = "/media/customMap/data/getDevIfs.json";
                    var params = {moUid:moUid, moType:moType};
                    nb.rpc.customerMapViews.c("map_listIfaces", params).success(function(interfaces){
                        interfaceListUl.html('');
                        var ids = getExistIfIds();
                        $.each(interfaces, function(i, xif){
                            if($.inArray(xif._id, ids) >=0) return;
                            var li = $(Raphael.format('<li>{0}</li>', xif.title));
                            li.appendTo(interfaceListUl);
                            li.data('ifInfo', xif);
                                      
                        })//end each    
                    	
                    });
                    
                    
                };
                
                //if(! this._loadInterfaceListTimer) loadInterfaceList();
                //this._loadInterfaceListTimer = setTimeout(function(){loadInterfaceList()},100 * 1);
                loadInterfaceList();
                
            });
            
            mainMenuItem.find('>li.addInterface').delegate('li','click', function(evt){
                Ncm.Menus.hide();
                var ifInfo = $(this).data('ifInfo');
                Ncm.Menus.addInterface({id: ifInfo._id,label:{text: ifInfo.title}});
            });


            mainMenuItem.find('>li.setSize').delegate('li','click', function(evt){
                //Ncm.Menus.hide();
                var sizeStr = $(this).text();
                /\s*(\d+)\s*\*\s*(\d+)\s*/.test(sizeStr);
                var size = {w: RegExp.$1 * 1, h: RegExp.$2 * 1};
                Ncm.Menus.setSize(size);
            });



        },

        /**
         * 初始画布菜单
         */
        _initCanvasMenuItems: function(){
            var mainMenuItem =  $('#custom_map_menus .mainMenu.canvas');
            //--------------------------------------------------------------------//
			mainMenuItem.find('>li.addDevice').bind('mouseover', function(evt){
                
			    if(evt.target != this){clearTimeout(this._loadDeviceListTimer); return;}
				clearTimeout(this._loadDeviceListTimer);
				var addDeviceLi = this;
				var getExistDevIds = function(){
					var rs = [];
					for(var uid in Ncm.core.components){
						var cmo = Ncm.core.components[uid];
						if(! (cmo instanceof Ncm.CustomMapObjDev))  continue;
						if(cmo.cnf.id) rs.push(cmo.cnf.id);
						
					}
					//console.info(rs);
					return rs;
				};
				
				var loadDeviceList = function(){
                    
    				var deviceListUl = $(addDeviceLi).children('ul:first').html('loading...');
                    //var url = "/media/customMap/data/devList.json";
                    nb.rpc.customerMapViews.c("map_listMos", {}).success(function(devices){
        			    deviceListUl.html('');
        			    var ids = getExistDevIds();
                        $.each(devices, function(i, dev){
                            
                        	if($.inArray(dev._id, ids) >=0) return;
                            var li = $(Raphael.format('<li>{0}<span style="color:#AAA;">{1}</span></li>', dev.manageIp, (dev.title == dev.manageIp ? '' : "(" + dev.title + ")" )));
                            li.appendTo(deviceListUl);
                            li.data('devInfo', dev);
                                      
                        })//end each    
                    });
				};
				
				if(! this._loadDeviceListTimer) loadDeviceList();
				this._loadDeviceListTimer = setTimeout(function(){loadDeviceList()},10 * 1);
				//loadDeviceList();
				
			});
			
			
            mainMenuItem.find('>li.addLocation').bind('mouseover', function(evt){
                if(evt.target != this){clearTimeout(this._loadLocationListTimer); return;}
                clearTimeout(this._loadLocationListTimer);
                var addLocationLi = this;
                var getExistLocIds = function(){
                    var rs = [];
                    for(var uid in Ncm.core.components){
                        var cmo = Ncm.core.components[uid];
                        if(! (cmo instanceof Ncm.CustomMapObjLoc))  continue;
                        if(cmo.cnf.id) rs.push(cmo.cnf.id);
                        
                    }
                    //console.info(rs);
                    return rs;
                };
                
                var loadLocationList = function(){
                    var locationListUl = $(addLocationLi).children('ul:first').html('loading...');
                    //var url = "/media/customMap/data/getLocations.json";
                    nb.rpc.customerMapViews.c("map_listSubLocs", {orgUid:window.orgUid}).success(function(locations){
                        locationListUl.html('');
                        var ids = getExistLocIds();
                        $.each(locations, function(i, loc){
                            
                            if($.inArray(loc._id, ids) >=0) return;
                            var li = $(Raphael.format('<li>{0}</li>', loc.title));
                            li.appendTo(locationListUl);
                            li.data('locInfo',loc);
                                      
                        })//end each    
                    });
                };
                
                if(! this._loadLocationListTimer) loadLocationList();
                this._loadLocationListTimer = setTimeout(function(){loadLocationList()},10 * 1);
                
                
            });
			
			 //--------------------------------------------------------------------//
			
            mainMenuItem.find('>li.addDevice').delegate('li','click', function(evt){
                var devInfo = $(this).data('devInfo');
                var mp = Ncm.Menus._mp;
                Ncm.Menus.addDevice({p:{x:mp.x-20, y:mp.y-20}, label:{text: devInfo.title}, id: devInfo._id, moType:devInfo.moType});
                Ncm.Menus.hide();
                $(this).remove();
            });

            mainMenuItem.find('>li.addLocation').delegate('li','click', function(evt){
                var locInfo = $(this).data('locInfo');
                var mp = Ncm.Menus._mp;
                Ncm.Menus.addLocation({p:{x:mp.x-20, y:mp.y-20}, label:{text: locInfo.title}, id: locInfo._id});
                Ncm.Menus.hide();
            });


            mainMenuItem.find('>li.addVirtualNode').bind('click', function(evt){
                //console.info('addVirtualNode');
                var mp = Ncm.Menus._mp;
                Ncm.Menus.addVirtualNode({p:{x:mp.x-20, y:mp.y-20}, label:{text: '未命名虚对象'}});
                Ncm.Menus.hide();
            });

            mainMenuItem.find('>li.setCanvasSize').bind('click', function(evt){
                Ncm.Menus.hide();
                var sizeStr = prompt('画布尺寸, 宽度 800~1600 , 高度 600~2000',  Ncm.core.size.w + ',' + Ncm.core.size.h);
                var exp = /^\s*(\d+)\s*,\s*(\d+)\s*$/;
                if(! (sizeStr &&  exp.test(sizeStr))) return;

                var size = {w: RegExp.$1 * 1, h: RegExp.$2 * 1};
                if(size.w > 1600 || size.w < 800 || size.h < 600 || size.h > 2000){
                    return;
                }
                Ncm.Menus.setCanvasSize(size);



            });

            
            mainMenuItem.find('>li.setBgImg').delegate('li', 'click', function(evt){
                Ncm.Menus.hide();
                var img = $(this).text();
                if(img == 'None') img = 'default.png';
                Ncm.Menus.setBgImg(img);
                
            });
            
            


        },
        initMenuItemEvents : function(){
            this._initCmoMenuItems();
            this._initCanvasMenuItems();
            getCanvasContiner().bind('click', function(){Ncm.Menus.hide();});
            getCanvasContiner().bind('mouseup', function(evt){
                //console.info('popupCanvasMenu',evt);
                if(!(evt.buttons == 2 || evt.button == 2)){
                    return ;
                }
                
                if(!(evt.target == getPager().canvas || evt.target == this || evt.target == Ncm.core.backgroundImg.node)){ //this is div#canvas_continer
                    return ;
                }
                //console.info('popupCanvasMenu');
                Ncm.Menus.popupCanvasMenu(evt);

            });



        }

    };

	
    
    var loadIcons = function(){
        var url = "/media/customMap/data/getIcons.json";
        
        $.post(url, {}, function(icons){
            var iconsDiv = $("#custom_map_cmo_icons");
            var _fillImgs = function(xtype, xtype2){
                $.each(icons[xtype], function(i, icon){
                    var html = Raphael.format('<div><img width="60px" src="{2}icons/{1}/{0}" /></div>', icon, xtype2, skinDir)
                    iconsDiv.find(">." + xtype).append(html);
                });
            };
            
            _fillImgs("device","dev");
            _fillImgs("location","loc");
            _fillImgs("virtual","vir");

        },"json");
        
        $('#custom_map_cmo_icons').delegate('img', 'click', function(evt){
            var src = $(this).attr('src');
            if(/([^/]+\.(png|jpg|bpm))\s*$/gi.test(src)){
                var icon = RegExp.$1;
                Ncm.Menus.setIcon(icon);
            }
            

        });
    
    };
    
    var saveToServer = Ncm.utils.DelayTaskMrg.createTask("saveToServer", function(){
    	var mapData = jQuery.parseJSON(Ncm.core.serialize());
        nb.rpc.customerMapViews.c("map_savemapData", {mcUid:window.mcUid, mapData:mapData}).success(function(msg){
        	nb.AlertTip.auto(msg);
        });
    })
    
    var loadMap=function(){
    
    	nb.rpc.customerMapViews.c("map_getMapData", {mcUid:window.mcUid}).success(function(mapData){
        	Ncm.core.loadFromJson(mapData);
        });
    };
    
    Ncm.on("afterChange", function(){
       saveToServer.run(1000);
    });
    
    $(document).ready(function(){
    	loadMap();
        loadIcons();
        Ncm.Menus.initMenuItemEvents();   
        
    });
    
	
})();