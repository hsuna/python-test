from selenium import webdriver  #导入Selenium
import requests
from bs4 import BeautifulSoup  #导入BeautifulSoup 模块
import os  #导入os模块
import time

class KXFiction():
    def __init__(self):  #类的初始化操作
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'}  #给请求指定一个请求头来模拟chrome浏览器
        self.web_url = 'https://m.boluoxs.com/'  #要访问的网页地址
        self.folder_path = 'D:\Desktop\quanzhigaoshou.txt'  #设置图片要存放的文件目录

    def start(self):
        f = open(self.folder_path, 'ab')
        f.seek(0)
        f.truncate()   #清空文件

        # 抓取所有文章链接
        hrefs = '489030.htm|489031.htm|489032.htm|489033.htm|489034.htm|489035.htm|489036.htm|148878.htm|489037.htm|148880.htm|148881.htm|148882.htm|148883.htm|148884.htm|148885.htm|489038.htm|489039.htm|489040.htm|489041.htm|489042.htm|148891.htm|148892.htm|489043.htm|489044.htm|489045.htm|489046.htm|489047.htm|148898.htm|148899.htm|148900.htm|148901.htm|148902.htm|148903.htm|148904.htm|148905.htm|148906.htm|148907.htm|148908.htm|148909.htm|148910.htm|148911.htm|148912.htm|148913.htm|148914.htm|148915.htm|148916.htm|148917.htm|148918.htm|148919.htm|148920.htm|148921.htm|148922.htm|148923.htm|148924.htm|148925.htm|148926.htm|148927.htm|148928.htm|148929.htm|489048.htm|148931.htm|148932.htm|148933.htm|148934.htm|148935.htm|148936.htm|489049.htm|148938.htm|148939.htm|148940.htm|148941.htm|148942.htm|148943.htm|148944.htm|148945.htm|489050.htm|148947.htm|148948.htm|148949.htm|148950.htm|148951.htm|148952.htm|489051.htm|148954.htm|148955.htm|148956.htm|148957.htm|148958.htm|148959.htm|148960.htm|148961.htm|148962.htm|148963.htm|148964.htm|148965.htm|148966.htm|148967.htm|91.htm|92.htm|93.htm|94.htm|95.htm|96.htm|97.htm|98.htm|99.htm|100.htm|101.htm|102.htm|103.htm|104.htm|105.htm|106.htm|107.htm|108.htm|109.htm|110.htm|111.htm|112.htm|113.htm|114.htm|115.htm|116.htm|117.htm|118.htm|119.htm|120.htm|121.htm|122.htm|123.htm|124.htm|125.htm|126.htm|127.htm|128.htm|129.htm|130.htm|131.htm|132.htm|133.htm|134.htm|135.htm|136.htm|137.htm|138.htm|139.htm|140.htm|141.htm|142.htm|143.htm|144.htm|145.htm|146.htm|147.htm|148.htm|149.htm|150.htm|151.htm|152.htm|153.htm|154.htm|155.htm|156.htm|157.htm|158.htm|159.htm|160.htm|161.htm|162.htm|163.htm|164.htm|165.htm|166.htm|167.htm|168.htm|169.htm|170.htm|171.htm|172.htm|173.htm|174.htm|175.htm|176.htm|177.htm|178.htm|179.htm|180.htm|181.htm|182.htm|489052.htm|184.htm|185.htm|186.htm|187.htm|188.htm|189.htm|489053.htm|191.htm|192.htm|489054.htm|194.htm|195.htm|196.htm|197.htm|198.htm|199.htm|489055.htm|201.htm|202.htm|203.htm|204.htm|205.htm|206.htm|207.htm|208.htm|209.htm|210.htm|211.htm|489056.htm|213.htm|214.htm|215.htm|489057.htm|217.htm|218.htm|489058.htm|220.htm|489059.htm|222.htm|489060.htm|224.htm|225.htm|226.htm|227.htm|489061.htm|229.htm|230.htm|231.htm|232.htm|233.htm|234.htm|235.htm|236.htm|237.htm|238.htm|239.htm|240.htm|241.htm|242.htm|243.htm|244.htm|245.htm|246.htm|247.htm|248.htm|249.htm|250.htm|251.htm|252.htm|253.htm|254.htm|255.htm|256.htm|257.htm|258.htm|259.htm|260.htm|261.htm|262.htm|263.htm|264.htm|265.htm|266.htm|267.htm|268.htm|269.htm|270.htm|271.htm|272.htm|273.htm|274.htm|275.htm|276.htm|277.htm|278.htm|279.htm|280.htm|489062.htm|282.htm|283.htm|284.htm|285.htm|286.htm|287.htm|489063.htm|289.htm|290.htm|291.htm|292.htm|293.htm|294.htm|295.htm|296.htm|297.htm|298.htm|299.htm|300.htm|301.htm|302.htm|303.htm|304.htm|305.htm|306.htm|307.htm|308.htm|309.htm|310.htm|311.htm|312.htm|313.htm|314.htm|315.htm|316.htm|317.htm|318.htm|319.htm|320.htm|321.htm|322.htm|323.htm|324.htm|325.htm|326.htm|327.htm|328.htm|329.htm|330.htm|331.htm|332.htm|333.htm|334.htm|335.htm|336.htm|337.htm|338.htm|339.htm|340.htm|341.htm|342.htm|343.htm|344.htm|345.htm|346.htm|347.htm|348.htm|349.htm|350.htm|351.htm|352.htm|353.htm|354.htm|355.htm|356.htm|357.htm|358.htm|359.htm|360.htm|361.htm|362.htm|363.htm|364.htm|365.htm|366.htm|367.htm|368.htm|369.htm|370.htm|371.htm|372.htm|373.htm|374.htm|375.htm|376.htm|377.htm|378.htm|379.htm|380.htm|381.htm|382.htm|383.htm|384.htm|385.htm|386.htm|387.htm|388.htm|389.htm|390.htm|391.htm|392.htm|393.htm|394.htm|395.htm|396.htm|397.htm|398.htm|399.htm|400.htm|401.htm|402.htm|403.htm|404.htm|405.htm|406.htm|407.htm|408.htm|409.htm|410.htm|411.htm|412.htm|413.htm|414.htm|415.htm|416.htm|417.htm|418.htm|419.htm|420.htm|421.htm|422.htm|423.htm|424.htm|425.htm|426.htm|427.htm|428.htm|429.htm|430.htm|431.htm|432.htm|433.htm|434.htm|435.htm|436.htm|437.htm|438.htm|439.htm|440.htm|441.htm|442.htm|443.htm|444.htm|445.htm|446.htm|447.htm|448.htm|449.htm|450.htm|451.htm|452.htm|453.htm|454.htm|455.htm|456.htm|457.htm|458.htm|459.htm|460.htm|461.htm|462.htm|463.htm|464.htm|465.htm|466.htm|467.htm|468.htm|469.htm|470.htm|471.htm|472.htm|473.htm|474.htm|475.htm|476.htm|477.htm|478.htm|479.htm|480.htm|481.htm|482.htm|483.htm|484.htm|485.htm|486.htm|487.htm|488.htm|489.htm|490.htm|491.htm|492.htm|493.htm|494.htm|495.htm|496.htm|497.htm|498.htm|499.htm|500.htm|501.htm|502.htm|503.htm|504.htm|505.htm|506.htm|507.htm|508.htm|509.htm|510.htm|511.htm|512.htm|513.htm|514.htm|515.htm|516.htm|517.htm|518.htm|519.htm|520.htm|521.htm|522.htm|523.htm|524.htm|489064.htm|526.htm|527.htm|528.htm|529.htm|530.htm|531.htm|489065.htm|533.htm|534.htm|535.htm|536.htm|537.htm|538.htm|539.htm|540.htm|541.htm|542.htm|543.htm|544.htm|545.htm|546.htm|547.htm|548.htm|489066.htm|550.htm|551.htm|552.htm|553.htm|554.htm|555.htm|489067.htm|557.htm|558.htm|559.htm|560.htm|561.htm|489068.htm|563.htm|564.htm|489069.htm|566.htm|567.htm|489070.htm|489071.htm|570.htm|571.htm|489072.htm|573.htm|574.htm|489073.htm|489074.htm|577.htm|578.htm|579.htm|580.htm|581.htm|582.htm|489075.htm|584.htm|585.htm|586.htm|587.htm|588.htm|589.htm|590.htm|591.htm|592.htm|593.htm|594.htm|595.htm|596.htm|597.htm|598.htm|599.htm|600.htm|601.htm|602.htm|603.htm|604.htm|605.htm|606.htm|607.htm|608.htm|609.htm|610.htm|611.htm|612.htm|613.htm|614.htm|615.htm|616.htm|617.htm|618.htm|619.htm|620.htm|621.htm|622.htm|623.htm|624.htm|625.htm|626.htm|627.htm|628.htm|629.htm|630.htm|631.htm|632.htm|633.htm|634.htm|635.htm|636.htm|637.htm|638.htm|639.htm|640.htm|641.htm|642.htm|643.htm|644.htm|645.htm|646.htm|647.htm|648.htm|489076.htm|650.htm|489077.htm|652.htm|653.htm|654.htm|655.htm|489078.htm|657.htm|489079.htm|659.htm|660.htm|661.htm|662.htm|663.htm|664.htm|665.htm|666.htm|667.htm|668.htm|669.htm|670.htm|671.htm|672.htm|673.htm|489080.htm|675.htm|676.htm|677.htm|678.htm|679.htm|680.htm|489081.htm|489082.htm|683.htm|684.htm|685.htm|686.htm|687.htm|688.htm|489083.htm|690.htm|691.htm|692.htm|693.htm|694.htm|695.htm|696.htm|697.htm|698.htm|699.htm|700.htm|701.htm|702.htm|703.htm|704.htm|705.htm|706.htm|707.htm|708.htm|709.htm|489084.htm|711.htm|712.htm|713.htm|714.htm|715.htm|716.htm|489085.htm|718.htm|719.htm|720.htm|721.htm|722.htm|723.htm|724.htm|725.htm|726.htm|727.htm|728.htm|489086.htm|730.htm|731.htm|732.htm|733.htm|734.htm|735.htm|489087.htm|737.htm|738.htm|739.htm|740.htm|741.htm|742.htm|743.htm|744.htm|745.htm|746.htm|747.htm|748.htm|749.htm|750.htm|751.htm|752.htm|753.htm|754.htm|755.htm|756.htm|757.htm|758.htm|759.htm|760.htm|761.htm|762.htm|763.htm|764.htm|765.htm|766.htm|767.htm|768.htm|769.htm|770.htm|771.htm|772.htm|773.htm|774.htm|775.htm|776.htm|777.htm|778.htm|779.htm|780.htm|781.htm|782.htm|783.htm|784.htm|785.htm|786.htm|787.htm|788.htm|789.htm|790.htm|791.htm|792.htm|793.htm|794.htm|795.htm|796.htm|797.htm|798.htm|799.htm|800.htm|801.htm|802.htm|803.htm|804.htm|805.htm|806.htm|807.htm|808.htm|809.htm|810.htm|811.htm|812.htm|813.htm|814.htm|815.htm|816.htm|817.htm|818.htm|819.htm|820.htm|821.htm|822.htm|823.htm|824.htm|825.htm|826.htm|827.htm|828.htm|489088.htm|830.htm|831.htm|832.htm|833.htm|834.htm|835.htm|489089.htm|837.htm|838.htm|839.htm|840.htm|841.htm|842.htm|843.htm|844.htm|845.htm|846.htm|847.htm|848.htm|849.htm|850.htm|851.htm|852.htm|853.htm|854.htm|855.htm|856.htm|857.htm|858.htm|859.htm|860.htm|861.htm|862.htm|863.htm|864.htm|865.htm|866.htm|867.htm|868.htm|869.htm|870.htm|871.htm|872.htm|873.htm|874.htm|875.htm|876.htm|877.htm|878.htm|879.htm|880.htm|881.htm|882.htm|883.htm|884.htm|885.htm|886.htm|887.htm|888.htm|889.htm|890.htm|891.htm|892.htm|893.htm|894.htm|895.htm|896.htm|897.htm|898.htm|899.htm|900.htm|901.htm|902.htm|903.htm|904.htm|905.htm|906.htm|907.htm|908.htm|909.htm|910.htm|911.htm|912.htm|913.htm|914.htm|915.htm|916.htm|917.htm|918.htm|919.htm|920.htm|921.htm|922.htm|923.htm|924.htm|925.htm|926.htm|927.htm|928.htm|929.htm|930.htm|931.htm|932.htm|933.htm|934.htm|935.htm|936.htm|937.htm|938.htm|939.htm|940.htm|941.htm|942.htm|943.htm|944.htm|945.htm|946.htm|947.htm|948.htm|949.htm|950.htm|951.htm|952.htm|953.htm|954.htm|955.htm|956.htm|957.htm|958.htm|959.htm|960.htm|961.htm|962.htm|963.htm|964.htm|965.htm|966.htm|967.htm|968.htm|969.htm|970.htm|971.htm|972.htm|973.htm|974.htm|975.htm|976.htm|977.htm|978.htm|979.htm|980.htm|981.htm|982.htm|983.htm|984.htm|985.htm|986.htm|987.htm|988.htm|989.htm|990.htm|991.htm|992.htm|993.htm|994.htm|995.htm|996.htm|997.htm|998.htm|999.htm|1000.htm|1001.htm|1002.htm|1003.htm|1004.htm|1005.htm|1006.htm|1007.htm|1008.htm|1009.htm|1010.htm|1011.htm|1012.htm|1013.htm|1014.htm|1015.htm|1016.htm|1017.htm|1018.htm|1019.htm|1020.htm|1021.htm|1022.htm|1023.htm|1024.htm|1025.htm|1026.htm|1027.htm|1028.htm|1029.htm|1030.htm|1031.htm|1032.htm|1033.htm|1034.htm|1035.htm|1036.htm|1037.htm|1038.htm|1039.htm|1040.htm|1041.htm|1042.htm|1043.htm|1044.htm|1045.htm|1046.htm|489090.htm|1048.htm|1049.htm|1050.htm|1051.htm|1052.htm|1053.htm|489091.htm|1055.htm|1056.htm|1057.htm|1058.htm|1059.htm|1060.htm|1061.htm|1062.htm|1063.htm|1064.htm|1065.htm|1066.htm|1067.htm|1068.htm|1069.htm|1070.htm|1071.htm|1072.htm|1073.htm|1074.htm|1075.htm|1076.htm|1077.htm|1078.htm|1079.htm|1080.htm|1081.htm|1082.htm|1083.htm|1084.htm|1085.htm|1086.htm|1087.htm|1088.htm|1089.htm|1090.htm|1091.htm|1092.htm|1093.htm|1094.htm|1095.htm|1096.htm|1097.htm|1098.htm|1099.htm|1100.htm|1101.htm|1102.htm|1103.htm|1104.htm|1105.htm|1106.htm|1107.htm|1108.htm|1109.htm|1110.htm|1111.htm|1112.htm|1113.htm|1114.htm|1115.htm|1116.htm|1117.htm|1118.htm|1119.htm|1120.htm|1121.htm|1122.htm|1124.htm|1125.htm|1126.htm|1127.htm|1128.htm|1129.htm|1130.htm|1131.htm|1132.htm|1133.htm|1134.htm|1135.htm|1136.htm|1137.htm|1138.htm|1139.htm|1140.htm|1141.htm|1142.htm|1143.htm|1144.htm|1145.htm|1146.htm|1147.htm|1148.htm|1149.htm|1150.htm|1151.htm|1152.htm|1153.htm|1154.htm|1155.htm|1156.htm|1157.htm|1158.htm|1159.htm|1160.htm|1161.htm|1162.htm|1486468.htm|1164.htm|1165.htm|1166.htm|1167.htm|1168.htm|1169.htm|1170.htm|1171.htm|1172.htm|1486469.htm|1486470.htm|1175.htm|1176.htm|1177.htm|1178.htm|1179.htm|1180.htm|1181.htm|1182.htm|1183.htm|1184.htm|1185.htm|1186.htm|1187.htm|1188.htm|1189.htm|1190.htm|1191.htm|1192.htm|1193.htm|1194.htm|1195.htm|1196.htm|1197.htm|1198.htm|1199.htm|1200.htm|1201.htm|1202.htm|1203.htm|1204.htm|1205.htm|1206.htm|1207.htm|1208.htm|1209.htm|1210.htm|1211.htm|1212.htm|1213.htm|1214.htm|1215.htm|1216.htm|1217.htm|1218.htm|1219.htm|1220.htm|1221.htm|1222.htm|1223.htm|1224.htm|1225.htm|1226.htm|1227.htm|1228.htm|1229.htm|1230.htm|1231.htm|1232.htm|1233.htm|1234.htm|1235.htm|1236.htm|1237.htm|1238.htm|1239.htm|1240.htm|1241.htm|1242.htm|1243.htm|1244.htm|1245.htm|1246.htm|1247.htm|1248.htm|1249.htm|1250.htm|1251.htm|1252.htm|1253.htm|1254.htm|1255.htm|1256.htm|1257.htm|1258.htm|1259.htm|1260.htm|1261.htm|1262.htm|1263.htm|1264.htm|1265.htm|1266.htm|1267.htm|1268.htm|1269.htm|1270.htm|1271.htm|1272.htm|1273.htm|1274.htm|1275.htm|1276.htm|1277.htm|1278.htm|1279.htm|1280.htm|1282.htm|1283.htm|1284.htm|1285.htm|1286.htm|1287.htm|1288.htm|1289.htm|1290.htm|1291.htm|1292.htm|1293.htm|1294.htm|1295.htm|1296.htm|1297.htm|1298.htm|1299.htm|1300.htm|1301.htm|1302.htm|1303.htm|1304.htm|1305.htm|1306.htm|9835.htm|9836.htm|9837.htm|9838.htm|9839.htm|9840.htm|9841.htm|9842.htm|9843.htm|9844.htm|9845.htm|9846.htm|9847.htm|9848.htm|9849.htm|489093.htm|9851.htm|148968.htm|9853.htm|9854.htm|9855.htm|9856.htm|489094.htm|9858.htm|9859.htm|9860.htm|9861.htm|9862.htm|489095.htm|9864.htm|148969.htm|9866.htm|40704.htm|40705.htm|40706.htm|489096.htm|40708.htm|40709.htm|40710.htm|40711.htm|40712.htm|40713.htm|40714.htm|40715.htm|40716.htm|40717.htm|40718.htm|40719.htm|40720.htm|40721.htm|40722.htm|40723.htm|40724.htm|40725.htm|40726.htm|144692.htm|144161.htm|144162.htm|144163.htm|144164.htm|144165.htm|144166.htm|144167.htm|144168.htm|144169.htm|144170.htm|144171.htm|144172.htm|144173.htm|144174.htm|144175.htm|144176.htm|144177.htm|144178.htm|144179.htm|144180.htm|144181.htm|144182.htm|144183.htm|144184.htm|144185.htm|144186.htm|144187.htm|144188.htm|144189.htm|144190.htm|144191.htm|144192.htm|144193.htm|144194.htm|144195.htm|144196.htm|144197.htm|144198.htm|144199.htm|144200.htm|144201.htm|144202.htm|144203.htm|144204.htm|144205.htm|144206.htm|144208.htm|144209.htm|144210.htm|144211.htm|144213.htm|144214.htm|144215.htm|144216.htm|144217.htm|144218.htm|144219.htm|144220.htm|144221.htm|144222.htm|144223.htm|144224.htm|144226.htm|144227.htm|144228.htm|144693.htm|144694.htm|144695.htm|144696.htm|145151.htm|145152.htm|145153.htm|145164.htm|145165.htm|145357.htm|145358.htm|145464.htm|145465.htm|145677.htm|145678.htm|145679.htm|146025.htm|146400.htm|146401.htm|146588.htm|146589.htm|146639.htm|146703.htm|146717.htm|147787.htm|147806.htm|148970.htm|148971.htm|148109.htm|148110.htm|148133.htm|148295.htm|148296.htm|148297.htm|148298.htm|148313.htm|149579.htm|149904.htm|151610.htm|151669.htm|151670.htm|151671.htm|152331.htm|152456.htm|153405.htm|153803.htm|155599.htm|156467.htm|157538.htm|158262.htm|160023.htm|161209.htm|162199.htm|163190.htm|163551.htm|163557.htm|163920.htm|164063.htm|164071.htm|164250.htm|164563.htm|164975.htm|165129.htm|165162.htm|165667.htm|166164.htm|166563.htm|167293.htm|167537.htm|167890.htm|168122.htm|168395.htm|168660.htm|168707.htm|168753.htm|168793.htm|169122.htm|169199.htm|169242.htm|169290.htm|169298.htm|169368.htm|169376.htm|169425.htm|169447.htm|169468.htm|169515.htm|169565.htm|169603.htm|169649.htm|169678.htm|169692.htm|169701.htm|169918.htm|169919.htm|169972.htm|170077.htm|170136.htm|170160.htm|170277.htm|170320.htm|170435.htm|170488.htm|170532.htm|170747.htm|170847.htm|170897.htm|170971.htm|171159.htm|171224.htm|171284.htm|171332.htm|171390.htm|171443.htm|171490.htm|171585.htm|171639.htm|171675.htm|171720.htm|171789.htm|171854.htm|171867.htm|171917.htm|171924.htm|171952.htm|171968.htm|172195.htm|172249.htm|172296.htm|172352.htm|172405.htm|172452.htm|172498.htm|172550.htm|178581.htm|172678.htm|172713.htm|172751.htm|173711.htm|173745.htm|173802.htm|174179.htm|174510.htm|174551.htm|174607.htm|175132.htm|175179.htm|175186.htm|175237.htm|175285.htm|175351.htm|175422.htm|175654.htm|175742.htm|175762.htm|175822.htm|176996.htm|177036.htm|177143.htm|177185.htm|177248.htm|177652.htm|177685.htm|177741.htm|177745.htm|177973.htm|178011.htm|178231.htm|178270.htm|178325.htm|178498.htm|178536.htm|178582.htm|178621.htm|178661.htm|178710.htm|178748.htm|178790.htm|178794.htm|178829.htm|178874.htm|178916.htm|179340.htm|179362.htm|179564.htm|179635.htm|179748.htm|179781.htm|179782.htm|179815.htm|179821.htm|179828.htm|179830.htm|179846.htm|179847.htm|179892.htm|179893.htm|179924.htm|179933.htm|179973.htm|179992.htm|179994.htm|180022.htm|180044.htm|180045.htm|180046.htm|180782.htm|180787.htm|180788.htm|180800.htm|180826.htm|180829.htm|180837.htm|180857.htm|180870.htm|180871.htm|181120.htm|181121.htm|181122.htm|181410.htm|181413.htm|181450.htm|181489.htm|181494.htm|181509.htm|181528.htm|181754.htm|181798.htm|181802.htm|181840.htm|181874.htm|181876.htm|181924.htm|181971.htm|181984.htm|182023.htm|182058.htm|182105.htm|182141.htm|182217.htm|182242.htm|182249.htm|182251.htm|182295.htm|182330.htm|182364.htm|182602.htm|489092.htm|182636.htm|182668.htm|182764.htm|182793.htm|182836.htm|182866.htm|183138.htm|183185.htm|183242.htm|183601.htm|183992.htm|184279.htm|184339.htm|184491.htm|184561.htm|184608.htm|185099.htm|185158.htm|185212.htm|185266.htm|185312.htm|185355.htm|185404.htm|185448.htm|185486.htm|185536.htm|185656.htm|185711.htm|185759.htm|185806.htm|185851.htm|185896.htm|185929.htm|185950.htm|185967.htm|185997.htm|186012.htm|186019.htm|186033.htm|186041.htm|186058.htm|186078.htm|186095.htm|489098.htm|186285.htm|186353.htm|186378.htm|186409.htm|186419.htm|186431.htm|489099.htm|186466.htm|186482.htm|186488.htm|186499.htm|186508.htm|186535.htm|186807.htm|186808.htm|186809.htm|186810.htm|186811.htm|186812.htm|186813.htm|186814.htm|186815.htm|186816.htm|186817.htm|186818.htm|187012.htm|187040.htm|187072.htm|187124.htm|187142.htm|187153.htm|187196.htm|187209.htm|187238.htm|187276.htm|187278.htm|187302.htm|187371.htm|187383.htm|187417.htm|187426.htm|187448.htm|187799.htm|188208.htm|188498.htm|188556.htm|188566.htm|188615.htm|188735.htm|188771.htm|188880.htm'
        all_href = hrefs.split('|')
        
        for href in all_href:
            req = self.request(self.web_url + '/txt/36/' + href)
            text = req.content.decode('gb18030', 'ignore')
            soup = BeautifulSoup(text, 'lxml')
            
            #抓取文章标题
            title = soup.select('.bookname h1')
            tm = title[0].get_text().strip()

            #抓取文章内容
            content = soup.select('#zjneirong')
            nr = content[0].get_text()
            
            txt = '\t' + tm + '\r\n\r\n' + nr + '\r\n\r\n'
            f.write(txt.encode('utf-8'))
            print(tm)
            
        f.close()
    
    def request(self, url):  #返回网页的response
        r = requests.get(url, headers=self.headers)  # 像目标url地址发送get请求，返回一个response对象。有没有headers参数都可以。
        r.encoding = 'utf-8' 
        return r



comic = KXFiction()  #创建类的实例
comic.start()  #执行类中的方法