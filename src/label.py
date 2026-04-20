import pandas as pd

def make_risk_label(df: pd.DataFrame) -> pd.DataFrame:
    """재무지표 기반 부도위험 라벨 생성"""
    
    def score(row):
        risk = 0
        # 부채비율 200% 이상 → 위험
        if row["부채비율(%)"] and row["부채비율(%)"] > 200:
            risk += 1
        # 유동비율 100% 미만 → 위험
        if row["유동비율(%)"] and row["유동비율(%)"] < 100:
            risk += 1
        # ROA 마이너스 → 위험
        if row["ROA(%)"] and row["ROA(%)"] < 0:
            risk += 1
        # 영업이익률 마이너스 → 위험
        if row["영업이익률(%)"] and row["영업이익률(%)"] < 0:
            risk += 1
        # 2개 이상 해당 → 부도위험(1)
        return 1 if risk >= 2 else 0

    df["default"] = df.apply(score, axis=1)
    return df

if __name__ == "__main__":
    df = pd.read_csv("../data/financial_2023.csv")
    df = make_risk_label(df)
    print(df[["corp_name", "부채비율(%)", "ROA(%)", "default"]])
    df.to_csv("../data/financial_labeled.csv", index=False, encoding="utf-8-sig")
    print("저장 완료")