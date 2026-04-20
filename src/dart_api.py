import requests
import zipfile
import io
import xml.etree.ElementTree as ET

API_KEY = "6544dd16cd587e13be1a314b5cb6223644cdebff"

# def get_corp_codes() -> list:
#     url = "https://opendart.fss.or.kr/api/corpCode.xml"
#     params = {"crtfc_key": API_KEY}
#     res = requests.get(url, params=params)
    
#     # ZIP 압축 해제
#     with zipfile.ZipFile(io.BytesIO(res.content)) as z:
#         with z.open("CORPCODE.xml") as f:
#             tree = ET.parse(f)
#             root = tree.getroot()
    
#     # 기업 목록 파싱
#     corps = []
#     for item in root.findall("list"):
#         corps.append({
#             "corp_code": item.findtext("corp_code"),
#             "corp_name": item.findtext("corp_name"),
#             "stock_code": item.findtext("stock_code"),
#         })
    
#     return corps

if __name__ == "__main__":
    # 알려진 대기업으로 먼저 테스트
    test_corps = [
        {"corp_code": "00126380", "corp_name": "삼성전자"},
        {"corp_code": "00164779", "corp_name": "SK하이닉스"},
        {"corp_code": "00401731", "corp_name": "카카오"},
        {"corp_code": "00247243", "corp_name": "현대차"},
        {"corp_code": "00108662", "corp_name": "LG전자"},
    ]

    results = []
    for corp in test_corps:
        result = get_financial_statement(corp["corp_code"], "2023")
        if result.get("status") == "000":
            metrics = extract_key_metrics(result["list"])
            metrics["corp_code"] = corp["corp_code"]
            metrics["corp_name"] = corp["corp_name"]
            results.append(metrics)
            print(f"{corp['corp_name']} ✓")

    import pandas as pd
    df = pd.DataFrame(results)
    print(df)
    df.to_csv("../data/financial_2023.csv", index=False, encoding="utf-8-sig")
    print("CSV 저장 완료")