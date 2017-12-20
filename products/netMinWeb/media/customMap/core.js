(function(){
	var $ = jQuery;
    
    
    var canvasContinerId =  "canvas_continer";
    var skinDir = "/media/customMap/skins/";
    var defaultSize = {w:1000, h:600};
    var Ncm = window.Ncm = {};
    
    var Observer = Ncm.Observer = function(){
        this.events = {};
        
        /** 触发事件  */
        this.fireEvent = function(eName){
            var events = this.events[eName];
            if(! events) return;

            var handlerArguments = [];
            for(var i = 1; i < arguments.length; i++){
                handlerArguments.push(arguments[i]);
            }

            for(var i = 0; i < events.length; i++){
                var event = events[i];
                event.handler.apply(event.scope || this, handlerArguments);
            }

        };
        
        /** 事件绑定 */
        this.on = function(eName, handler, scope){
            if(!this.events[eName])  this.events[eName] = [];
            this.events[eName].push({handler: handler, scope: scope});
        };

        /** 取消事件，如果handler不存在，取消所有事件 */
        this.un = function(eName, handler){
            var events = this.events[eName];
            if(!events || events.length == 0) return;
            if(events && !handler){
                events.splice(0, events.length);
                return;
            }
            

            for(var i = events.length - 1; i >= 0; i--){
                if(events[i].handler == handler) events.splice(i,1);
            }
        }
    };
    $.extend(Ncm, new Observer());
    Ncm.core = $.extend({
        size: {w: defaultSize.w, h: defaultSize.h},
        bg: {img: 'default.png'},
        components:{},
        connections : [],
        
        /** 设置宽度、高度 */
        setSize: function(w,h){
            Ncm.core.paper.setSize(w, h);
            $("#"+canvasContinerId).width(w).height(h);
            this.size.w = w;
            this.size.h = h;
            this.backgroundImg.attr({width:w, height:h});
            this.fireEvent('afterResize');
            
        },
        /** 设置背景图 */
        setBgImg: function(img){
            this.backgroundImg.attr({src: skinDir + 'background/'+img});
            this.bg.img = img;
        },
        
        /** 
         *  序列化Custom Map 
         *  @return {String}
         */
        serialize: function(){
            var components = {};
            for(var uid in this.components){
                var cmoCnf = this.components[uid].cnf;
                components[uid] = cmoCnf;
            }

            var connections = [];
            for(var i = 0; i < this.connections.length; i++){
                var conn = this.connections[i];
                var xconn = {from: conn.from.cnf.uid, to: conn.to.cnf.uid};
                connections.push(xconn);
            }
            //return $.toJSON(connections);

            return window.JSON.stringify({
                bg:{img: Ncm.core.bg.img},
                size: Ncm.core.size,
                components: components,
                connections: connections
            });

        },

        /** 加载图像
         * @param {String|object} json
         */
        loadFromJson: function(json){
            var data = json;
            for(var uid in data.components){
                var createCmo = function(cnf){
                    if(Ncm.core.components[cnf.uid]) return Ncm.core.components[cnf.uid];
                    var xClass = Ncm[cnf.className];
                    var cmo = new xClass(cnf);
                    cmo.createUI();
                    //console.info('uid:'+ cnf.uid);
                    return cmo;
                };

                var cnf = data.components[uid];

                if(cnf.parentUid){
                    var parentCmo = createCmo(data.components[cnf.parentUid]);
                    parentCmo.addInterface(cnf);
                    continue;
                }
                createCmo(cnf);
            }
            
            if(data.connections){
                $.each(data.connections, function(i, xconn){
                    var cmo1 = Ncm.core.components[xconn.from];
                    var cmo2 = Ncm.core.components[xconn.to];
                    var conn = Ncm.utils.connection2(cmo1, cmo2);
                    Ncm.core.connections.push(conn);
                
                });
                
            }
            
            if(data.size) Ncm.core.setSize(data.size.w, data.size.h);
            if(data.bg) Ncm.core.setBgImg(data.bg.img);
        },
        
        /** 消除图像 */
        clearMap: function(){
            for(var uid in Ncm.components){
                var cmo = Ncm.components[uid];
                if(! cmo) continue;
                cmo.remove();
            }
        },
        

        
        __init__: function(){
            //canvasContiner = $('#' + canvasContinerId);
            var paper =  Raphael(canvasContinerId, defaultSize.w, defaultSize.h);
            this.paper = paper;
            
            this.backgroundImg = paper.image(skinDir + 'background/default.png', 0, 0, defaultSize.w, defaultSize.h);
            
            this.__backgroundFgPath = paper.path([['M',0,0],['L',0,0]]);
            this.__firstFgPath = paper.path('M0,0L0,0');
            this.__rectFgPath= paper.path('M1,1L1,1');
            
        }        
    
    
    }, new Observer());
    
    
    
    
    
    Ncm.on("initMapObj", function(mapObj){
        Ncm.core.components[mapObj.cnf.uid] = mapObj;
        
    });
    
    Ncm.on("removeComponent", function(uid, cmo){
        delete Ncm.core.components[uid];
    });
    
    $(document).ready(function(){
        Ncm.core.__init__();
    
    });


})();