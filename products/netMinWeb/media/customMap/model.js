(function(){
    
    
    var  Ncm = window.Ncm || {};
    var $ = jQuery;
    
    var skinDir = "/media/customMap/skins/";
    
    var getPager = function(){return Ncm.core.paper;};
    

    /**
     * 矩形框DragDrop事件处理
     */
    var boxRectDragHandlers = {
        dragger : function (x, y, evt) {
            //console.info(evt.buttons, evt.button);
            if(evt.buttons == 2 || evt.button == 2){
                // mouse move 时，IE不支持右键判断,所以__evt_button__做记录
                this.__evt_button__ = 2; return false;
            }

            this.__dragStatus = 'start';
            this.ox = this.type == "rect" ? this.attr("x") : this.attr("cx");
            this.oy = this.type == "rect" ? this.attr("y") : this.attr("cy");
            this.animate({"fill-opacity": .2}, 500);


        },

        move : function (dx, dy, x, y, evt) {
            if(this.__evt_button__ == 2) return false;
            if(this.__dragStatus == 'start'){
                this._cmo.fireEvent('dragStart');
                this.__dragStatus = 'moveing';
            }
            this.__dragStatus = 'moveing';
            //console.info('moveing...');
            this.node.style.cursor = 'move';
            var p = {x: this.ox + dx, y: this.oy + dy};

            this._cmo.fireEvent('dragMove',p.x, p.y);
            for (var i = 0; i < Ncm.core.connections.length; i++) {
                Ncm.utils.connection2(Ncm.core.connections[i]);
            }
            getPager().safari();

        },

        up : function (evt) {
            delete this.__evt_button__;
            this.animate({"fill-opacity": 0}, 500);
            this.node.style.cursor = '';
            if(this.__dragStatus == 'moveing'){
                this._cmo.fireEvent('dragEnd');
            }
            this.__dragStatus == 'end';
            delete this.__dragStatus;

        }
    }
    

    
    

    /**
     * Custom Map 对象基类
     */
    var CustomMapObj = Ncm.CustomMapObj =  function(options){
        Ncm.Observer.call(this);
        //this.toString = function(){return this.cnf.className + ':' + this.cnf.id};
        this._getIconPath = function(icon){ //if not icon, return base path
            throw new Error('_getIconPath must be overwrite.');
        };

        /**
         * 创建、渲染UI， 触发afterCreateUI事件
         */
        this.createUI = function(){
            var cnf = this.cnf;
            var uiSet = this.uiSet = getPager().set(); //ui集
            var boxRect = this.boxRect = getPager().rect(cnf.p.x, cnf.p.y, cnf.p.w, cnf.p.h, 10); //主矩形框
            boxRect.attr({"fill-opacity": 0, fill:'#8C1C1C', stroke:'#fff', 'stroke-width':0});
            boxRect.drag(boxRectDragHandlers.move, boxRectDragHandlers.dragger, boxRectDragHandlers.up);
            boxRect._cmo = this;
            boxRect.node._cmo = this;

            var iconImg = this.iconImg = getPager().image(this._getIconPath(cnf.icon), cnf.p.x, cnf.p.y, cnf.p.w, cnf.p.h); //图标
            iconImg.insertBefore(boxRect);

            var labelTextUI = this.labelTextUI = getPager().text(cnf.p.x, cnf.p.y, cnf.label.text); //文本标签
            this.setLabel(null, cnf.label.dir, cnf.label.size);

            uiSet.push(iconImg);
            uiSet.push(boxRect);
            uiSet.push(labelTextUI);

            this._afterCreateUI(boxRect, iconImg, labelTextUI, uiSet); //扩展UI组件
            this.fireEvent('afterCreateUI'); //触发渲染结束事件
        };
        
        /**
         * 子类实现此方法，用于扩展UI组件
         */
        this._afterCreateUI = function(boxRect, iconImg, labelTextUI, uiSet){
            
        };
        
        /** 取消Drag功能 */
        this.undrag = function(){
            this.boxRect.undrag();
        };
        
        /** 获取中心点坐标 */
        this.getCenterPonit = function(){
            var bb2 = this.boxRect.getBBox();
            return {x: bb2.x + bb2.width / 2, y: bb2.y + bb2.height/2};
        };
        
        /** 获取主矩形框在uiSet中的下标 */
        this._getBoxRectIndex = function(){
            for(var i = 0; i < this.uiSet.length; i++){
                if(this.uiSet[i] == this.boxRect) return i;
            }
            return -1;
        };
        
        /**
         * 设置图标
         * @param {String} icon 图标文件名
         */
        this.setIcon = function(icon){
            this.iconImg.attr({src: this._getIconPath() + icon});
            this.cnf.icon = icon;
        };
        
        /**
         * 设置状态
         * @param {String} status
         */
        this.setStatus = function(status){ 
            this.statusImg.attr({'src':  skinDir + 'icons/status/' + status+'.png'});
            this.status = status;

        };
        
         /**
          * 设置尺寸
          * @param {object} size   size.w=宽度, size.h=高度
          * @param {boolean} an 是否启用动画功能
          * @param {Function} callback 动画执行结束后的回调
          */
        this.setSize = function(size, an, callback){
            var attrs = {width: size.w, height: size.h};
            var self = this;
            if(an){
                var anTime = 100;
                this.boxRect.animate(attrs, anTime,callback);
                this.iconImg.animate(attrs, anTime, function(){
                    self.setLabel(null, self.cnf.label.dir);
                });
            }
            else{
                this.boxRect.attr({width: size.w, height: size.h});
                this.iconImg.attr({width: size.w, height: size.h});
                this.setLabel(null, this.cnf.label.dir);
            }

            this.cnf.p.w = size.w;
            this.cnf.p.h = size.h;
        };
        
        /**
         * 移动至某坐标点
         * @param {Number} x 坐标点
         * @param {Number} y 坐标点
         */
        this.move2 = function(x,y){
            this.cnf.p.x = x; this.cnf.p.y = y;
            this.boxRect.attr({x: x, y: y});
            this.iconImg.attr({x: x, y: y});
            if(this.statusImg) this.statusImg.attr({x: x, y: y});
            this.setLabel(null, this.cnf.label.dir);
        };
        this._insertBeforeRectFgPath = function(){
            this.uiSet.insertBefore(Ncm.core.__rectFgPath);
        };

        /**
         * 绑定对象的Drag相关事件
         */
        this._bindDragEvents = function(){
            if(Ncm.viewfor == "BrowseMode") return;
            this.on('dragMove', function(x, y){
                if(x >= Ncm.core.size.w - this.cnf.p.w/3 || x <= 0) return;
                if(y >= Ncm.core.size.h - this.cnf.p.h/3 || y <= 0) return;

                if(this.ifArray){

                    for(var i = 0; i < this.ifArray.length; i++){
                        var ifObj = this.ifArray[i];
                        var ifp = {x: x + ifObj.cnf.p.x - this.cnf.p.x , y: y + ifObj.cnf.p.y - this.cnf.p.y };
                        ifObj.move2(ifp.x, ifp.y);
                    }
                }
                this.move2(x,y);

            });

            this.on('dragStart', function(){
                this._insertBeforeRectFgPath();
                Ncm.fireEvent('beforeChange', this.cnf.uid + 'dragStart');
            });
            this.on('dragEnd', function(){
                Ncm.fireEvent('afterChange');
            });



        };

        /**
         * 绑定其它的一些事件
         * @note 绑定右键弹出事件(popupMenu)
         */
        this._bindOtherEvents = function(){
            this.on('afterCreateUI', function(){
                var self = this;
                this._insertBeforeRectFgPath();

                //right mouse down? right button return true, else return false
                var stopEvtPropagation = function(evt){
                    if(evt.buttons == 2 || evt.button == 2){
                        evt.cancelBubble = true;
                        evt.returnValue  = false;
                        if(evt.stopPropagation) evt.stopPropagation();
                        return true;
                    }
                    return false;
                };
                if(Ncm.viewfor != "BrowseMode"){
                    this.boxRect.mouseup(function(evt){
                        var isRightButton = stopEvtPropagation(evt);
                        if(!isRightButton) return false;
                        self.fireEvent('popupMenu', evt); //绑定popupMenu事件，创建或打开右键菜单

                    });
                    
                }
                
                
                if(Ncm.viewfor == "BrowseMode"){
                	
                    this.boxRect.dblclick(function(evt){
                    	self.fireEvent('dblclick', evt);
                    });            
                	
                	this.boxRect.hover(function(evt){
                    	self.fireEvent('showTip', evt);
                    }); 
                }
            });

            this.on('popupMenu', function(evt){
                Ncm.Menus.popupCmoMenu(this, evt);
            });
            
            this.on('dblclick', function(evt){
                Ncm.Viewer.pageTo(this, evt);
            });
            
            this.on('showTip', function(evt){
                Ncm.Viewer.showTip(this, evt);
            });
            
            
        };

        /**
         *  连接至另一个对象
         *  @param {CustomMapObj} 
         *  @return {object|boolean} 如果两对象之无法连接，返回false，否则返回一个连接对象
         */
        this.conn2 = function(cmo){
            if(!cmo || cmo == this) return false;
            if(cmo.parentCmo && cmo.parentCmo == this) return false;
            if(this.parentCmo && this.parentCmo == cmo) return false;
            if(this.parentCmo && cmo.parentCmo && this.parentCmo == cmo.parentCmo) return false;

            for(var i = 0; i < Ncm.core.connections.length; i++){
                var conn = Ncm.core.connections[i];
                if((this == conn.from || this == conn.to) && (cmo == conn.from || cmo == conn.to)){
                    return false;
                }
            }
            var conn = Ncm.utils.connection2(this, cmo);
            Ncm.core.connections.push(conn);
            return conn;
        };

        /**
         * 设置标签
         * @param {String} text
         * @param {String} dir 方向、位置,可选参数top|left_top|right_top|left|left_bottom|right_bottom|right|bottom|center
         * @param {String} size  如12px, 14px, ....
         * @note 参数为null, 则不设置该项
         */
        this.setLabel = function(text, dir, size){
            var self = this;
            if(text){
                this.labelTextUI.attr('text', text);
                this.cnf.label.text = text;
            }

            var getLabelPs = function(){
                var bb1 = self.labelTextUI.getBBox();
                var bb2 = self.boxRect.getBBox();
                var ps = {
                    top: {x: bb2.x + bb2.width / 2 , y: bb2.y - bb1.height / 2},
                    left_top: {x: bb2.x, y: bb2.y - bb1.height / 2},
                    right_top: {x: bb2.x + bb2.width, y: bb2.y - bb1.height / 2},
                    left:{x: bb2.x - bb1.width / 2, y: bb2.y + bb2.height / 2},

                    left_bottom:{x: bb2.x, y: bb2.y + bb2.height + bb1.height/2},
                    right_bottom:{x: bb2.x+bb2.width, y: bb2.y + bb2.height + bb1.height/2},
                    right:{x: bb2.x + bb2.width + bb1.width / 2, y: bb2.y + bb2.height / 2},
                    bottom: {x: bb2.x + bb2.width / 2 , y:bb2.y + bb2.height + bb1.height/2},
                    center: {x: bb2.x + bb2.width / 2 , y:bb2.y + bb2.height / 2}
                };

                return ps;
            };

            if(size){
                this.labelTextUI.attr('font-size', size);
                this.cnf.label.size = size;
                var ps = getLabelPs();
                this.labelTextUI.attr(ps[this.cnf.label.dir]);
            }
            if(dir){
                var ps = getLabelPs();
                this.labelTextUI.attr(ps[dir]);
                this.cnf.label.dir = dir;
            }

        };

        /**
         * 删除连接线
         */
        this.removeLines = function(){
            var conns = Ncm.core.connections;
            for(var i = conns.length - 1; i >= 0; i--){
                var conn = conns[i];
                if(this == conn.to || conn.from == this){
                    //console.info('find ', i);
                    conn.line.remove();
                    conns.splice(i,1);
                }
            }
        };

        this.remove = function(){
            this.removeLines();
            this.uiSet.remove();
            Ncm.fireEvent('removeComponent', this.cnf.uid, this);
        };

        this.__init__ = function(options){
            var cnf = {
                p: {x:0, y: 0, w: 100, h: 100},
                icon:'default.png',
                label: {
                    text: 'None text', dir: 'left_top', size: '12px'
                }
            };

            //console.info('CustomMapObj.__init__');
            this.cnf = $.extend(true, cnf, options);
            this.cnf.className = 'CustomMapObj';
                       
            this._bindDragEvents();
            this._bindOtherEvents();
            //Ncm.components[this.cnf.uid] = this;
            //Ncm.fireEvent("initMapObj", this);
        };

        this.__init__(options);
    };

    /**
     * 生成唯一ID
     */
    CustomMapObj.createUid = function(cmo){       
        return  cmo.cnf.className + "_" + (cmo.cnf.id || new Date().getTime());
    };

    /**
     * 设备类
     */
    var CustomMapObjDev = Ncm.CustomMapObjDev = function(options){
        CustomMapObj.call(this, options);
        this._getIconPath = function(icon){
            if(!icon) return skinDir+"icons/dev/";
            return skinDir+"icons/dev/" + (icon || 'default.png');
        };
        
        /**
         * 扩展状态及接口UI
         */
        this._afterCreateUI = function(boxRect, iconImg, labelTextUI, uiSet){
            //console.info(this);
            if(!this.statusImg){
                this.statusImg = getPager().image(skinDir +  "icons/status/default.png", 
                                    this.cnf.p.x, this.cnf.p.y, 30, 30);
                this.statusImg.insertBefore(this.boxRect);
                var index = this._getBoxRectIndex();
                this.uiSet.splice(index, 0, this.statusImg);
            }
            this.ifset = getPager().set();
            this.uiSet.push(this.ifset);
            this.ifArray = [];
            
        };
        
        /**
         * 添加接口
         * @param {object} options
         */
        this.addInterface = function(options){
            var bb2 = this.boxRect.getBBox();
            var ifp = {x: bb2.x + bb2.width, y: bb2.y};
            var ifOptions = {p: ifp};
            $.extend(true, ifOptions, options);
            var ifObj = new CustomMapObjIf(ifOptions);
            ifObj.createUI();
            ifObj.parentCmo =  this;
            ifObj.cnf.parentUid = this.cnf.uid;
            this.ifset.push(ifObj.uiSet);
            this.ifArray.push(ifObj);

        };

        /**
         * 删除接口
         */
        this.removeInterfaces = function(ifCmo){
            for(var i = this.ifArray.length-1; i >= 0; i--){
                var tIfCom = this.ifArray[i];
                if(!ifCmo){
                    this.ifArray.splice(i,1)[0].remove(1);
                }
                else if(tIfCom == ifCmo){
                    this.ifArray.splice(i,1)[0].remove(1);
                    return;
                }

            }
        };
        
        /**
         * 删除
         */
        this.remove = function(){
            this.removeInterfaces();
            this.removeLines();
            this.uiSet.remove();
            Ncm.fireEvent('removeComponent', this.cnf.uid, this);
        };

        this.__init__  = function(options){
            var cnf = {
                p: {w: 100, h: 100}
            };

            $.extend(true, this.cnf, cnf, options);
            this.cnf.className = 'CustomMapObjDev';
            if(!this.cnf.uid) this.cnf.uid = CustomMapObj.createUid(this);
            Ncm.fireEvent("initMapObj", this);
        };

        this.__init__(options);
    }


    /**
     * 接口类
     */
    var CustomMapObjIf = Ncm.CustomMapObjIf = function(options){
        CustomMapObj.call(this, options);

        this._getIconPath = function(icon){
            if(!icon) return skinDir + "icons/if/";
            return skinDir + "icons/if/" + (icon || 'default.png');
        };
        /**
         * 删除接口
         * @param {Boolean} fg 为true, 则保留它在设备接口列表(ifArray)中的引用,默认false
         * 或者说它已经在接口列表中移除，不必再重复执行移除行为
         */
        this.remove = function(fg){
            this.removeLines();
            this.uiSet.remove();
            if((!fg) && this.parentCmo){
                var devCmo = this.parentCmo;
                for(var i = devCmo.ifArray.length-1; i >= 0; i--){
                    if(this == devCmo.ifArray[i]){
                        devCmo.ifArray.splice(i,1);
                        break;
                    }
                }
            }
            Ncm.fireEvent('removeComponent', this.cnf.uid, this);
        };

        /**
         * 设置状态
         */
        this.setStatus = function(status){
            this.iconImg.attr({'src':  skinDir + 'icons/status/if_' + status + '.png'});
            this.status = status;
            
        };

        this.__init__  = function(options){
            var cnf = {
                p: {x: 0, y: 0, w: 24, h: 24},
                icon:'if.png',
                label:{text: 'eth0', dir: 'right'}
            };

            $.extend(true, this.cnf, cnf, options);
            this.cnf.className = 'CustomMapObjIf';
            if(!this.cnf.uid) this.cnf.uid = CustomMapObj.createUid(this);
            Ncm.fireEvent("initMapObj", this);
        };

        this.__init__(options);
    };

    /**
     * 位置类
     */
    var CustomMapObjLoc = Ncm.CustomMapObjLoc = function(options){
        CustomMapObj.call(this, options);
        this._getIconPath = function(icon){
            if(!icon) return skinDir + "icons/loc/";
            return skinDir + "icons/loc/" + (icon || 'default.png');
        };
        
        /**
         * 扩展状态UI
         */
        this._afterCreateUI = function(boxRect, iconImg, labelTextUI, uiSet){
            if(!this.statusImg){
                this.statusImg = getPager().image(skinDir+"icons/status/default.png", 
                                    this.cnf.p.x, this.cnf.p.y, 30, 30);
                this.statusImg.insertBefore(this.boxRect);
                var index = this._getBoxRectIndex();
                this.uiSet.splice(index, 0, this.statusImg);
            }
            

        };
        this.__init__  = function(options){
            this.cnf.className = 'CustomMapObjLoc';
            if(!this.cnf.uid) this.cnf.uid = CustomMapObj.createUid(this);
            Ncm.fireEvent("initMapObj", this);
        };

        this.__init__(options);
    };

    /**
     * 虚点类
     */
    var CustomMapObjVir = Ncm.CustomMapObjVir = function(options){
        CustomMapObj.call(this, options);
        this._getIconPath = function(icon){
            if(!icon) return skinDir + "icons/vir/";
            return skinDir + "icons/vir/" + (icon || 'default.png');
        };
        
        /**
         * 扩展状态UI
         */
        this._afterCreateUI = function(boxRect, iconImg, labelTextUI, uiSet){
            if(!this.statusImg){
                this.statusImg = getPager().image(skinDir + "icons/status/default.png", 
                                    this.cnf.p.x, this.cnf.p.y, 30, 30);
                this.statusImg.insertBefore(this.boxRect);
                var index = this._getBoxRectIndex();
                this.uiSet.splice(index, 0, this.statusImg);
            }
            

        };

        this.__init__  = function(options){
            $.extend(true, this.cnf, {}, options);
            this.cnf.className = 'CustomMapObjVir';
            if(!this.cnf.uid) this.cnf.uid = CustomMapObj.createUid(this);
            Ncm.fireEvent("initMapObj", this);
        };

        this.__init__(options);
    };





})();