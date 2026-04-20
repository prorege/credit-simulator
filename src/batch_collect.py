import time
import pandas as pd
from financial import get_financial_statement, extract_key_metrics

if __name__ == "__main__":
    test_corps = [
        {"corp_code": "00126380", "corp_name": "삼성전자"},
        {"corp_code": "00164779", "corp_name": "SK하이닉스"},
        {"corp_code": "00401731", "corp_name": "카카오"},
        {"corp_code": "00164742", "corp_name": "현대차"},
        {"corp_code": "00215243", "corp_name": "LG전자"},
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
        else:
            print(f"{corp['corp_name']} 스킵: {result.get('message')}")
        time.sleep(0.3)

    df = pd.DataFrame(results)
    print(df[["corp_name", "부채비율(%)", "유동비율(%)", "ROA(%)", "영업이익률(%)"]])
    df.to_csv("../data/financial_2023.csv", index=False, encoding="utf-8-sig")
    print("CSV 저장 완료")