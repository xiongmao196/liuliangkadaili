import json
import ast
from datetime import datetime
from urllib.parse import quote

OPERATOR_MAP = {
    10000: "中国电信",
    10010: "中国联通",
    10086: "中国移动",
    10099: "广电"
}

def generate_table(goods):
    """生成带运营商分类的Markdown表格，自动过滤空分类"""
    categories = {
        "中国电信": {
            "header": "## 📡 中国电信套餐\n| 套餐名称 | 月租 | 通用流量 | 定向流量 | 通话 | 区域限制 | 立即办理 |\n|---------|------|----------|----------|------|----------|----------|",
            "rows": []
        },
        "中国联通": {
            "header": "## 📶 中国联通套餐\n| 套餐名称 | 月租 | 通用流量 | 定向流量 | 通话 | 区域限制 | 立即办理 |\n|---------|------|----------|----------|------|----------|----------|",
            "rows": []
        },
        "中国移动": {
            "header": "## 📱 中国移动套餐\n| 套餐名称 | 月租 | 通用流量 | 定向流量 | 通话 | 区域限制 | 立即办理 |\n|---------|------|----------|----------|------|----------|----------|",
            "rows": []
        },
        "广电": {
            "header": "## 📺 广电套餐\n| 套餐名称 | 月租 | 通用流量 | 定向流量 | 通话 | 区域限制 | 立即办理 |\n|---------|------|----------|----------|------|----------|----------|",
            "rows": []
        }
    }

    for item in goods:
        # 过滤无效数据
        if item.get('yuezu', 0) <= 0 or item.get('liuliang', 0) <= 0:
            continue

        # 清洗标题（根据实际数据情况调整）
        title = item['title'].strip().replace('\u200b', '')  # 示例：移除零宽空格
        
        # 获取运营商分类
        operator = OPERATOR_MAP.get(item['operator'], "其他")
        if operator not in categories:
            continue

        # 生成办理链接
        link = f"https://www.91haoka.cn/webapp/weixiaodian/index.html?shop_id=563381&fetch_code={quote(item['fetch_code'])}"
        
        # 区域限制解析（增强健壮性）
        region = "全国"
        selling_points = []
        try:
            # 尝试两种解析方式
            try:
                selling_points = json.loads(item['selling_point'].replace('""', '"'))
            except json.JSONDecodeError:
                selling_points = ast.literal_eval(item['selling_point'])
        except:
            pass
        
        # 使用正则表达式作为最后兜底方案
        import re
        region_match = re.search(r'仅发([\u4e00-\u9fa5]+)', item['selling_point'])
        if region_match:
            region = region_match.group(1)
        else:
            for point in selling_points:
                if "仅发" in point:
                    region = point.split("仅发")[-1].replace("）", "").strip()
                    break

        # 通话时长处理（增强类型容错）
        try:
            yuyin = int(item.get('yuyin', 0))
        except (ValueError, TypeError):
            yuyin = 0
        call_time = "0.1元/分钟" if yuyin == 0 else f"{yuyin}分钟"
        
        # 定向流量显示优化
        dx_liuliang = item.get('dx_liuliang', 0)
        dx_display = f"{dx_liuliang}G" if dx_liuliang > 0 else "无"

        # 构建表格行
        row = f"| {title} | {item['yuezu']}元 | {item['liuliang']}G | {dx_display} | " \
              f"{call_time} | {region} | [立即办理]({link}) |"
        
        categories[operator]['rows'].append(row)

    # 构建最终输出，过滤空分类
    output = []
    for category in ['中国移动', '中国电信', '中国联通', '广电']:  # 固定排序
        data = categories[category]
        if data['rows']:
            output.append("\n".join([data['header']] + data['rows']))
    
    return "\n\n".join(output)

if __name__ == "__main__":
    with open('data/cards.json', 'r', encoding='utf-8') as f:
        data = json.load(f)['data']['goods']
    
    md_content = f"""# 🚀 2025年最新流量卡套餐实时更新
**最后更新时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

{generate_table(data)}

## 📌 重要说明
1. 标注"仅发XX"需核对收货地址
2. 0.1元/分钟为全国通话资费
3. 定向流量包含抖音/微信等30+APP

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
