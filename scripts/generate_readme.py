import json
from datetime import datetime
from urllib.parse import quote

OPERATOR_MAP = {
    10000: "中国电信",
    10010: "中国联通",
    10086: "中国移动",
    10099: "广电"
}

def generate_table(goods):
    """生成带运营商分类的Markdown表格"""
    categories = {
        "中国电信": "## 📡 中国电信套餐\n| 套餐名称 | 月租 | 通用流量 | 定向流量 | 通话 | 区域限制 | 立即办理 |\n|---------|------|----------|----------|------|----------|----------|",
        "中国联通": "## 📶 中国联通套餐\n| 套餐名称 | 月租 | 通用流量 | 定向流量 | 通话 | 区域限制 | 立即办理 |\n|---------|------|----------|----------|------|----------|----------|",
        "中国移动": "## 📱 中国移动套餐\n| 套餐名称 | 月租 | 通用流量 | 定向流量 | 通话 | 区域限制 | 立即办理 |\n|---------|------|----------|----------|------|----------|----------|",
        "广电": "## 📺 广电套餐\n| 套餐名称 | 月租 | 通用流量 | 定向流量 | 通话 | 区域限制 | 立即办理 |\n|---------|------|----------|----------|------|----------|----------|"
    }

    for item in goods:
        # 过滤无效数据
        if item.get('yuezu', 0) == 0 or item.get('liuliang', 0) == 0:
            continue

        # 修复编码问题（关键点）
        title = item['title'].encode('utf-8').decode('unicode_escape').replace("\\", "")
        operator = OPERATOR_MAP.get(item['operator'], "其他")
        
        # 生成办理链接
        link = f"https://www.91haoka.cn/webapp/weixiaodian/index.html?shop_id=563381&fetch_code={quote(item['fetch_code'])}"
        
        # 区域限制解析（增强容错）
        region = "全国"
        try:
            selling_points = json.loads(item['selling_point'].replace('""', '"').strip('"'))
        except json.JSONDecodeError:
            selling_points = eval(item['selling_point'])  # 强制修复非标准JSON
        
        for point in selling_points:
            if "仅发" in point:
                region = point.split("仅发")[1].replace("）", "").strip()
                break

        # 通话时长处理
        call_time = "0.1元/分钟" if item.get('yuyin', 0) == 0 else f"{item['yuyin']}分钟"
        
        # 构建表格行
        row = f"| {title} | {item['yuezu']}元 | {item['liuliang']}G | {item['dx_liuliang']}G | " \
              f"{call_time} | {region} | [立即办理]({link}) |"
        
        if operator in categories:
            categories[operator] += "\n" + row
            
    return "\n\n".join(categories.values())

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
"""
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(md_content)
