

window.NbHelpTips = {
    'help':'\
WIN7用户下载文件后如无法查看，请点<br/> \
击文件右键"属性"-->点击"解除锁定"',
    
   '001':' \
设备状态说明:<br/> \
<span class="status-icon-small up"></span> 状态正常  <br> \
<span class="status-icon-small down"></span> 状态异常/宕机  <br> \
<span class="status-icon-small unknown"></span> 状态未知    <br> \
<p> \
设备的状态，来源于后台Ping进程（每20秒，作为循环周期）获取，<br> \
出现"未知状态",是Ping进程暂时未收集到设备的相关状态数据，请稍后几分钟刷新组件 <br> \
</p> \
 <br/><br/>\
Cpu与内存利用率计算说明: <br/> \
1. CPU利用率公式 Cpu=100-空闲Cpu <br/> \
2. 内存利用率公式 Mem=100-(可用内存/总内存) ',


    '002':' \
设备产生的相关事件，如设备内存、CPU超过最大的设定的阀值,设备宕机。<br> \
    <span class="severity-icon-small Info"></span> 代表消息事件<br> \
    <span class="severity-icon-small Warning"></span> 代表警告事件<br> \
    <span class="severity-icon-small Error"></span> 代表错误事件<br> \
    <span class="severity-icon-small Critical"></span> 代表严重事件<br> ',  
   
    '003':'\
&nbsp;&nbsp;&nbsp;&nbsp;显示设备的CPU与内存的性能趋势图，用户可以根据需要，在右上角选择相应的时间段<span style="color:red">(天，周，月)</span>。\
后台对于主机设备是每60秒轮询一次，然后得到一个数据。用户设备宕机时，性能数据线条是截断。如果用户想了解某一时间段的性能信息，可以拖动最下方两边的时间条。',
   
    '004':'\
显示设备磁盘的基本信息，如名称，容量、使用容量。只有用户在对应的设备配置页面上手动添加磁盘时，这个组件才会显示数据。',
    
    '005':'\
显示设备<span style="color:red">(tcp|udp)</span>类型的端口状态，只有用户在对应的设备配置页面上手动添加服务时，这个组件才会显示数据。',
    
    '006':'\
显示设备CPU温度基本信息，依赖IPMI设置。<span style="color:red">只有用户在设备配置页面正确配置了IPMI并启动IPMI</span>。然后添加了温度组件，该框才会有数据显示。',
    
    '007':'\
显示设备CPU温度趋势图，只有用户在设备配置页面上手动添加了CPU温度功能，该框才会显示图像。后台对于主机设备是每5分钟轮询一次，然后得到一个数据。用户设备宕机时，性能数据线条是截断。\
如果用户想了解某一时间段的性能信息，可以拖动最下方两边的时间条。',
    
    '008':'\
显示设备相应的接口的基本信息，如流入流量、流出流量，接口名称、接口所在的主机IP地址等。只有用户在设备配置页面手动添加接口，该框才会有数据显示。',
    
    '009':'\
显示设备已添加的接口性能趋势图，只有用户在设备配置页面上手动添加了接口，该框才会显示图像.后台对于主机设备是每60秒轮询一次，然后得到一个数据。用户设备宕机时，性能数据线条是截断。\
如果用户想了解某一时间段的性能信息，可以拖动最下方两边的时间条。',
    
    '010':'\
显示设备已添加的进程的基本信息，只有用户在设备配置页面上手动添加了进程，该框才会显示数据。',
   
    '011':'\
显示设备的进程所占用的CUP与内存的性能趋势图，只有用户在设备配置页面上手动添加了进程，该框才会显示图像.后台对于主机设备是每60秒轮询一次，然后得到一个数据。用户设备宕机时，\
性能数据线条是截断。如果用户想了解某一时间段的性能信息，可以拖动最下方两边的时间条。',
   
    '012':'\
显示设备已添加的风扇的基本信息，只有用户在设备配置页面上手动添加了风扇，该框才会显示数据。',
    
    '013':'\
显示设备的风扇所占用的CUP与内存的性能趋势图，只有用户在设备配置页面上手动添加了风扇，该框才会显示图像.后台对于主机设备是每60秒轮询一次，然后得到一个数据。用户设备宕机时，\
性能数据线条是截断。如果用户想了解某一时间段的性能信息，可以拖动最下方两边的时间条。',
    
    'dev_base':'\
列出设备的基本信息，如设备标题、管理IP(创建后不能更改)、设备的描述',
    
    'dev_snmp':'\
SNMP介绍：<br>\
&nbsp;&nbsp;&nbsp;&nbsp;SNMP(Simple Network Management Protocol,简单网络管理协议)的前身是简单网关\
监控协议(SGMP)，用来对通信线路进行管理。随后，人们对SGMP进行了很大的修改，特别是加入了符合Internet定义\
的SMI和MIB：体系结构，改进后的协议就是著名的SNMP。SNMP的目标是管理互联网Internet上众多厂家生产的软硬件平台，\
因此SNMP受Internet标准网络管理框架的影响也很大。现在SNMP已经出到第三个版本的协议，其功能较以前已经大大地加强和改进了。<br>\
&nbsp;&nbsp;&nbsp;&nbsp;更加详细信息，请<a href="http://baike.baidu.com/link?url=dmxO7_P21rj7X8aVWFAJD5NOPsd0xfG8RmARuodEF7kaLWrb-BGyrVZLAcbzeaHR" target="_blank" >点击</a><br>\
SNMP配置根据snmp版本的不同而不同,V3才有的配置参数：<br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">.Snmp私有密码</span><br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">.Snmp认证类型</span><br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">.Snmp私有类型</span><br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">.Snmp验证密码</span><br>\
  &nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">.Snmp安全名</span>',
    
    'dev_comm':'\
配置SSL相关信息。SSL采用公开密钥技术，保证两个应用间通信的保密性和可靠性，使客户与服务器应用之间的通信不被攻击者窃听。\
它在服务器和客户机两端可同时被支持，目前已成为互联网上保密通讯的工业标准。更加详细信息，请<a href="http://baike.baidu.com/link?url=ekC63ytm4f_v_t97g0LEYjiookxvYWUNaFtBfbHLBdWR2yQDSnpToxN7QngYcesz" target="_blank" >点击</a>',
    
    'dev_ipmi':'\
IPMI介绍： <br>\
&nbsp;&nbsp;&nbsp;&nbsp;智能平台管理接口 (IPMI) 是一种开放标准的硬件管理接口规格，定义了嵌入式管理子系统进行通信的特定方法. \
IPMI 信息通过基板管理控制器 (BMC)（位于 IPMI 规格的硬件组件上）进行交流。使用低级硬件智能管理而不使用操作系统进行管理，具有两个主要   \
优点： 首先，此配置允许进行带外服务器管理；其次，操作系统不必负担传输系统状态数据的任务。<br>\
字段介绍： <br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">是否开启IPMI:</span>配置设备是否开启IPMI，设备远程开机功能启动提前要启动IPMI<br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">IPMI地址:</span>配置IPMI所在的服务器地址，如果设备没有启动IPMI，该字段可以为空，如果填写该字段，必需写对格式<br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">IPMI端口:</span>配置IPMI所在的服务器相对的端口，如果设备没有启动IPMI，该字段可以为空，如果填写该字段，必需写对格式默认为80<br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">IPMI用户名:</span>配置连接设置有IPMI的服务器的用户名，如果设备没有启动IPMI，该字段可以为空<br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">IPMI密码:</span>配置连接设置有IPMI的服务器的用户名对应的密码，如果设备没有启动IPMI，该字段可以为空<br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">hcType类型：</span>IPMI工作方式，默认为ping方式',
    
    'bootpo_index':'\
能够使用开机助手的前提是用户在设备配置页面上正确配置并启动了IPMI。并在左上方的启动/关闭远程开机功能按钮的弹出框上启动设备的远程开机功能。远程开机视图有会显示该设备。当然，如果用户\
想关闭某设备的远程开机功能，可以点击左上方的启动/关闭远程开机功能按钮，在弹出的列表中，选择你想关闭的某个设备，然后去掉后面的勾。<br>\
<br>\
<span style="color:red">一键开机：</span> <br>\
&nbsp;&nbsp;&nbsp;&nbsp;能够使用一键开机功能的前提是用户配置了IPMI并启动IPMI。这个之前有说明过。一键开机也需要设备连通网络。也就是说，ping得通过。一键开机这个功能\
执行时间会花费一些时间，当用户点击一键开机按键，在弹出的选择框选择确定后，页面上会显示<span style="color:red">"正在发送远程命令，请稍后..."</span>，过了大概5分钟后\
如果显示<span style="color:red">"开机命令超时,请检查网络连接是否正常!"</span>,表示设备的网络可能有问题，请检查网络再做一键开机操作。 <br>\
如果显示<span style="color:red">"连接服务器地址错误:(显示一些错误信息)"</span>,表示设备配置的IPMI服务器地址有问题，请检查IPMI相关\
参数，再做一键开机操作。 <br>\
如果显示<span style="color:red">"连接服务器出错!"</span>,表示设备的IPMI配置或IPMI服务器有问题，请检查IPMI相关参数再做一键开机操作。 <br>\
如果显示<span style="color:red">"已经成功发送了远程操作命令!"</span>,表示netbase已经成功发送一键开机命令给设备了。<br>\
<br>\
<span style="color:red">一键关机：</span> <br>\
&nbsp;&nbsp;&nbsp;&nbsp;能够使用一键关机的功能提前要求和操作与上述介绍的一键开机一样，这里就不再介绍了。<br>\
<span style="color:red">一键硬关机：</span> <br>\
&nbsp;&nbsp;&nbsp;&nbsp;能够使用一键硬关机的功能提前要求和操作与上述介绍的一键开机一样，这里就不再介绍了。一键硬关机与一键关机的区别是一键硬关机是直接粗暴地断开电源 \
，关机时间相对比较快些，一键关机是使用文明的方法，等设备里所有的进程都关闭时，才断开电源。非紧急情况，推荐使用一键关机。<br>\
<span style="color:red">一键硬重启：</span> <br>\
&nbsp;&nbsp;&nbsp;&nbsp;一键硬重启，是直接断开电源再重启。能够使用一键硬重启的功能提前要求和操作与上述介绍的一键开机一样，这里就不再介绍了。',
    
    'shortcutCmdList_index':'\
<span style="color:red">快捷命令：</span> <br>\
快捷命令通过远程SSH发送命令给linux主机。快捷命令使用的前提是先通过主机配置页面，正确配置“通用配置”。<br>\
<span style="color:red">快捷命令的使用：</span><br>\
首先要说明，只有linux主机才可以使用快捷命令。其次，执行时间过长的命令，不建议直接使用，如长ping、top<br>\
<span style="color:red">创建命令：</span> 点击右上角的创建按钮，在弹出的窗口，填写你命令的名称(可任意)、命令。在设备列表里选择接收命令的远程设备。创建命令后，\
点击命令后面的执行操作按键，就可以执行你选择的命令了。在弹出的窗口，你可以看到，命令返回的结果。<br>\
<span style="color:red">编辑命令：</span>在命令列表里，选择你想要编辑的命令(每条命令的最左边有一个单选按钮，把它打上勾，就表示选择上这条命令)，然后点击右上角的\
编辑按钮，在弹出的命令编辑窗口里更改命令。<br>\
<span style="color:red">删除命令：</span>在命令列表里，选择你想要编辑的命令(每条命令的最左边有一个单选按钮，把它打上勾，就表示选择上这条命令)，然后点击右上角的\
删除按钮。',
    
    'dev_index_baseInfo':'\
设备状态说明:<br/> \
<span class="status-icon-small up"></span> 状态正常  <br> \
<span class="status-icon-small down"></span> 状态异常/宕机  <br> \
<span class="status-icon-small unknown"></span> 状态未知    <br> \
<p> \
设备的状态，来源于后台Ping进程（每20秒，作为循环周期）获取，<br> \
出现"未知状态",是Ping进程暂时未收集到设备的相关状态数据，请稍后几分钟刷新组件 <br> \
</p> \
 <br/><br/>\
Cpu与内存利用率计算说明: <br/> \
1. CPU利用率公式 Cpu=100-空闲Cpu <br/> \
2. 内存利用率公式 Mem=100-(可用内存/总内存)',
    
    'dev_index_newEvent':'\
列出当前设备列表的事件级别大于3的最新的前10条事件记录。通过事件列表，可以知道设备当前出现的情况，帮助用户尽早发现问题。<br> \
    <span class="severity-icon-small Info"></span> 代表消息事件<br> \
    <span class="severity-icon-small Warning"></span> 代表警告事件<br> \
    <span class="severity-icon-small Error"></span> 代表错误事件<br> \
    <span class="severity-icon-small Critical"></span> 代表严重事件<br> ',
    'dev_index_hostAvail':'\
一定时间段内无法连接次数最多主机前十名,当设备宕机时，该设备在这时间段的可以用性为0.用户可以根据需要，在右上角选择相应的时间\
段<span style="color:red">(天，周，月)</span>',
    
    'dev_index_interfaceAvail':'\
一定时间段内掉线次数最多,断线时间最长的接口前十名,当设备宕机时，该设备相应的接口在这时间段的可以用性也为0.用户可以根据需要，在右上角选择相应的时间\
段<span style="color:red">(天，周，月)</span>。当然，只用用户手动为设备列表添加接口时，该显示框才会有数据显示。',
   
    'dev_index_processAvail':'\
一定时间段内停止运行次数最多进程前十名,当设备宕机时，该设备相应的进程在这时间段的可以用性也为0.用户可以根据需要，在右上角选择相应的时间\
段<span style="color:red">(天，周，月)</span>。当然，只用用户手动为设备列表添加进程时，该显示框才会有数据显示。',
   
    'dev_index_serviceAvail':'\
一定时间段内连接不上次数最多的服务前十名,当设备宕机时，该设备相应的服务在这时间段的可以用性也为0.用户可以根据需要，在右上角选择相应的时间\
段<span style="color:red">(天，周，月)</span>。当然，只用用户手动为设备列表添加服务时，该显示框才会有数据显示。',
    
    'web_index_webAvail':'\
站点可用性：指的是站点在单位时间内正常运行的时间与单位时间的比率。反应站点连通性的高低。<br/>\
点击某个站点，展开各个检测点的详情 <br/></br/> \
\
<font style="color:red">(注:网脊科技会在全国各地布署多个服务器，通过不同的运营商检测站点的连通性、延时)</font>\
',


    'web_index_newEvent':'\
列出当前站点列表的事件级别大于3的最新的前10条事件记录。通过事件列表，可以知道站点当前出现的情况，帮助用户尽早发现问题。<br> \
    <span class="severity-icon-small Info"></span> 代表消息事件<br> \
    <span class="severity-icon-small Warning"></span> 代表警告事件<br> \
    <span class="severity-icon-small Error"></span> 代表错误事件<br> \
    <span class="severity-icon-small Critical"></span> 代表严重事件<br> ',
    'dev_index_ResponesTime':'\
站点的近一小时的平均响应时间，及当前响应时间(单位ms)<br>\
点击各个站点，展开不同的检测点的详情',
    'dev_index_webResponesTimeTop10':'\
站点响应时间top10:各个站点在不同的检测点（运营商线路）的响应时间排行。',

    'dev_index_webAvailMap':'\
站点可用性top10:各个站点在不同的检测点（运营商线路）的可用性排行',



    'web_config_edit':'\
左边的站点目录树上点击你想编辑的站点，然后在右边的编辑页面上修改对应的站点的配置信息。<br>\
<span style="color:red">站点配置参数介绍:</span><br>\
站点添加页面已介绍，这里不再作介绍，详情请看添加站点页面的帮助信息。',
    'web_config_add':'\
站点配置参数介绍:<br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">重定向IP:</span><br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">http用户名:</span>用户名，要登陆站点时，才会用于这个参数。<br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">http密码:</span>用户密码，要登陆站点时，才会用于这个参数。<br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">正则:</span>筛选适合一定条件的站点<br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">正则取反:</span>与正则配合使用，筛选以正则相反的结果<br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">超时:</span>连接站点最长允许时间，默认是10秒<br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">是否使用SSL:</span>连接站点是否使用安全套接字<br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">url:</span>站点对应的URL地址<br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">区分大小写:</span>url是否区别大小写，默认是否',

    'web_config_webCls':'\
为了更好的管理站点，可以根据情况进行站点分类。',

    'setting_index_baseInfo':'\
显示用户基本信息，如用户名、帐户余额、邮件、联系电话、公司等信息。',

    'setting_index_changePassword':'\
修改用户密码',

    'setting_index_changeEmailAandPhone':'\
修改用户邮箱与电话',

    'setting_addBillingRecord':'\
列出当前用户充值记录，最新的充值是表格的最上端。',

    'setting_rmBillingRecordWidget':'\
列出用户近12个月的扣费记录，以及下一个月用户扣费预算。<br/> \
点击展开扣费的详细列表',
   
    'setting_allAlarmRules':'\
告警规则：用户可以自定义一系列的规则，用于筛选Netbase事件，并将过滤的事件以邮件方式发送、通知用户<br/><br/>\
操作：用户可以点击列表里任意条告警规则，然后，在告警规则列表正方显示选择的告警规则详细配置信息，用户可以编辑选择的规则。',
   
    'setting_editAlarmRule':'\
显示在规则列表里选中的规则详细信息，用户可以对此规则进行修改和删除。规则各参数的说明请参照创建告警规则提示信息，这里不再说明。',
    
    'setting_createAlarmRuesWidget':'\
<span style="color:red">什么叫告警规则？</span><br>\
&nbsp;&nbsp;&nbsp;&nbsp;告警规则是用户自行设置的，当设置的设备，如主机，站点，中间件等产生的事件匹配用户的告警规则时，系统会自行向用户的邮箱发送事件邮件。邮箱是用\
户基本信息里的邮箱。<br>\
<span style="color:red">告警规则部分参数说明</span><br>',
    
    'midd_index_listMidd':'\
中间件状态说明:<br/> \
<span class="status-icon-small up"></span> 状态正常  <br> \
<span class="status-icon-small down"></span> 状态异常/宕机  <br> \
<span class="status-icon-small unknown"></span> 状态未知    <br> \
<p> \
中间件的状态，来源于后台Ping进程（每20秒，作为循环周期）获取，<br> \
出现"未知状态",是Ping进程暂时未收集到中间件的相关状态数据，请稍后几分钟刷新组件 ',
   
    'midd_index_newEvent':'\
中间件产生的相关事件，如中间件的连接数最大的设定的阀值<br> \
    <span class="severity-icon-small Info"></span> 代表消息事件<br> \
    <span class="severity-icon-small Warning"></span> 代表警告事件<br> \
    <span class="severity-icon-small Error"></span> 代表错误事件<br> \
    <span class="severity-icon-small Critical"></span> 代表严重事件<br> ',
    
    'midd_col_baseInfo':'\
中间件状态说明:<br/> \
<span class="status-icon-small up"></span> 状态正常  <br> \
<span class="status-icon-small down"></span> 状态异常/宕机  <br> \
<span class="status-icon-small unknown"></span> 状态未知    <br> \
<p> \
中间件的状态，来源于后台Ping进程（每20秒，作为循环周期）获取，<br> \
出现"未知状态",是Ping进程暂时未收集到中间件的相关状态数据，请稍后几分钟刷新组件 ',
    
    'midd_col_newEvent':'\
中间件产生的相关事件，如中间件的连接数最大的设定的阀值<br> \
    <span class="severity-icon-small Info"></span> 代表一般事件<br> \
    <span class="severity-icon-small Warning"></span> 代表警告事件<br> \
    <span class="severity-icon-small Error"></span> 代表错误事件<br> \
    <span class="severity-icon-small Critical"></span> 代表严重事件<br> ',
    'midd_col_conn':'\
一段时间内，中间件连接数变化趋势图',
    
    'midd_col_throughputImg':'\
<span style="color:red">什么叫吞吐量：</span><br>\
&nbsp;&nbsp;&nbsp;&nbsp;吞吐量是指对网络、设备、端口或其他设施，单位时间内成功地传送数据的数量（以比特、字节、分组等测量）。通过观察中间件的吞吐量变化趋势图，了解\
中间件的负载。',
   
    'midd_col_jvm':'\
操作系统为tomcat JVM分配的总内存以及空闲内存的大小，随着时间的变化而变化。通过观察JVM视图可以动态查看TOMCAT使用JVM情况',
    
    'midd_col_threadImg':'\
显示当前线程量及当前忙碌线程量变化趋势图，在并发量很大时，可以根据情况，适当增加默认的线程数据，以提高并发性。通过这个性能图，可以了解一段时间内，tomcat的并发访问量。',
    
    'nginx_config_add':'\
部分配置参数介绍：<br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">http用户名:</span>登录的用户名<br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">http密码:</span>登录的密码<br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">url:</span>nginx监控配置页面对应的url地址，不填时，默认为 /nginx-status <br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">正则:</span>查找符合正则表达式的页面，可选项<br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">错误正则:</span>查找符合错误正则表达式的页面，可选项<br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">所在主机IP:</span>nginx 宿主主机IP地址<br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">端口:</span>nginx 宿主主机对应的端口',

    'iis_config_add':'\
部分配置参数介绍：<br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">用户名:</span>登录WMI用户名 <br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">密码:</span>登录WMI密码 <br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">代理:</span>WMI所在的代理服务器IP地址 <br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">所在主机IP:</span>iis 宿主主机IP地址 <br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">端口:</span>iis 宿主主机对应的端口',

    'tomcat_config_add':'\
部分配置参数介绍：<br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">http用户名:</span>登录的用户名<br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">http密码:</span>登录的密码<br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">url:</span>tomcat监控配置页面对应的url地址，不填时，默认为 /manager/status <br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">正则:</span>查找符合正则表达式的页面，可选项<br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">错误正则:</span>查找符合错误正则表达式的页面，可选项<br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">所在主机IP:</span>tomcat 宿主主机IP地址<br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">端口:</span>tomcat 宿主主机对应的端口',

    'apache_config_add':'\
部分配置参数介绍：<br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">url:</span>apache监控配置页面对应的url地址，不填时，默认为 /server-status?auto <br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">正则:</span>查找符合正则表达式的页面，可选项<br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">错误正则:</span>查找符合错误正则表达式的页面，可选项<br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">所在主机IP:</span>apache 宿主主机IP地址<br>\
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:red">端口:</span>apache 宿主主机对应的端口',
    
    'event_index':'\
该页面显示用户添加的设备、中间件等产生的事件信息。用户可以通过级别、开始时间、结束时间、监控项目、组件、事件信息等对事件进行筛选。还有，用户可以点击事件表格的列头对选择的列进行\
排序',
'thresholdConfig':'\
阀值设置--指通过设置一定的阀值界限后，当监控数据达到设定的界限值时将产生事件报告。阀值类型包括以下：<br>\
（1）最小阀值：当监控实际值小于该设定值时，系统即产生事件报告。<br />\
（2）最大阀值：当监控实际值大于该设定值时，系统即产生事件报告。<br />\
（3）范围阀值：当监控实际值介于该设定值范围内时，系统即产生事件报告。<br />\
（4）关键字阀值：当监控数据中包含该设定值的字符、数字时，系统即产生事件报告。<br />\
（5）状态阀值：当监控数据一旦等于该设定值，系统即产生事件报告。<br /><br/>\
\
把鼠标悬停在“阀值项”上，可查看具体的阀值配置说明'


}
