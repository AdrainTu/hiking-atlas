"""Curated facts from public sources; no copied photos, article bodies or GPX."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent
links=json.loads((ROOT/'domestic-source-discovery.json').read_text(encoding='utf-8'))['items']
S={}
for item in links:
 name=re.sub(r'\s*\d+篇.*$','',item['title']).strip()
 S[name]=['8264：'+name+'游记索引（社区参考，非通行许可）',item['url']]
S.update({
 'gongga':['8264：贡嘎线路版本资料（2026）','https://bbs.8264.com/thread-5762274-1-1.html'],
 'gongga-small':['巅峰徒步：贡嘎小环线所述版本','https://www.dianfengtubu.com/outdoor/show_1108.html'],
 'kangding-control':['康定市：未开发户外区域封闭公告（2025-11-20起）','https://www.kangding.gov.cn/ttxw/article/678900'],
 'kangding-fire':['康定市：2024—2025防火期封山范围（历史公告）','https://www.kangding.gov.cn/jczwgkzcwj/article/626257'],
 'seven':['8264：七藏沟社区线路记录（2025）','https://bbs.8264.com/thread-5745495-1-1.html'],
 'genyen-pasture':['8264：格聂牧场线版本记录','https://www.8264.com/youji/5709414.html'],
 'genyen-central':['8264：格聂中线与不同版本讨论','https://bbs.8264.com/thread-5714994-1-1.html'],
 'meili-north':['8264：梅里北坡社区记录（2024）','https://www.8264.com/youji/5727707.html'],
 'gongga-old':['两步路：贡嘎大环线历史分段参考','https://www.2bulu.com/community/gotohuatinfo.htm?id=74121191'],
 'ship':['8264：船底顶罗新大环历史记录','https://bbs.8264.com/thread-5705762-1-1.html'],
 'graduate':['户外线路名称与版本汇总（社区参考）','https://t.studyisland.cn/hiking-in-china/'],
 'anima':['国家体育总局：阿尼玛卿环山历史活动资料','https://www.sport.gov.cn/n20001280/n20745751/n20767239/c21763896/content.html'],
 'mengke':['尼勒克县：孟克特古道介绍','https://www.xjnlk.gov.cn/xjnlk/c112921/202508/877684f1b38345bea8fed262b4060981.shtml'],
 'national':['云南省体育局：登山协会推荐步道目录','https://tyj.yn.gov.cn/tyzx/tycy/202310/t20231027_3417352.html'],
 'guizhou':['贵州省体育局：十条徒步线路参考','https://www.sport.gov.cn/n14471/n14495/n14543/c29596319/content.html'],
 'shenzhen':['深圳远足径：官方线路目录与参考指标','https://smartum.sz.gov.cn/gateway/road-site/yzj/home'],
 'sz-corridor':['深圳城管：山海通廊与东西涌段介绍','https://www.sz.gov.cn/cn/xxgk/zfxxgj/bmdt/content/post_10449608.html'],
 'tanglang':['深圳城管：塘朗山郊野公园','https://cgj.sz.gov.cn/xsmh/gysz/twf/jytb/content/post_10840038.html'],
 'jingxi':['北京市：京西古道水峪嘴景区段','https://www.beijing.gov.cn/renwen/bjgk/mtggk/mtgwl/202304/t20230410_2994458.html'],
 'bj-water':['北京文旅局：滨水徒步主题线路','https://whlyj.beijing.gov.cn/zwgk/xwzx/gzdt/202203/t20220331_2644973.html'],
 'limutai':['天津政务网：梨木台景区介绍','https://www.tj.gov.cn/sq/yztj/jqjs/202005/t20200520_2467978.html'],
 'shewalk':['上海市：东佘山登山步道活动资料','https://www.shanghai.gov.cn/nw15343/20251103/3a997544aa514dd7aae5af6967ece985.html'],
 'sh-spring':['上海市：近郊健行线路参考','https://japanese.shanghai.gov.cn/ja-EditorsPick-travelinshanghai/20260302/360ab70dd37d47448ecd5183db08d44a.html'],
 'xiake':['浙江省：霞客古道规划图（不作实时导航）','https://zjjcmspublic.oss-cn-hangzhou-zwynet-d01-a.internet.cloud.zj.gov.cn/jcms_files/jcms1/web2242/site/attach/0/8f1613b33ecd49b78089989e3a38bbef.pdf'],
 'xianxia':['浙江日报：仙霞古道及江山景观介绍','https://zjrb.zjol.com.cn/images/2014-10/21/zjrb2014102100008v01n.pdf'],
 'smallwutai':['人民法院报转载：小五台保护区常态管控说明','https://www.sdcourt.gov.cn/dzlyfy/392669/392640/7357866/index.html'],
 'wutai-control':['五台山游客服务中心：非游览线路管控','https://www.wtsykfwzx.com/tzzn_show.aspx?id=77'],
 'qinling-control':['西安市秦岭保护管理局：违规穿越点位管控（2026）','https://xaqlbhj.xa.gov.cn/xwdt/gzdt/2102659407987367937.html'],
 'qinling-news':['西安市秦岭保护管理局：冰晶顶穿越处罚通报（2026）','https://xaqlbhj.xa.gov.cn/xwdt/gzdt/2080533939170091009.html'],
 'laojun':['洛阳市：老君山官方徒步通道预约说明（2024参考）','https://www.ly.gov.cn/public-jc/2024/06-26/6460.html'],
 'mengshan':['临沂市体育局：龟蒙登山步道活动（2026）','https://lyty.linyi.gov.cn/info/1315/35696.htm'],
 'niushou':['牛首山景区：山岳游览介绍','https://tchinese.niushoushan.net/Notify/3172.html'],
 'qiyun':['齐云山徒步环线版本介绍（旅游平台参考）','https://travelnews.qunar.com/qa_strategy/huangshan-qiyunshan-hiking-travel-guide'],
 'hubei':['湖北文旅推荐山地线路名单（新闻报道）','https://news.cjn.cn/hbpd_19912/sy_19931/202606/t5303426.htm'],
 'wudang':['湖北公安：武当金顶与景区路线安全提示','https://gaj.wuhan.gov.cn/jmzx/jwdt/202209/t20220909_2038267.html'],
 'shennong':['湖北文旅厅：神农顶等开放景点参考','https://wlt.hubei.gov.cn/bmdt/ztzl/wltztzyhhdxjc/wltztzyhbdxjcyxxl/wltztzyhbdxjczrst/202608/t20260827_6002306.shtml'],
 'jinfo':['重庆市：金佛山碧潭幽谷—万步游道介绍','https://admin.cq.gov.cn/zwgk/zfxxgkml/zdlyxxgk/ggwh/ly/zxdt/202504/t20250403_14491960.html'],
 'heishan':['重庆市：黑山谷景区介绍（含交通段）','https://admin.cq.gov.cn/zjcq/cycq/zmjd/zqaaaaajjq/202606/t20260604_15729059.html'],
 'bajiao':['重庆市：黑山八角健身环线','https://admin.cq.gov.cn/zjcq/ydjs/scbd/202408/t20240808_13482642.html'],
 'hainan':['国家林草局：海南国家公园分区体验线路','https://www.forestry.gov.cn/c/www/lcdt/646322.jhtml'],
 'jingyuetan':['吉林文旅官方号：净月潭木栈道与短途步道','https://m.thepaper.cn/newsDetail_forward_27933042'],
 'benxi':['本溪市：关门山等秋季步道景点（2026）','https://www.benxi.gov.cn/ly/lyzx/content_669048'],
 'dawei':['湖南省：大围山赏花徒步线路','https://hunan.gov.cn/hnszf/hnyw/sy/hnyw1/202504/t20250415_33641418.html'],
 'qingyuan':['泉州市：清源山景区介绍','https://www.quanzhou.gov.cn/lyb/lysy/shfg/201510/t20151024_176894.htm'],
 'mingyue':['文旅部：明月山青云栈道等游览景点','https://sjfw.mct.gov.cn/site/dataservice/culdetails?curId=10&id=34932'],
 'maor':['文旅部：猫儿山及漓江源旅游分段','https://www.mct.gov.cn/preview/whzx/qgwhxxlb/gx/202102/t20210219_921683.htm'],
 'li-river':['8264：漓江不同徒步版本记录','https://www.8264.com/youji/list-370906496219040-5-1.html'],
 'taiwan':['观光署：淡兰古道路线体系','https://www.taiwan.net.tw/m1.aspx?SNo=0030278'],
 'caoling':['淡兰绿道官网：草岭古道本体参考长度','https://danlantrail.necoast-nsa.gov.tw/Trails-List.aspx?a=2862&l=1&r=47166373'],
 'nuandong':['观光署开放资料：暖东旧道','https://media.taiwan.net.tw/zh-tw/portal/travel/details/attraction_376570000a_000547'],
 'hk':['香港渔护署：郊野公园远足与季节参考','https://enjoyleisure.afcd.gov.hk/zh-CN/thematic-experiences/country-parks-and-hiking-trails'],
 'eagle':['香港渔护署：鹰巢山自然教育径','https://enjoyleisure.afcd.gov.hk/zh-HK/whats-on/IntotheCountrysideWhereNatureTeaches'],
 'macau':['澳门旅游局：路环与黑沙步行径','https://www.macaotourism.gov.mo/zh-hant/shows-and-entertainment/sports-and-recreation/trails'],
 'guia':['澳门旅游局：松山健康径','https://www.macaotourism.gov.mo/zh-hans/events/whatson/9281/'],
})
ROWS="""
gongga-grand|贡嘎大环线 · 老榆林—巴王海历史版本|四川|29.58,101.90|alpine|4|5|85|4920|格西草原、日乌切垭口、莫溪沟、贡嘎寺、子梅村与巴王海的社区五日版本；不是同起终点的标准闭环|雪峰、冰川谷地、森林与牧场|gongga,gongga-old,kangding-control|R
gongga-small|贡嘎小环线 · 巴王海—子梅村版本|四川|29.52,101.79|alpine|3|4|50|0|选取俱乐部巴王海—子梅村—贡嘎寺组合的四个步行日；不含日乌切垭口，交通天另计|贡嘎西坡、寺院与湖谷|gongga-small,kangding-control|R
gongga-lenggacuo|冷嘎措 · 贡嘎观景历史徒步版本|四川|29.66,101.61|alpine|3|0|0|0|冷嘎措不同进出方向不能合并成一条轨迹，保留区域资料|雪山倒影与高山湖泊|gongga,kangding-control,kangding-fire|R
gongga-bawang|巴王海 · 湖谷历史徒步版本|四川|29.42,101.80|alpine|3|0|0|0|巴王海湖谷不同往返与穿越版本，不能等同贡嘎全线|森林湖泊与贡嘎南部山谷|gongga-small,kangding-control,kangding-fire|R
yala-history|雅拉雪山 · 穿越历史资料|四川|30.43,101.72|alpine|4|0|0|0|雅拉周边多日穿越主题；不等同景区已开放的观光步道|高原牧场与雪峰景观|雅拉雪山,kangding-control|R
qizanggou|七藏沟 · 社区穿越版本|四川|32.81,103.64|alpine|4|3|50|0|按2025社区活动所述约50公里三日版本归档，未取得实测轨迹|高原海子与沟谷|seven,七藏沟|U
genyen-grand|格聂大环线 · 多日线路资料|四川|29.83,99.77|alpine|4|0|0|0|格聂多日大环各队伍进出口不同，须先选定具体版本|雪峰环抱的高原谷地|格聂神山,genyen-central|U
genyen-small|格聂小环线 · 短环版本资料|四川|29.88,99.77|alpine|3|0|0|0|格聂小环是社区统称，不能直接套用大环的距离与垭口数据|牧场、山谷与雪峰远景|格聂神山,genyen-small-proof|U
genyen-pasture|格聂牧场线 · 河谷改线版本|四川|29.85,99.75|alpine|4|0|0|0|采用2023社区记录的牧场与肖扎河谷组合概览，区别山脊版本|花季草甸、溪谷与寺院区域|genyen-pasture|U
dangling-hulu|党岭葫芦海 · 高山湖泊资料|四川|30.83,101.58|alpine|3|0|0|0|党岭湖泊方向的往返主题，不把多海子串线当作同一版本|山谷森林与高山湖泊|党岭|U
yading-grand-kora|亚丁大转山 · 外圈历史版本|四川|28.44,100.30|alpine|4|0|0|0|三神山外圈的多日主题，区别于已收录的景区牛奶海与珍珠海步道|雪峰外圈与高原海子|亚丁大转山|U
longyan-history|龙眼线 · 历史穿越资料|四川|31.28,102.88|alpine|4|0|0|0|龙眼相关不同连穿版本的资料概览，不含登峰或冰川攀登方案|横断山高山谷地|龙眼|U
zilong-history|子龙秘境 · 多日山野线路资料|四川|31.23,102.89|alpine|4|0|0|0|采用社区子龙主题归档，进出口和垭口版本尚未统一核实|高山湖谷与雪峰区域|子龙秘境|U
yangmolong-history|央莫龙 · 山麓徒步资料|四川|29.68,99.30|alpine|4|0|0|0|仅收录山麓徒步主题，不能将雪山攀登线路视为普通徒步|雪峰、牧场与山麓谷地|央莫龙|U
meili-north-new|梅里北坡 · 社区线路资料|云南|28.63,98.78|alpine|4|0|0|0|梅里北坡多日徒步主题，不等同雨崩景区步道|梅里北部雪峰与山谷|meili-north,梅里北坡|U
meili-outer-new|梅里外转 · 滇藏历史线路资料|云南 / 西藏|28.55,98.65|alpine|4|0|0|0|梅里外圈长距离历史主题，跨地区通行与具体版本另行核实|雪峰外围村落与山谷|梅里外转|U
yubeng-ice-lake|雨崩冰湖 · 传统往返版本|云南|28.42,98.81|alpine|3|0|0|0|冰湖往返主题，与神瀑步道分开收录；当前步道开放待核实|梅里山麓森林与高山湖谷|雨崩|U
kula-kangri-new|库拉岗日 · 高原湖泊徒步资料|西藏|28.28,90.60|alpine|4|0|0|0|围绕库拉岗日的多湖泊版本，不包含山峰攀登|喜马拉雅雪峰与高原湖泊|库拉岗日|U
everest-east-new|珠峰东坡 · 嘎玛沟传统版本|西藏|27.94,87.09|alpine|4|0|0|0|嘎玛沟多日徒步主题，非珠峰登顶，也不能套用尼泊尔EBC数据|喜马拉雅东侧山谷与冰川远景|珠峰东坡|U
shishapangma-new|希夏邦马 · 南侧山麓徒步资料|西藏|28.20,85.79|alpine|4|0|0|0|希夏邦马山麓徒步主题与技术攀登区分；边境和保护地手续待核实|雪峰南侧谷地|希夏邦马|U
nyenchen-east-new|念青唐古拉东段 · 历史穿越资料|西藏|30.10,94.70|alpine|4|0|0|0|念青东是大型山区的多条穿越主题，不代表唯一的一条轨迹|藏东雪峰与高山湖谷|念青东|U
thanthang-new|他念他翁 · 多日穿越资料|西藏|29.47,98.48|alpine|4|0|0|0|社区他念他翁多日穿越主题，不同组合不能合并里程|藏东山脊与高原湖泊|他念他翁|U
guokala-new|郭喀拉日居 · 历史徒步资料|西藏|29.11,90.83|alpine|4|0|0|0|仅归档社区高海拔徒步主题，不提供未核实的实走轨迹|高原湖群与雪山景观|郭喀拉日居|U
boshula-new|伯舒拉岭 · 多日线路资料|西藏|30.13,96.65|alpine|4|0|0|0|伯舒拉岭山区的长线主题，具体起终点与许可待核实|藏东山地与谷地|伯舒拉岭|U
lengbu-new|冷布岗日 · 高海拔徒步资料|西藏|28.54,86.03|alpine|4|0|0|0|山麓高海拔主题，不包含冰川通行或技术登顶|喜马拉雅山麓与高原荒野|冷布岗日|U
south-tianshan-new|南天山北线 · 历史穿越资料|新疆|42.77,82.38|alpine|4|0|0|0|南天山北线长距离穿越主题，口径与出入口尚未统一核实|天山谷地与高山牧场|南天山北线|U
bogda-circuit-new|博格达环线 · 山麓历史版本|新疆|43.85,88.32|alpine|4|0|0|0|博格达环线与峰顶攀登分开，仅保留社区山麓线路资料|天山雪峰与湖谷|博格达峰|U
karajun-crossing-new|喀拉峻穿越 · 草原长线资料|新疆|43.00,82.10|mountain|3|0|0|0|草原跨区域穿越主题，与景区鲜花台观光段区分|伊犁草原与山谷|喀拉峻草原|U
mengke-new|孟克特古道 · 山地穿越资料|新疆|43.82,83.85|alpine|4|0|70|0|采用县级介绍的古道全线约70公里口径，不等同当前开放观光段|天山古道与湖谷|mengke,孟克特古道|U
tianlang-new|天狼之路 · 历史长线资料|新疆|43.62,86.42|alpine|4|0|0|0|天狼之路是社区长线主题，不能直接合并已有狼塔和乌孙数据|天山山脊与谷地|天狼之路|U
zhagana-crossing-new|扎尕那 · 迭山多日穿越资料|甘肃|34.28,103.16|mountain|4|0|0|0|迭山多日穿越主题，区别于现有仙女滩景区往返步道|石峰、牧场与藏寨区域|扎尕那|U
badain-lakes-new|巴丹吉林沙漠 · 湖区徒步资料|内蒙古|39.65,102.55|desert|4|0|0|0|沙漠湖区多日主题，选择湖泊、车辆支援和版本后才能核算里程|沙丘与内陆湖泊|巴丹吉林|U
tengger-new|腾格里沙漠 · 湖泊穿越资料|内蒙古|38.28,105.05|desert|3|0|0|0|不同五湖与多湖组合的距离差异较大，当前只收录湖泊穿越主题|沙丘与湖泊绿洲|腾格里沙漠|U
anima-new|阿尼玛卿转山 · 历史环山资料|青海|34.80,99.46|alpine|4|0|0|0|以2016年组织活动作为历史证据；现行路线与通行另行核实|果洛雪峰与高原草甸|anima|U
great-wutai-new|五台山大朝台 · 合法游览段资料|山西|39.10,113.57|mountain|4|0|0|0|大朝台社区主题，非游览山路不得擅自进入，不能将台怀镇步道视为全线|五座台顶所在山区与寺院文化|五台山,wutai-control|R
small-wutai-new|小五台 · 历史穿越资料|河北|39.94,115.01|mountain|4|0|0|0|小五台保护区历史穿越主题，不作为可自由进入的登山路线|高山草甸与山脊区域|smallwutai|R
south-taihang-new|南太行 · 郭亮—王莽岭分段资料|河南 / 山西|35.69,113.58|mountain|3|0|0|0|南太行有景区步道与未开放野线；这里只归档跨景区徒步主题，不默认连续可通行|崖壁、村落与太行山景|南太行|U
west-taihang-new|西太行 · 山地穿越资料|山西 / 河北|37.50,113.55|mountain|4|0|0|0|西太行社区主题范围较大，具体版本和合法通行区域待核实|太行山谷与山地村落|西太行|U
bj-three-peaks-new|北京三峰 · 传统环穿资料|北京|40.05,116.02|mountain|3|0|0|0|大觉寺、阳台山与妙峰山方向的社区版本，当前进出口开放待核实|京西山地与古道|graduate|U
zhejiang-qianba-new|浙南千八 · 历史连峰资料|浙江|27.74,119.28|mountain|4|0|0|0|千八并非一个景区步道，连峰范围、保护地与具体版本需单独核实|浙南高山与森林|qianba|U
zhejiang-seven-new|天目七尖 · 历史穿越资料|浙江|30.33,119.42|mountain|4|0|0|0|七尖山脊穿越与已收录的西天目大树王步道不同|天目山山脊与山林|seven-peaks|U
zhejiang-three-new|临安三尖 · 历史穿越资料|浙江|30.35,119.40|mountain|3|0|0|0|社区三尖短连穿主题，不能以山峰景点开放推定山脊穿越合法|浙西山脊与草坡|three-peaks|U
boat-bottom-new|船底顶罗新大环 · 历史资料|广东|24.57,113.34|mountain|4|3|47|1586|参考2023社区罗新大环版本约47公里，不包括其他石布或联布走法|碎石山坡、草甸与森林|ship|U
qinling-ice-new|秦岭冰晶顶 · 管控历史线路|陕西|33.86,108.51|mountain|4|0|0|0|现行官方管控点位，仅保留山地资料，不提供进入方式|秦岭石海与山脊区域|qinling-control,qinling-news|R
qinling-lujiao-new|秦岭鹿角梁 · 管控历史线路|陕西|33.73,108.61|mountain|4|0|0|0|现行官方管控点位，不能依旧游记或商业页面安排进入|秦岭草甸与森林区域|qinling-control|R
wugong-traverse-new|武功山 · 发云界山脊历史版本|江西|27.50,114.20|mountain|4|0|0|0|发云界等山脊穿越主题，区别于已收录的金顶景区台阶往返|山脊草甸与云海|武功山|U
jingxi-new|京西古道 · 水峪嘴—牛角岭景区段|北京|39.97,116.04|ancient|2|1|0|0|仅选择京西古道风景区实际开放的水峪嘴一带游步道，非京西全路网|蹄窝古道与关城遗迹|jingxi|O
beijing-canal-new|北京大运河森林公园 · 滨水分段|北京|39.85,116.79|urban|2|1|0|0|大运河森林公园开放岸线分段往返，不把官方多点旅游行程误算成全程步行|运河、水岸林地与观景平台|bj-water|O
limutai-new|天津梨木台 · 景区山林步道|天津|40.17,117.59|forest|2|1|0|0|梨木台景区开放游步道往返，不包含九山顶跨区野线|山林、溪谷与岩壁|limutai|O
seshan-new|上海东佘山 · 登高步道|上海|31.10,121.20|forest|2|1|0|0|东佘山园登山步道与观景段，区别于东西佘山全域串联|竹林与近郊山景|shewalk|O
sh-hill-new|上海双子山 · 世博文化公园步道|上海|31.18,121.48|urban|2|1|4|0|官方温室花园—园内景点—双子山—温室花园约4公里组合；非单纯上下双子山距离|城市山丘与公园景观|sh-spring|O
xiake-new|宁海霞客古道 · 分段徒步|浙江|29.22,121.18|ancient|2|0|0|0|霞客古道跨宁海、新昌与天台的分段主题，古道与公路连接段须区分|古村、山林与诗路文化|xiake|O
xianxia-new|仙霞古道 · 仙霞关开放段|浙江|28.47,118.49|ancient|2|1|0|0|选仙霞关已开放古道段，非浙闽古道全长穿越|古关、石阶与山林|xianxia|O
qiyun-new|齐云山 · 景区徒步环线|安徽|29.81,118.03|mountain|2|1|0|0|景区步道组合资料；2026年7月部分登山道曾封闭，本版本当前通行尚未核实|丹霞岩壁与道教山村|qiyun,qiyun-notice|U
niushou-new|南京牛首山 · 山岳游览步道|江苏|31.89,118.73|urban|2|1|0|0|景区开放山路与人文景点分段游览，观光车段不计入徒步|山地公园与人文景观|niushou|O
changling-new|长岭国家登山健身步道 · 分段体验|广东|23.23,113.53|forest|2|0|0|0|登山协会推荐的广州黄埔长岭步道体系，需依据当地开放线路选段|丘陵森林与健身步道|national|O
mengshan-new|蒙山龟蒙 · 景区登山步道|山东|35.61,117.84|mountain|3|1|0|0|按龟蒙景区正式游步道登山，不进入护栏外或未开放路线|沂蒙山林与岩峰|mengshan|O
laojun-new|老君山 · 官方徒步通道|河南|33.78,111.65|mountain|3|1|0|0|选景区公告中的预约徒步通道，入口与开放时段按新公告核实|伏牛山景与山顶古建筑|laojun|O
baoq-new|宝泉崖上太行 · 山地游步道|河南|35.47,113.57|mountain|2|1|0|0|登山协会推荐步道主题，按景区合法开放游线选择|太行崖壁与高处观景|national|O
ningxia-wall-new|盐池长城 · 山地徒步廊道|宁夏|37.79,107.38|ancient|2|0|0|0|国家推荐的长城徒步廊道分段，不踩踏城墙遗存或翻越封闭段|长城遗址与塞上旷野|national|O
aobaoling-new|敖包岭 · 登山健身步道|黑龙江|47.52,122.89|forest|2|1|0|0|碾子山敖包岭山地步道主题，按当地标识选择实际开放段|山林与城市周边山地|national|O
yichun-new|伊春森林徒步 · 开放步道分段|黑龙江|47.75,128.90|forest|2|0|0|0|国家推荐的伊春森林徒步主题；先选定景区或线路再核算里程|小兴安岭森林|national|O
guiyang-ridge-new|贵阳黔山岭脊 · 城市山地线|贵州|26.62,106.68|forest|2|1|10.6|0|官方推荐黔灵山、鹿冲关与植物园组合参考，连接段按开放标识核实|城市林带与山脊视野|guizhou|O
zhengan-new|正安桴㯊十景 · 分段徒步资料|贵州|28.34,107.40|mountain|3|0|22.5|0|官方推荐组合的参考长度，不自行进入天坑、洞穴或保护区核心范围|竹海、茶园与峡谷区域|guizhou|U
nightroad-new|六盘水夜郎天路 · 草甸环线|贵州|26.11,105.42|mountain|3|1|9|0|官方推荐的半坡村高山草甸环线版本|草甸、石林与江谷远景|guizhou|O
getuhe-new|格凸河 · 穿洞徒步资料|贵州|25.76,106.08|mountain|4|0|12|0|官方推荐的穿洞组合资料，技术段与开放游览栈道不混为一条线|洞穴、峡谷与峰丛|guizhou|U
youshan-new|油杉河山骨 · 山地步道组合|贵州|27.49,105.73|mountain|3|0|20|0|官方推荐的山地步道组合参考，分段开放和接驳另行核实|岩峰、峡谷与草原|guizhou|O
fanjing-west-new|梵净山西线 · 西上东下版本|贵州|27.89,108.70|mountain|4|0|25|0|官方推荐的西上东下组合，门票、通行方向与下撤时段以景区安排为准|山地森林与金顶岩峰|guizhou|O
kaili-waterfall-new|凯里响水岩瀑布 · 白岩村组合|贵州|26.45,107.95|forest|2|1|6|0|官方约6公里组合；瀑布与白岩村之间含另行接驳，不是全程连续步道|林间瀑布与梯田村落|guizhou|O
longli-canyon-new|龙里草原—峡谷 · 徒步资料|贵州|26.41,106.98|mountain|3|0|15|0|官方推荐的草原峡谷组合，绳索和洞穴段需核实组织与技术要求|草原、竹林与峡谷|guizhou|U
maling-new|马岭河峡谷 · 天星画廊步道组合|贵州|25.17,104.95|mountain|2|1|12|0|官方峡谷与峰林组合参考；分景区段和交通接驳必须另外区分|峡谷瀑布与峰林景观|guizhou|O
chetian-new|贵安车田峡谷 · 休闲徒步组合|贵州|26.41,106.51|forest|2|1|9|0|官方推荐的车田湖、峡谷和村落组合参考|峡谷湖泊与石板民居|guizhou|O
shenzhen-kunpeng-new|深圳鲲鹏径 · 全径分段|广东|22.63,114.09|mountain|3|0|199.03|927|采用官方目录全径参考口径；不是单日线路，各段开放另核实|城市山脊与山海连城景观|shenzhen|O
shenzhen-yangtai-new|深圳阳台山 · 官方环线|广东|22.68,113.99|mountain|3|0|36.9|569|官方目录的阳台山环线参考版本，非任意登顶往返里程|山林与城市远景|shenzhen|O
shenzhen-fenghuang-new|深圳凤凰径 · 分段体验|广东|22.69,113.88|mountain|3|0|81.89|301|采用官方目录凤凰径全线参考，单日需另选分段|丘陵山林与城市边缘|shenzhen|O
shenzhen-maluan-new|深圳马峦山 · 官方环线|广东|22.67,114.32|mountain|3|0|40.22|461|官方环线参考指标，不等同瀑布短线往返|山林、村落与山地景观|shenzhen|O
shenzhen-cuiwei-new|深圳翠微径 · 官方全线参考|广东|22.73,114.12|mountain|3|0|47.16|312|以官方目录全线指标为参考，具体选段和交通另安排|郊野丘陵与森林|shenzhen|O
shenzhen-tanglang-new|深圳塘朗山 · 郊野公园步道|广东|22.60,113.98|mountain|2|1|0|430|公园开放登高步道参考，最高点与单次步行里程不同指标|森林与深圳山海城景|tanglang|O
shenzhen-corridor-new|塘朗山—大沙河—深圳湾 · 山海通廊|广东|22.57,113.96|urban|2|1|13|0|采用2023官方介绍的约13公里贯通版本，后续改线按现场标识核实|山地、河岸与海湾|sz-corridor|O
shenzhen-coast-new|东西涌 · 海岸徒步段|广东|22.48,114.58|coast|3|1|0|0|官方介绍的东西涌海岸段；风浪、潮汐、预约与关闭须出发前核实|海蚀地貌与大鹏海岸|sz-corridor|O
shenzhen-dading-new|深圳大顶岭 · 郊野步道|广东|22.77,113.97|forest|2|1|0|0|大顶岭开放郊野径与观景桥分段，非光明全区道路串联|山林、桥梁与城市景观|sz-corridor|O
wudang-new|武当山金顶 · 景区游步道|湖北|32.40,111.00|mountain|3|1|0|0|景区正式金顶游步道，实际起点决定里程，不进入非开放岔路|山岳古建筑与石阶|wudang,hubei|O
shennong-new|神农顶 · 景区观景步道|湖北|31.44,110.30|mountain|3|1|0|0|只选神农顶景区实际开放步道，非核心保护区穿越|高山森林与观景平台|shennong,hubei|O
luyuan-new|鹿院坪 · 景区山谷步道|湖北|30.50,109.25|mountain|3|1|0|0|推荐主题中的景区步道版本，不合并未开发外穿线路|山谷村落与瀑布|hubei|O
qingjiang-bed-new|清江古河床 · 线路资料|湖北|30.36,108.93|mountain|3|0|0|0|古河床与洞穴版本的资料概览，当前安全开放条件待核实|古河床、岩石与洞穴区域|hubei|U
jinfo-new|金佛山 · 碧潭幽谷—万步游道|重庆|29.03,107.18|mountain|3|1|0|0|官方介绍的西门登山步道组合，冬季冰雪关闭与恢复须按新公告|峡谷、森林与山顶观景|jinfo|O
heishan-new|重庆黑山谷 · 景区谷道|重庆|28.87,106.98|forest|2|1|0|0|景区介绍13公里含多种交通段，此记录只指实际开放步行谷道，不把13公里当徒步实测|峡谷、溪流与浮桥|heishan|O
bajiao-new|黑山八角 · 健身环线|重庆|28.87,106.96|forest|2|1|8|0|官方介绍的约8公里健身绿道环线|山林与度假区步道|bajiao|O
hainan-jianfeng-new|尖峰岭 · 获准开放雨林步道|海南|18.73,108.87|forest|2|1|0|0|仅收录国家公园获准开放体验步道主题，不进入核心保护范围|热带雨林与观景点|hainan|O
hainan-bawang-new|霸王岭 · 获准开放体验步道|海南|19.09,109.12|forest|2|1|0|0|国家公园片区公开体验线路分段，不等同保护区野外穿越|热带森林与自然教育|hainan|O
hainan-diaoluo-new|吊罗山 · 获准开放步道分段|海南|18.72,109.83|forest|2|1|0|0|以国家公园公开体验线路选段，步道范围以管理机构公布为准|雨林与山谷景观|hainan|O
jingyue-long-new|净月潭 · 环潭木栈道|吉林|43.79,125.47|forest|2|1|17.5|0|官方文旅介绍的环潭木栈道版本，冰雪季按开放段调整|湖泊与森林|jingyuetan|O
jingyue-short-new|净月潭 · 月亮湾短线|吉林|43.80,125.46|forest|2|1|3.5|0|官方正门、西环潭、月亮湾、东环潭短线参考|湖岸与林间步道|jingyuetan|O
benxi-new|本溪关门山 · 景区森林步道|辽宁|41.21,124.27|forest|2|1|0|0|景区开放森林步道选段，非周边山脊野线穿越|辽东山林与秋季枫色|benxi|O
dawei-new|浏阳大围山 · 赏花徒步版本|湖南|28.42,114.06|forest|2|1|10|0|2025官方花季活动约10公里版本，非保护区任意线路|杜鹃花与山地森林|dawei|O
qingyuan-new|泉州清源山 · 老君岩游步道|福建|24.95,118.60|mountain|2|1|0|0|老君岩与景区开放游步道分段，不把山峰海拔当作本段爬升|石刻、山林与城市远景|qingyuan|O
mingyue-new|明月山 · 青云栈道游览段|江西|27.57,114.26|mountain|2|1|0|0|选青云栈道等实际开放高山游览步道，进出索道或小火车另计|悬空栈道、湖泊与云雾|mingyue|O
maor-new|猫儿山 · 合法开放观景步道|广西|25.87,110.42|mountain|3|1|0|0|只选景区依法开放观景段；生态核心区和保护区非游览范围不得进入|桂北山地森林与水源地远景|maor|O
li-river-new|漓江 · 杨堤—兴坪徒步资料|广西|24.91,110.44|ancient|2|0|0|0|沿岸不同走法含渡运和不连续村道，不能直接套用百公里漓江全线|喀斯特峰林与江岸村落|li-river|U
taiwan-danlan-new|淡兰古道 · 北路分段|台湾|25.03,121.83|ancient|2|0|0|0|北路的多段古道体系，不把网络总长算成单次徒步距离|古道、茶山与山海文化|taiwan|O
taiwan-caoling-new|草岭古道 · 古道本体版本|台湾|24.97,121.92|ancient|2|1|6.2|0|采用淡兰绿道官网的古道本体约6.2公里口径，不含福隆车站等额外进出步行|芒草、碑刻与东北角山海|caoling|O
taiwan-nuandong-new|暖东旧道 · 淡兰中路分段|台湾|25.07,121.76|ancient|2|1|0|0|观光署公开介绍的旧道分段，进出道路与登山口步行另核实|山林与百年古道路网|nuandong|O
hk-eagle-new|鹰巢山 · 自然教育径|香港|22.34,114.17|forest|2|1|3|0|官方自然教育径约3公里版本，非狮子山登顶路线|林间研习与水塘远景|eagle|O
hk-tai-mo-new|大帽山 · 开放郊游段|香港|22.41,114.12|mountain|3|1|0|0|渔护署介绍的郊游主题，按标记山径分段，不包含未核实野线|山坡芒草与郊野景观|hk|O
hk-tai-lam-new|大榄郊野公园 · 枫香林步道分段|香港|22.41,114.02|forest|2|1|0|0|渔护署介绍的季节郊游主题，按正式步道选段|枫香林与郊野森林|hk|O
macau-guia-new|澳门松山 · 健康径与东望洋观景|澳门|22.20,113.55|urban|2|1|0|0|松山健康径与开放观景区域步行；隧道400米不是本线路总长|山林与历史灯塔|guia|O
macau-heisha-new|黑沙龙爪角 · 家乐径|澳门|22.11,113.58|coast|2|1|2.15|0|官方2.15公里循环家乐径，按现场开放支路行走|海岸岩石与海景|macau|O
macau-coloane-new|路环 · 官方步行径分段|澳门|22.12,113.56|forest|2|0|0|0|路环步行径体系的分段主题，与黑沙龙爪角海岸短线分开|岛上山林与社区边缘|macau|O
"""

ROWS+="大雪塘-new|大雪塘 · 山麓历史线路资料|四川|30.72,102.88|alpine|4|0|0|0|大雪塘山区多日徒步主题，仅保留山麓资料，不包括峰顶攀登|雪峰与高山谷地|大雪塘|U\n"
ROWS=ROWS.replace('大雪塘-new','daxuetang-new')
S.update({
 'qianba':['8264：千八连峰历史版本记录（2025）','https://www.8264.com/youji/5745666.html'],
 'seven-peaks':['社区作者：天目七尖版本参考','https://post.smzdm.com/p/a5r8qg77/'],
 'three-peaks':['8264：临安三尖历史版本记录','https://bbs.8264.com/thread-5703620-1-1.html'],
 'qiyun-notice':['休宁县官方发布转载：齐云山部分登山道临时关闭（2026-07）','https://m.sohu.com/a/1045371711_121106991'],
 'changling-proof':['广州市体育局：黄埔长岭步道（2026）','https://tyj.gz.gov.cn/xxgk/zfxxgkml/zfxxgkml/gzdt/content/post_10718629.html'],
 'genyen-small-proof':['两步路运营方：格聂小环等路线名称','https://www.2bulu.com/spaceindex/personal_dynamic_new.htm?did=tUNsV9qhJ2Hp%2FR2KBg5Tzw%3D%3D&userId='],
})
TERRAIN={
 'alpine':('高海拔山地',['保暖层、帽与手套','防风防水外层','适合地形的徒步鞋','头灯与备用电源','离线地图与可靠的紧急通信设备','基础急救包与个人必需用品','足量路餐、饮水与应急保温装备','垃圾袋和防晒用品'],'高海拔低氧、强风、骤冷与复杂地形叠加；不要把单篇游记视为能力评估或当前路况证明。'),
 'mountain':('山地步道',['防滑徒步鞋','防雨外层与保暖备用层','登山杖（按个人习惯与地形选择）','头灯与备用电源','离线地图和应急联系安排','饮水、路餐与备用食品','基础急救包、求救哨与应急保温毯','垃圾袋'],'山地陡坡、湿滑石阶、雷暴和路况变化需要关注；不同支线的强度与技术要求可能不同。'),
 'forest':('森林步道',['防滑步行或徒步鞋','雨具与备用衣物','饮水和轻便路餐','头灯或备用照明','离线地图与充电电源','基础急救包与求救哨','适合季节的防晒与防虫用品','垃圾袋'],'雨后湿滑、倒木、临水边缘和季节性关闭需要关注；不要越过围栏或进入非游览区域。'),
 'ancient':('古道与文化步道',['防滑步行鞋','雨具与轻便备用层','饮水、路餐和应急食品','离线地图与备用电源','头灯','基础急救包与求救哨','防晒用品','垃圾袋'],'古道石面、连接公路和文物保护范围需留意；不要将旅游串点图当作一条连续步行轨迹。'),
 'urban':('城市与公园步道',['舒适防滑鞋','饮水与轻便食品','遮阳帽和防晒用品','轻便雨具','手机与备用电源','基础急救用品','反光或备用照明用品','垃圾袋'],'城市步道仍需关注交通交叉、湿滑地面、闸门开放和高温；按体力选择分段。'),
 'coast':('海岸步道',['防滑徒步鞋','防晒衣、帽与防晒用品','饮水与路餐','防水收纳袋','离线地图与备用电源','头灯与求救哨','基础急救包','垃圾袋'],'潮汐、风浪、海岸湿滑岩石和天气关闭尤其重要；不进行未经核实的涉水或攀岩捷径。'),
 'desert':('沙漠徒步',['防晒衣、帽与护目装备','防沙收纳与适合沙地的鞋','可靠的离线导航与备用电源','通信和正规后勤支援安排','按正式方案配置的饮水与备用食品','头灯和备用电池','基础急救包与应急保温装备','垃圾袋'],'沙地消耗、昼夜温差、风沙、缺水与通信盲区会叠加；未核实支援和许可前不作为出发方案。'),
}
def build():
 from catalog import normalize
 from submissions import PROVINCES
 output=[];seen=set()
 for line in ROWS.strip().splitlines():
  if not line.strip():continue
  fields=line.strip().split('|')
  if len(fields)!=13:raise ValueError('bad row '+line)
  rid,name,province,coords,terrain,level,days,km,alt,variant,scenes,source_keys,mode=fields
  assert rid not in seen and re.fullmatch('[a-z0-9-]{1,50}',rid);seen.add(rid)
  assert all(p in PROVINCES for p in province.split(' / '));assert terrain in TERRAIN and mode in ('O','U','R')
  kind,gear,risk=TERRAIN[terrain];days=int(days);km=float(km);alt=float(alt);lat,lon=map(float,coords.split(','));assert 17<=lat<=55 and 73<=lon<=136
  sources=[S[k] for k in source_keys.split(',')]
  if rid=='changling-new':sources.append(S['changling-proof'])
  permit='实际开放步道、预约与临时关闭请出发前向管理方核实；官方推荐或历史活动不保证今天每段都可通行。'
  if mode=='R':
   permit='已有官方管控资料，仅作历史或景观介绍；不得擅自进入非开放范围，恢复或获准进入须以管理机构明确公告为依据。'
   if 'kangding-control' in source_keys:permit='康定2025-11-20公告对未开发户外区域实行封闭并注明另行公布恢复；本次未核实上述徒步版本的恢复公告。不要进入受管控范围。'
   if 'qinling-control' in source_keys:permit='西安秦岭保护管理部门2026年资料将相关点位列为管控禁入区域；仅保留历史地理介绍，不提供进入安排。'
   if 'smallwutai' in source_keys:permit='官方转载资料说明小五台保护区实行常态管控，禁止擅自开展旅游、登山等活动；仅保留历史资料。'
   if 'wutai-control' in source_keys:permit='五台山官方公告禁止经非游览线路开展登山探险；大朝台各段不得因旧轨迹而推定可通行。'
  elif mode=='U':permit='未核实本版本的当前通行许可、开放和实走条件；仅展示公开线路资料，不作为出发或导航方案。'
  metrics=('距离和高点采用所列来源的版本参考，不是本站实测。' if km or alt else '里程、路线高点与累计爬升尚未取得一致的可靠数据。')+'难度为本站参考分级；地图为区域粗略标记，不是登山口或GPX。'
  description=name+'的资料整理。该条目按具体版本或主题独立收录，主要看点为'+scenes+'。'+variant+'。'+metrics+('当前仅作资料展示。' if mode!='O' else '体验时只采用合法开放并有现场标识的路段。')
  r=normalize({'name':name,'english':'China Trail · '+rid.replace('-',' ').title(),'country':'中国','continent':'亚洲','province':province,'description':description,'level':int(level),'distance':km,'altitude':alt,'days':days,'points':[[lat,lon]],'gear':gear,'itinerary':[['版本与看点',variant+'；'+scenes+'。'],['核验与选择',permit]],'type':kind+' / '+('公开步道参考' if mode=='O' else '线路资料'),'infoOnly':mode!='O','locationOnly':True,'permit':permit,'risks':risk,'sources':sources,'tags':[kind,province,'国内线路补充','版本参考'],'highlights':[scenes,'明确版本，避免混用里程','源页可追溯'],'accessText':('按实际开放步道安排' if mode=='O' else '官方管控 · 资料展示' if mode=='R' else '开放未核实 · 资料展示')})
  r.update(id=rid,photoPending=True,access='planning' if mode=='O' else 'restricted' if mode=='R' else 'reference',routeVersion=variant,dataNotes=metrics,sourceCheckedAt='2026-10-11',sourceVerification='公开步道/活动资料；当前开放须核实' if mode=='O' else '官方管控与历史资料' if mode=='R' else '社区资料，现行开放未核实',ascent=0,ascentText='累计爬升待核实',altitudeLabel='所述版本参考高点（非累计爬升）',altitudeText=(f'来源参考约 {alt:g} m，非实测；不代表雪山主峰海拔' if alt else '线路高点待核实，不以主峰海拔代替'),distanceText=(f'来源所述版本约 {km:g} km，非本站实测；交通与延伸段另核实' if km else '版本里程待核实'),duration=(f'{days} 天 · 所述版本/单日分段参考，交通另计' if days else '天数待核实 · 先选择具体分段或版本'),seasonText='季节与天气条件待核实；不以固定月份保证通行',logistics='先确认具体入口、出口及正规接驳。地图点仅粗略表示所属地区，不可直接作为导航终点。',stay='仅考虑合法开放范围内的接待设施；当前未收录核实的营地、床位或营业信息。',food='自备适合选定路段的饮水与路餐；补给点营业和水源情况未实时核实，不直接饮用未经处理的野外水。',photoTip='在合法开放步道内拍摄并尊重文物、野生动植物与他人隐私。未授权社区照片不转载，欢迎用户提交自己的实拍。')
  if rid=='gongga-grand':r['dataNotes']+='约85公里为2026社区帖子五段数字相加，原作者亦说明估算不准确；4920米为日乌切垭口参考。'
  if rid=='gongga-small':r['dataNotes']+='约50公里为所列俱乐部17、9、15、9公里四个步行日合计；不是全车程，也不含日乌切垭口。'
  output.append(r)
 return output
if __name__=='__main__':
 rows=build();seed=json.loads((ROOT/'catalog-seed.json').read_text(encoding='utf-8'));ids={r['id'] for r in seed['routes']};assert not ids&{r['id'] for r in rows}
 path=ROOT/'domestic-expansion-20261011.json';path.write_text(json.dumps({'batch':'domestic-public-sources-20261011-v1','routes':rows,'policy':'Original short summaries and fact metadata; no copied images, GPX, private contacts or complete articles.'},ensure_ascii=False,indent=2),encoding='utf-8')
 provinces={p for r in seed['routes']+rows for p in r.get('province','').split(' / ') if p};print(json.dumps({'newRoutes':len(rows),'domesticTotal':sum(r['country'].startswith('中国') for r in seed['routes']+rows),'total':len(seed['routes'])+len(rows),'provinceCoverage':len(provinces),'uniqueSources':len({u for r in rows for _,u in r['sources']}),'referenceOnly':sum(r['infoOnly'] for r in rows)},ensure_ascii=True))
