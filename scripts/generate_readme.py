import json
import re
from datetime import datetime

def generate_table(goods):
    """生成带样式优化的Markdown表格"""
    operator_map = {
        10000: "中国电信",
        10010: "中国联通",
        10086: "中国移动",
        10099: "广电"
    }

    categories = {
        "中国电信": [],
        "中国联通": [],
        "中国移动": [],
        "广电": []
    }

    for item in goods:
        # 数据有效性校验
        if item.get('yuezu', 0) <= 0 or item.get('liuliang', 0) <= 0:
            continue

        # 解码标题并处理特殊字符
        title = json.loads(f'"{item["title"]}"').replace('\uff0c', '，')
        
        # 生成标签系统
        tags = []
        if item.get('is_top', 0) > 0:
            tags.append("🔝置顶")
        if item.get('is_main', 0) == 1:
            tags.append("⭐主推")

        # 解析产品亮点
        try:
            selling_points = json.loads(item['selling_point'].replace('""', '"'))
        except:
            selling_points = re.findall(r'"([^"]+)"', item['selling_point'])
        
        # 生成粉色标签块
        highlight_tags = "".join(
            [f'<span style="background: #FFB6C1; padding: 2px 5px; border-radius: 4px; margin: 2px;">{point}</span>' 
             for point in selling_points if point.strip()]
        )

        # 动态生成链接（关键修复）
        product_shop_id = item['product_shop_id']
        template = "merchant/templet1.html" 
        if product_shop_id == 316354:  # 特殊处理海南卡
            template = "gantanhaoluodi/index.html"
            
        link = f"https://www.91haoka.cn/webapp/{template}?share_id={item['page_shop_id']}&id={item['id']}&weixiaodian=true"

        # 区域限制解析增强
        region = "全国"
        if match := re.search(r'仅发([\u4e00-\u9fa5]{2,7})', title):
            region = match.group(1)

        # 运营商分类
        operator = operator_map.get(item['operator'], "其他")
        if operator not in categories:
            continue

        # 构建表格行
        row = f"| {' '.join(tags)}<br>{title}<br>{highlight_tags} | {item['yuezu']}元 | {item['liuliang']}G | {item['dx_liuliang']}G | " \
              f"{item['yuyin'] or '0.1元/分钟'} | {region} | [立即办理]({link}) |"
        
        categories[operator].append(row)

    # 构建分类表格
    tables = []
    for operator in ['中国移动', '中国电信', '中国联通', '广电']:
        if rows := categories[operator]:
            header = f"## {'📱' if operator == '中国移动' else '📡' if operator == '中国电信' else '📶' if operator == '中国联通' else '📺'} {operator}套餐\n" \
                     "| 套餐信息 | 月租 | 通用流量 | 定向流量 | 通话 | 区域限制 | 立即办理 |\n" \
                     "|----------|------|----------|----------|------|----------|----------|"
            tables.append("\n".join([header] + rows))
    
    return "\n\n".join(tables)

if __name__ == "__main__":
    with open('data/cards.json', 'r', encoding='utf-8') as f:
        data = json.load(f)['data']['goods']
    
    md_content = f"""# 🚀 2025年最新流量卡套餐实时更新
**最后更新时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
📌 2025年最新流量卡套餐合集：https://www.91haoka.cn/webapp/weixiaodian/index.html?shop_id=563381&fetch_code=Qm9SpxyHEe  
<strong style="color:red;">⚠️ 失效链接都可以来这里找！📞 客服微信: XKKJ66（备注「办理流量卡」）</strong>
📌 企业官网：https://www.haoka100.cn/
{generate_table(data)}

## 📌 办理须知
1. 粉色标签为产品核心亮点
2. 置顶/主推标识为平台推荐套餐
3. 实际资费以运营商为准

📞 客服微信: XKKJ66（备注「流量卡」）

---

### 🔍 流量卡SEO关键词  
`2025流量卡推荐` `全国通用流量套餐` `低月租大流量手机卡`  
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
