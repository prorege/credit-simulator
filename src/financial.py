import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("DART_API_KEY")

def get_financial_statement(corp_code: str, year: str, report_type: str = "11011") -> dict:
    url = "https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json"
    for fs_div in ["CFS", "OFS"]:
        params = {
            "crtfc_key": API_KEY,
            "corp_code": corp_code,
            "bsns_year": year,
            "reprt_code": report_type,
            "fs_div": fs_div,
        }
        res = requests.get(url, params=params)
        data = res.json()
        if data.get("status") == "000":
            return data
    return {"status": "999", "message": "CFS/OFS 모두 없음"}

def extract_key_metrics(data: list) -> dict:
    bs = {}
    is_ = {}
    for item in data:
        name = item.get("account_nm")
        amount = item.get("thstrm_amount", "0").replace(",", "").replace(" ", "").strip()
        try:
            value = int(amount)
        except:
            value = 0
        if item.get("sj_div") == "BS":
            bs[name] = value
        elif item.get("sj_div") in ("IS", "CIS"):
            is_[name] = value

    total_assets   = bs.get("자산총계", 0)
    total_liab     = bs.get("부채총계", 0)
    total_equity   = bs.get("자본총계", 0)
    current_assets = bs.get("유동자산", 0)
    current_liab   = bs.get("유동부채", 0)
    net_income     = (
        is_.get("당기순이익(손실)") or
        is_.get("당기순이익") or
        0
    )
    revenue   = is_.get("영업수익") or is_.get("매출액") or is_.get("수익(매출액)") or 0
    op_income = is_.get("영업이익") or is_.get("영업이익(손실)") or 0

    return {
        "부채비율(%)":    round(total_liab / total_equity * 100, 1) if total_equity else None,
        "유동비율(%)":    round(current_assets / current_liab * 100, 1) if current_liab else None,
        "ROA(%)":        round(net_income / total_assets * 100, 2) if total_assets else None,
        "영업이익률(%)":  round(op_income / revenue * 100, 2) if revenue else None,
        "자산총계(억)":   total_assets // 100000000,
        "당기순이익(억)": net_income // 100000000,
    }