// 线路坐标为关键地点走向示意，不是实测 GPX。数值按所列版本取近似值。
window.TRAILS = [
  {
    id:'tmb',name:'环勃朗峰',english:'Tour du Mont Blanc',country:'法国 · 意大利 · 瑞士',continent:'欧洲',flag:'🇫🇷',level:3,
    distance:170,distanceText:'约 165–170 km',duration:'9–14 天',days:11,altitude:2665,altitudeText:'2,665 m（高线变体）',altitudeLabel:'高线最高海拔',season:[6,7,8,9],seasonText:'6 月下旬至 9 月',type:'环线',tags:['阿尔卑斯','雪山','山屋'],subtitle:'一步一国，绕行阿尔卑斯的雪白心脏。',
    description:'绕勃朗峰山群穿越三国，景观从冰川、垭口切换到牧场与山村。成熟的山屋网络让你不必每天携带全部食物，但连续多日的升降依然考验体能。经典路线和高线变体不同，2,665 米指 Col des Fours 或 Fenêtre d’Arpette 变体，并非每个行程都会经过。',
    highlights:['意大利 Val Ferret 的雪山长廊','勃朗峰冰川与高山牧场','法、意、瑞三国山村与山屋文化'],
    gear:['防水外套与雨裤','抓地力好的徒步鞋','登山杖','保暖中层','山屋睡袋内胆','头灯与备用电池','离线地图与充电宝'],
    logistics:'日内瓦抵达后转往霞慕尼或 Les Houches；也可从库马约尔出发。',stay:'山屋、旅馆；旺季应提前订床位。',food:'多数山屋可提供餐食，跨垭口日仍要自带饮水与午餐。',permit:'山屋住宿需预订；露营规则因国家与保护区而异。',risks:'残雪、雷暴、连续爬升与陡降。高线变体需要额外判断能力。',photoTip:'清晨 Val Ferret 侧光适合拍雪峰；在山屋门口拍日落无需冒险离开步道。',
    itinerary:[['启程','Les Houches → Les Contamines'],['翻越垭口','Les Chapieux → 库马约尔'],['进入瑞士','Val Ferret → La Fouly → Champex'],['回归法国','Trient → 霞慕尼山谷 → Les Houches']],
    points:[[45.89,6.80],[45.82,6.73],[45.70,6.73],[45.77,6.84],[45.79,6.97],[45.89,7.05],[45.93,7.10],[46.03,7.12],[46.06,7.01],[46.00,6.93],[45.93,6.88],[45.89,6.80]],
    sources:[['TMB 山屋协会','https://www.autourdumontblanc.com/en/'],['路线与高线变体','https://en.wikipedia.org/wiki/Tour_du_Mont_Blanc']]
  },
  {
    id:'ebc',name:'珠峰南坡大本营',english:'Everest Base Camp',country:'尼泊尔',continent:'亚洲',flag:'🇳🇵',level:4,
    distance:130,distanceText:'约 130 km 往返',duration:'12–16 天',days:14,altitude:5364,altitudeText:'5,364 m（大本营）',altitudeLabel:'目的地海拔',season:[3,4,5,10,11],seasonText:'3–5 月 / 10–11 月',type:'往返',tags:['喜马拉雅','高海拔','茶屋'],subtitle:'沿夏尔巴人的山谷，走向世界之巅的脚下。',
    description:'从卢克拉沿河谷、吊桥和夏尔巴村落逐渐走入昆布冰川地带，南坡大本营是徒步终点而非登顶路线。行程要把南池与丁波切的适应日算进去；约 130 公里的距离随住宿点与支线变化。卡拉帕塔观景支线比大本营更高，本页海拔不含该支线。',
    highlights:['南池集市与夏尔巴村落','腾波切寺的阿玛达布拉姆背景','昆布冰川与珠峰南坡大本营'],gear:['分层保暖衣物与羽绒服','防水徒步鞋','保暖睡袋（按季节选温标）','防紫外线太阳镜','防晒霜与润唇膏','净水工具','头灯与离线地图'],
    logistics:'经加德满都或实际航班指定机场前往卢克拉；为山地航班延误预留时间。',stay:'沿途茶屋，越往高处条件越简单。',food:'茶屋餐食与处理后的饮水；高处补给价格及可用性变化较大。',permit:'需要国家公园及当地入区许可；导游和许可政策请向当地主管部门核实。',risks:'高海拔适应、低温、山地航班延误；不应为赶进度取消适应日。',photoTip:'腾波切的山峰背景很适合长焦；大本营通常不是拍珠峰顶峰的最佳角度。',
    itinerary:[['进入山谷','卢克拉 → 帕克丁 → 南池'],['逐步适应','南池适应日 → 腾波切 → 丁波切适应日'],['大本营段','罗布切 → 戈拉克舍普 → 南坡大本营'],['返回','沿原路下降至卢克拉，并预留交通缓冲']],
    points:[[27.687,86.731],[27.74,86.713],[27.805,86.713],[27.836,86.764],[27.893,86.831],[27.948,86.811],[27.981,86.829],[28.002,86.852]],
    sources:[['尼泊尔旅游局','https://ntb.gov.np/everest-base-camp'],['大本营海拔资料','https://en.wikipedia.org/wiki/Everest_base_camps']]
  },
  {
    id:'tiger',name:'虎跳峡高路',english:'Tiger Leaping Gorge',country:'中国 · 云南',continent:'亚洲',flag:'🇨🇳',level:2,
    distance:22,distanceText:'约 22 km（高路）',duration:'2 天',days:2,altitude:2650,altitudeText:'约 2,650 m',altitudeLabel:'参考高点',season:[3,4,5,10,11],seasonText:'3–5 月 / 10–11 月',type:'穿越',tags:['峡谷','雪山','客栈'],subtitle:'在金沙江之上，听两座雪山之间的风。',
    description:'高路沿虎跳峡山腰穿行，在哈巴雪山与玉龙雪山之间俯瞰金沙江。二十八道拐是经典上升段，之后可在山腰客栈停留。这里收录的是高路概览；下到中虎跳的陡峭支线不在行程内。起终点选择会改变公里数与高点。',
    highlights:['二十八道拐后的峡谷视野','山腰客栈的玉龙雪山背景','金沙江与峡谷峭壁'],gear:['防滑徒步鞋','登山杖','轻量雨衣','遮阳帽与防晒','头灯','饮水与便携食物','离线地图'],
    logistics:'从丽江或香格里拉到桥头附近入山，终点需安排车辆接驳。',stay:'沿途山腰客栈；节假日提前询问房间。',food:'可在客栈用餐，路段间仍需携带饮水。',permit:'景区票务、路段开放及临时封闭以当地公告为准。',risks:'雨季滑坡、落石和临崖窄路；出发前向当地核实高路通行情况。',photoTip:'上午拍雪山轮廓更清晰；用宽角表现峡谷纵深，站在稳固的步道内。',
    itinerary:[['第 1 天','桥头附近 → 二十八道拐 → 山腰客栈'],['第 2 天','山腰客栈 → 瀑布路段 → 高路出口']],
    points:[[27.178,100.079],[27.185,100.106],[27.208,100.123],[27.231,100.143],[27.257,100.171]],
    sources:[['虎跳峡与高路介绍','https://en.wikipedia.org/wiki/Tiger_Leaping_Gorge']]
  },
  {
    id:'kumano',name:'熊野古道 · 中边路',english:'Kumano Kodo · Nakahechi',country:'日本 · 和歌山',continent:'亚洲',flag:'🇯🇵',level:2,
    distance:38,distanceText:'约 38 km（泷尻至本宫）',duration:'3–4 天',days:3,altitude:700,altitudeText:'约 700 m（路段参考）',altitudeLabel:'山地路段海拔',season:[3,4,5,10,11],seasonText:'3–5 月 / 10–11 月',type:'穿越',tags:['森林','古道','文化'],subtitle:'穿过杉木林与石阶，让脚步慢下来。',
    description:'中边路是熊野古道的核心朝圣线路。本页选取泷尻王子至熊野本宫大社的一段，经过高原、近露和继樱王子。森林、石阶与神社串起历史，也能与温泉民宿结合。去那智大社需要继续走额外路段，照片和行程在这里均以中边路段为主。',
    highlights:['高原村的山间景色','牛马童子与沿途王子社','熊野本宫大社与森林古道'],gear:['防滑徒步鞋','轻便雨具','登山杖','驱虫用品','离线官方地图','现金与巴士时刻表','饮水与午餐'],
    logistics:'纪伊田边乘巴士至泷尻；终点可接驳本宫或汤之峰温泉。',stay:'小型民宿、温泉旅馆；房间数量有限。',food:'提前向民宿订餐，部分村落商店很少。',permit:'住宿和餐食应提前预订；临时绕行请查看官方路线地图。',risks:'湿滑石阶、山区连续起伏与错过末班巴士。',photoTip:'阴天杉木林光线更柔和；神社内部遵守摄影规定。',
    itinerary:[['启程','泷尻王子 → 高原'],['森林与村落','高原 → 近露 → 继樱王子'],['抵达本宫','继樱王子 → 发心门王子 → 熊野本宫大社']],
    points:[[33.791,135.504],[33.804,135.507],[33.817,135.605],[33.828,135.629],[33.861,135.708],[33.84,135.774]],
    sources:[['田边市熊野观光局','https://www.tb-kumano.jp/en/kumano-kodo/nakahechi/'],['官方路线地图','https://www.tb-kumano.jp/en/kumano-kodo/maps/']]
  },
  {
    id:'whw',name:'苏格兰西高地之路',english:'West Highland Way',country:'英国 · 苏格兰',continent:'欧洲',flag:'🇬🇧',level:2,
    distance:154,distanceText:'154 km',duration:'6–9 天',days:7,altitude:550,altitudeText:'550 m',altitudeLabel:'最高海拔',season:[5,6,7,8,9],seasonText:'5–9 月',type:'穿越',tags:['高地','湖泊','荒原'],subtitle:'从洛蒙德湖，走向高地尽头的群山。',
    description:'从米尔盖维到威廉堡的苏格兰经典长线，沿洛蒙德湖经过荒原与山谷，翻越 Devil’s Staircase。海拔不高，但湖畔崎岖路面和连续步行很消耗体力；行李转运与沿途住宿可以减轻负担。最高点 550 米指步道，不含攀登本尼维斯山的额外行程。',
    highlights:['洛蒙德湖的湖畔步道','兰诺克荒原的开阔天际','格伦科与 Devil’s Staircase'],gear:['防水外套与雨裤','防水鞋与备用袜','防蠓虫头网','登山杖','保暖层','水瓶与午餐','离线地图'],
    logistics:'格拉斯哥前往米尔盖维，威廉堡可乘铁路或巴士返程。',stay:'民宿、旅馆、营地，可使用行李转运服务。',food:'村镇补给，荒原路段提前带足。',permit:'一般徒步无全线许可；洛蒙德湖部分区域露营存在季节限制。',risks:'连雨、湿冷、蠓虫与湖边难走路面。',photoTip:'格伦科山谷阴天很有层次，雨后云隙光适合远景。',
    itinerary:[['湖畔','米尔盖维 → Drymen → 洛蒙德湖'],['进入高地','Crianlarich → Tyndrum → Bridge of Orchy'],['荒原','兰诺克荒原 → Kingshouse'],['终段','Devil’s Staircase → Kinlochleven → 威廉堡']],
    points:[[55.941,-4.318],[56.065,-4.452],[56.19,-4.63],[56.337,-4.719],[56.433,-4.714],[56.518,-4.771],[56.65,-4.83],[56.713,-4.963],[56.819,-5.107]],
    sources:[['西高地之路官网','https://www.westhighlandway.org/'],['距离与最高点','https://ldwa.org.uk/ldp/members/show_path.php?path_name=West+Highland+Way']]
  },
  {
    id:'laugavegur',name:'冰岛劳加维格步道',english:'Laugavegur Trail',country:'冰岛',continent:'欧洲',flag:'🇮🇸',level:3,
    distance:55,distanceText:'约 54–56 km',duration:'4 天',days:4,altitude:1200,altitudeText:'约 1,200 m',altitudeLabel:'参考高点',season:[7,8,9],seasonText:'7–8 月最常见 / 9 月视开放',type:'穿越',tags:['火山','彩色山','荒野'],subtitle:'彩色流纹岩、黑沙与冰川之间的异星旅程。',
    description:'从兰德曼纳劳卡到索斯莫克，沿途从彩色山体转入熔岩、黑沙、湖泊与桦树林。标准行程通常四天，官网按不同统计口径给出 54–56 公里。高地天气可能在夏天转为风雪，涉水也要求稳健判断。',
    highlights:['兰德曼纳劳卡的流纹岩山地','Álftavatn 湖与黑沙荒原','索斯莫克冰川谷地'],gear:['防风防水外套与雨裤','保暖层与帽手套','涉水鞋','可靠徒步鞋','离线地图与导航备份','保暖睡袋','食物与炉具（按住宿方式）'],
    logistics:'乘高地巴士往返起终点，运行受道路与天气影响。',stay:'山屋或指定营地，需提前落实住宿。',food:'携带所需食物，按住宿设施安排炉具与燃料。',permit:'山屋和营地请提前预订；先核实高地道路与步道开放。',risks:'强风、雾、残雪与涉水；不是全年可随意通行的路线。',photoTip:'彩色山地与黑沙适合广角；风大时保护镜头并避免在蒸汽区离开步道。',
    itinerary:[['第 1 天','Landmannalaugar → Hrafntinnusker'],['第 2 天','Hrafntinnusker → Álftavatn'],['第 3 天','Álftavatn → Emstrur'],['第 4 天','Emstrur → Þórsmörk']],
    points:[[63.992,-19.061],[63.934,-19.168],[63.856,-19.225],[63.829,-19.198],[63.767,-19.376],[63.686,-19.483]],
    sources:[['冰岛徒步协会 FÍ','https://www.fi.is/en/hiking-trails/trails/laugavegur'],['高地环境与海拔','https://www.fi.is/is/gonguleidir/yfirlit-gonguleida/laugavegur']]
  },
  {
    id:'halfdome',name:'优胜美地半圆顶',english:'Half Dome',country:'美国 · 加利福尼亚',continent:'北美洲',flag:'🇺🇸',level:4,
    distance:26,distanceText:'约 23–26 km 往返',duration:'10–12 小时',days:1,altitude:2682,altitudeText:'约 2,682 m',altitudeLabel:'顶峰海拔',season:[6,7,8,9],seasonText:'钢索开放季，通常晚春至初秋',type:'往返',tags:['花岗岩','瀑布','钢索'],subtitle:'走过瀑布，迎接花岗岩穹顶的最后挑战。',
    description:'由山谷经过 Vernal 与 Nevada 瀑布，最终通过钢索路段登上半圆顶。起点和 Mist Trail / John Muir Trail 选择会改变总距离。这是漫长、暴露的强体能线路；通行许可和钢索状态是计划的前提。',
    highlights:['Vernal 与 Nevada 瀑布','半圆顶钢索末段','俯瞰优胜美地山谷'],gear:['抓地力可靠的鞋','合适防滑手套','头灯与备用电池','足量饮水与食物','防晒帽与太阳镜','防水外套','许可与离线地图'],
    logistics:'从优胜美地山谷 Happy Isles 一带出发，提前安排园内交通。',stay:'可做长日徒步；过夜需对应荒野许可。',food:'沿途处理饮水点很有限，按官方建议安排饮水。',permit:'钢索开放时攀登需要 Half Dome 许可；天气或维护可改变开放日期。',risks:'湿岩和钢索、雷暴、暴露地形、长时间行走；遇雨或雷暴不进入钢索段。',photoTip:'山谷中即可拍半圆顶全貌；钢索段集中注意通行，不停下来摆拍。',
    itinerary:[['清晨出发','Happy Isles → Vernal Fall'],['持续爬升','Nevada Fall → Sub Dome'],['关键决策','天气与钢索条件允许时前往顶峰'],['返回','预留体力、日照与下撤时间']],
    points:[[37.732,-119.558],[37.728,-119.544],[37.731,-119.533],[37.738,-119.519],[37.747,-119.514],[37.746,-119.533]],
    sources:[['美国国家公园局：Half Dome','https://www.nps.gov/yose/planyourvisit/halfdome.htm']]
  },
  {
    id:'inca',name:'印加古道',english:'Inca Trail to Machu Picchu',country:'秘鲁',continent:'南美洲',flag:'🇵🇪',level:3,
    distance:43,distanceText:'约 40–43 km（经典线）',duration:'4 天',days:4,altitude:4215,altitudeText:'约 4,215 m',altitudeLabel:'垭口海拔',season:[5,6,7,8,9],seasonText:'5–9 月干季',type:'穿越',tags:['遗迹','云雾林','高海拔'],subtitle:'沿古老石阶，走入马丘比丘的晨光。',
    description:'经典线从 Km 82 附近出发，穿过高海拔垭口、云雾林和印加遗址，最后经太阳门一带抵达马丘比丘。短版古道与经典四日线差别很大，本页仅概述经典线。',
    highlights:['Dead Woman’s Pass 高山垭口','普尤帕塔马尔卡的遗址与云雾','马丘比丘与印加石阶'],gear:['防水徒步鞋','登山杖（保护套按规定）','保暖睡袋','防水外套','防晒与太阳镜','头灯','轻量日包与饮水'],
    logistics:'库斯科先适应海拔，由合规运营方安排前往起点与返程。',stay:'按运营方获批行程在指定营地住宿。',food:'随行团队供餐，出发前确认个人饮食需求。',permit:'经典古道名额有限，应通过获授权运营方提前办理；维护关闭及遗址规则须核实。',risks:'高海拔、陡石阶、阴雨湿冷；为库斯科适应与交通预留时间。',photoTip:'云雾中的遗迹比赶日出更值得停留；遗址内遵守指定参观线路。',
    itinerary:[['第 1 天','Km 82 → 山谷营地'],['第 2 天','跨越 Dead Woman’s Pass'],['第 3 天','垭口、遗址与云雾林'],['第 4 天','太阳门附近 → 马丘比丘 → 返程']],
    points:[[-13.258,-72.265],[-13.279,-72.288],[-13.256,-72.332],[-13.243,-72.371],[-13.2,-72.535],[-13.164,-72.544]],
    sources:[['秘鲁旅游局','https://www.peru.travel/experiences/trekking-the-inca-trail'],['经典线路资料','https://en.wikipedia.org/wiki/Inca_Trail_to_Machu_Picchu']]
  },
  {
    id:'wtrek',name:'百内国家公园 W 线',english:'Torres del Paine · W Trek',country:'智利 · 巴塔哥尼亚',continent:'南美洲',flag:'🇨🇱',level:3,
    distance:70,distanceText:'约 70–80 km（按支线）',duration:'4–5 天',days:5,altitude:1200,altitudeText:'约 900–1,200 m（按观景支线）',altitudeLabel:'参考高点',season:[10,11,12,1,2,3,4],seasonText:'10–4 月，南半球春夏',type:'穿越含支线',tags:['冰川','湖泊','花岗岩'],subtitle:'三座石塔，蓝色冰川，巴塔哥尼亚的风。',
    description:'三个山谷的往返支线构成 W 形，把 Grey 冰川、法国谷与百内三塔串在一起。智利旅游局的五日示例为约 70 公里，增加观景支线或改变住宿点会增加里程。高点取决于是否走更深的法国谷观景线。',
    highlights:['百内三塔脚下的冰川湖','法国谷的岩壁与悬冰川','Grey 冰川与湖岸'],gear:['防风防水外套','登山杖','保暖层与帽手套','防水徒步鞋','防水收纳袋','头灯','露营装备（选择营地时）'],
    logistics:'纳塔莱斯港乘巴士前往公园，按行走方向安排接驳与渡船。',stay:'营地与山屋，每一晚都应有确认预订。',food:'山屋餐食可预订，徒步白天自带食物。',permit:'公园门票与全部过夜地点需提前落实；严禁随意生火。',risks:'极强阵风、天气突变、长路段与渡船时刻变动。',photoTip:'三塔常有云，给天气留余地；湖畔拍照避开迎风崖边。',
    itinerary:[['西侧','Paine Grande → Grey 冰川支线'],['中部','Paine Grande → 法国谷 → 湖畔营地'],['东侧','湖畔 → Chileno 或 Central'],['三塔','Base Torres 观景点 → 下撤返程']],
    points:[[-51.12,-73.14],[-50.97,-73.19],[-51.12,-73.14],[-51.08,-73.05],[-50.98,-73.04],[-51.08,-73.05],[-51.04,-72.95],[-50.97,-72.89],[-50.94,-72.96],[-50.97,-72.89]],
    sources:[['智利旅游局五日行程','https://chile.travel/en/itineraries/torres-del-paine-w-trek-the-definitive-guide/'],['公园预约与准备','https://chile.travel/atractivos/circuito-w/']]
  },
  {
    id:'kili',name:'乞力马扎罗 · 马查姆线',english:'Kilimanjaro · Machame',country:'坦桑尼亚',continent:'非洲',flag:'🇹🇿',level:4,
    distance:62,distanceText:'约 60–65 km（版本不同）',duration:'7 天常见',days:7,altitude:5895,altitudeText:'5,895 m',altitudeLabel:'Uhuru 峰海拔',season:[1,2,7,8,9,10],seasonText:'1–2 月 / 7–10 月',type:'登顶穿越',tags:['非洲之巅','高海拔','营地'],subtitle:'从热带雨林，走到非洲最高处的黎明。',
    description:'马查姆线由南侧雨林进入高山草甸和荒漠，再接近 Uhuru 峰。常见七日版本增加营地停留，具体距离按运营方路线变化。这是高海拔登顶行程，即使无需传统技术攀登，也需要充分适应、专业组织和撤退判断。',
    highlights:['雨林到高山荒漠的植被变化','Shira 高原与山体视野','Uhuru 峰的高海拔景观'],gear:['高海拔保暖羽绒服','保暖睡袋','防水外套与雨裤','保暖帽与厚手套','结实徒步靴','头灯与备用电池','太阳镜与防晒'],
    logistics:'乞力马扎罗机场到莫希，由获许可运营方安排入山。',stay:'指定营地，由运营方组织帐篷与后勤。',food:'团队供餐并处理饮水，提前确认装备和饮食包含项。',permit:'必须由获许可运营方组织，不允许独自攀登；费用与许可按官方最新要求。',risks:'极高海拔、顶峰夜间严寒与长时间上升；遵循向导对适应和撤退的判断。',photoTip:'山脚也能拍完整山体；顶峰附近先照顾保暖与状态。',
    itinerary:[['雨林','Machame Gate → Machame Camp'],['适应段','Shira → Lava Tower → Barranco'],['靠近顶峰','Karanga → Barafu'],['登顶与下降','Uhuru 峰 → Mweka → 出山']],
    points:[[-3.168,37.237],[-3.099,37.267],[-3.055,37.271],[-3.067,37.327],[-3.079,37.354],[-3.099,37.379],[-3.076,37.353],[-3.143,37.368],[-3.223,37.345]],
    sources:[['坦桑尼亚国家公园局','https://www.tanzaniaparks.go.tz/kilimanjaro/visitor-guide'],['马查姆七日示例','https://machame.com/machame-route-seven-day-itinerary']]
  },
  {
    id:'milford',name:'米尔福德步道',english:'Milford Track',country:'新西兰 · 南岛',continent:'大洋洲',flag:'🇳🇿',level:2,
    distance:53.5,distanceText:'53.5 km',duration:'4 天 / 3 夜',days:4,altitude:1154,altitudeText:'1,154 m',altitudeLabel:'最高海拔',season:[11,12,1,2,3,4],seasonText:'11–4 月 Great Walks 季',type:'单向穿越',tags:['雨林','瀑布','峡湾'],subtitle:'沿冰川雕刻的山谷，穿越雨林与瀑布。',
    description:'从蒂阿瑙湖一端走向米尔福德峡湾，穿越古老雨林、冰川谷地与麦金农垭口。官方标准为四天三夜单向行走，主线 53.5 公里；萨瑟兰瀑布支线需另留时间。雨水塑造了这里的美景，也会影响通行。',
    highlights:['Clinton 河谷与温带雨林','麦金农垭口的两侧谷地','萨瑟兰瀑布周边景观'],gear:['防水外套与雨裤','保暖衣物','防水徒步鞋','睡袋','食物与餐具','防沙蝇用品','头灯与防水袋'],
    logistics:'需安排蒂阿瑙湖起点船程与终点船程，并衔接陆路交通。',stay:'Clinton、Mintaro、Dumpling 三间官方小屋。',food:'自带食物；按当季小屋设施确认炉具需求。',permit:'Great Walks 季小屋必须提前预订，交通另行落实。',risks:'大雨、洪水、垭口天气与雪崩地形；非旺季需要更强的山地经验。',photoTip:'雨后瀑布和湿润苔藓很出片；垭口风大，不为取景离开步道。',
    itinerary:[['第 1 天','Glade Wharf → Clinton Hut'],['第 2 天','Clinton Hut → Mintaro Hut'],['第 3 天','麦金农垭口 → Dumpling Hut'],['第 4 天','Dumpling Hut → Sandfly Point']],
    points:[[-44.919,167.927],[-44.902,167.914],[-44.813,167.858],[-44.801,167.768],[-44.849,167.765],[-44.83,167.729],[-44.694,167.922]],
    sources:[['新西兰 DOC：Milford Track','https://www.doc.govt.nz/parks-and-recreation/places-to-go/fiordland/places/fiordland-national-park/things-to-do/tracks/milford-track/']]
  },
  {
    id:'tongariro',name:'汤加里罗高山穿越',english:'Tongariro Alpine Crossing',country:'新西兰 · 北岛',continent:'大洋洲',flag:'🇳🇿',level:3,
    distance:19.4,distanceText:'约 19.4 km',duration:'7–9 小时',days:1,altitude:1886,altitudeText:'1,886 m',altitudeLabel:'最高海拔',season:[11,12,1,2,3,4],seasonText:'11–4 月；仍需看天气',type:'单日穿越',tags:['火山','翡翠湖','高山'],subtitle:'越过红色火山口，遇见翡翠色的湖。',
    description:'从 Mangatepopo 谷地翻越 Red Crater，再经过翡翠湖与蓝湖下至 Ketetahi。主线最高点 1,886 米，沿途开阔而暴露。线路经过毛利人的神圣山地，请留在标记步道上，尊重湖泊与当地保护要求。',
    highlights:['Red Crater 红色火山口','翡翠湖与蓝湖的色彩','远处湖泊与熔岩地貌'],gear:['防风防水外套与雨裤','保暖层和帽手套','结实徒步鞋','2–3 升饮水（按条件调整）','午餐与能量食品','头灯','离线地图与通讯工具'],
    logistics:'安排国家公园周边城镇的单向接驳，确认回程班次。',stay:'通常住周边城镇，当天穿越。',food:'途中水不可直接饮用，自带饮水与食物。',permit:'官方建议预约；使用接驳或向导服务需要步道预约。',risks:'强风、湿冷、松散火山碎石；冬季有冰雪和雪崩风险，需要相应技能及装备。',photoTip:'翡翠湖在碎石下坡附近，先站稳再拍；不靠近蒸汽口或进入湖水。',
    itinerary:[['谷地','Mangatepopo → South Crater'],['最高点','Red Crater'],['火山湖','Emerald Lakes → Blue Lake'],['下降','北坡 → Ketetahi Road']],
    points:[[-39.145,175.579],[-39.137,175.632],[-39.133,175.652],[-39.131,175.658],[-39.12,175.66],[-39.076,175.665]],
    sources:[['新西兰 DOC：步道与准备','https://www.doc.govt.nz/tongariroalpinecrossing'],['线路里程资料','https://en.wikipedia.org/wiki/Tongariro_Alpine_Crossing']]
  }
];
window.TRAILS.forEach(route => route.gear.push('基础急救包与个人常用药', '应急保温毯与求救哨'));
window.TRAIL_META = {updated:'2026-10-08',levels:{2:'中等',3:'困难',4:'挑战'},colors:{2:'#8edcc5',3:'#f3bd72',4:'#ef8997'}};
