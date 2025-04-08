import json
import re
from datetime import datetime
from urllib.parse import quote

OPERATOR_MAP = {
    10000: "中国电信",
    10010: "中国联通",
    10086: "中国移动",
    10099: "广电"
}

def generate_table(goods):
    """生成带样式优化的Markdown表格"""
    categories = {
        "中国电信": [],
        "中国联通": [],
        "中国移动": [],
        "广电": []
    }

    for item in goods:
        # 基础数据校验
        if item.get('yuezu', 0) <= 0 or item.get('liuliang', 0) <= 0:
            continue

        # 直接使用JSON解析后的标题（解决乱码问题）
        title = item['title']  
        
        # 特殊标签处理
        tags = []
        if item.get('is_top', 0) > 0:
            tags.append("🔝置顶")
        if item.get('is_main', 0) == 1:
            tags.append("⭐主推")

        # 解析产品亮点（强制浅粉色背景）
        try:
            selling_points = json.loads(item['selling_point'].replace('""', '"'))
        except:
            selling_points = re.findall(r'"([^"]+)"', item['selling_point'])  # 正则兜底解析

        # 生成粉色标签块
        highlight_tags = "".join(
            [f'<span style="background: #FFB6C1; padding: 2px 5px; border-radius: 3px; margin: 2px;">{point}</span>' 
             for point in selling_points]
        )

        # 组合标题和标签
        full_title = f"{' '.join(tags)}<br>{title}<br>{highlight_tags}"

        # 生成正确办理链接
        link = f"https://www.91haoka.cn/webapp/merchant/templet1.html?share_id={item['product_shop_id']}&id={item['id']}&weixiaodian=true"

        # 区域限制检测
        region = "全国"
        if '仅发' in title:
            region = re.search(r'仅发([\u4e00-\u9fa5]+)', title).group(1) or "地区限制"

        # 运营商分类
        operator = OPERATOR_MAP.get(item['operator'], "其他")
        if operator not in categories:
            continue

        # 构建表格行
        row = f"| {full_title} | {item['yuezu']}元 | {item['liuliang']}G | {item['dx_liuliang']}G | " \
              f"{item['yuyin'] or '0.1元/分钟'} | {region} | [立即办理]({link}) |"
        
        categories[operator].append(row)

    # 构建分类表格
    tables = []
    for operator in ['中国移动', '中国电信', '中国联通', '广电']:  # 固定排序
        if rows := categories[operator]:
            header = f"## {'📱' if operator == '中国移动' else '📡' if operator == '中国电信' else '📶' if operator == '中国联通' else '📺'} {operator}套餐\n" \
                     "| 套餐信息 | 月租 | 通用流量 | 定向流量 | 通话 | 区域限制 | 立即办理 |\n" \
                     "|----------|------|----------|----------|------|----------|----------|"
            tables.append("\n".join([header] + rows))
    
    return "\n\n".join(tables)

if __name__ == "__main__":
    # 加载测试数据
    test_data = """
    # 这里粘贴用户提供的完整JSON数据
    """
    
    data = json.loads(test_data)['data']['goods']
    
    md_content = f"""# 🚀 2025年最新流量卡套餐实时更新
**最后更新时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

{generate_table(data)}

## 📌 办理须知
1. 粉色标签为产品核心亮点
2. 置顶/主推标识为平台推荐套餐
3. 实际资费以运营商为准
"""
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(md_content)

## 📌 办理须知
1. 标注"仅发XX"套餐需核对收货地址
2. 0.1元/分钟为全国通话标准资费
3. 色标说明：
   <span style="background: #FFD1DC; padding: 2px 5px;">首月优惠</span>
   <span style="background: #87CEEB; padding: 2px 5px;">全国套餐</span>
   <span style="background: #FFA07A; padding: 2px 5px;">大流量</span>
   <span style="background: #98FB98; padding: 2px 5px;">长期套餐</span>

📞 客服微信: XKKJ66（备注「流量卡」）

---

### 🔍 流量卡SEO关键词  
`2025流量卡推荐2` `全国通用流量套餐` `低月租大流量手机卡`  
`电信星卡办理` `联通长期套餐` `移动特惠卡` `广电5G套餐`  
`学生专属流量卡` `老年人优惠套餐` `企业集团卡`  
`省内流量卡` `全国发货电话卡` `免合约期套餐`  
`抖音免流卡` `微信定向流量` `流量结转服务`  
`高性价比套餐` `携号转网优惠` `物联网卡推荐`  
`上海移动本地卡` `广东联通特惠` `湖南电信大流量`  
`夜间流量包` `家庭共享套餐` `政企专享套餐`  
`短期临时流量卡` `海外漫游套餐` `乡村振兴优惠卡`  
`流量卡比价指南` `套餐续费攻略` `号卡代理佣金政策`  

*覆盖100+搜索关键词组合，提升搜索引擎可见性*
"""
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(md_content)
