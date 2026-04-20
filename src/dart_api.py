import requests
import zipfile
import io
import xml.etree.ElementTree as ET

API_KEY = "6544dd16cd587e13be1a314b5cb6223644cdebff"

def get_corp_codes() -> list:
    url = "https://opendart.fss.or.kr/api/corpCode.xml"
    params = {"crtfc_key": API_KEY}
    res = requests.get(url, params=params)
    
    # ZIP 압축 해제
    with zipfile.ZipFile(io.BytesIO(res.content)) as z:
        with z.open("CORPCODE.xml") as f:
            tree = ET.parse(f)
            root = tree.getroot()
    
    # 기업 목록 파싱
    corps = []
    for item in root.findall("list"):
        corps.append({
            "corp_code": item.findtext("corp_code"),
            "corp_name": item.findtext("corp_name"),
            "stock_code": item.findtext("stock_code"),
        })
    
    return corps

if __name__ == "__main__":
    corps = get_corp_codes()
    print(f"전체 기업 수: {len(corps)}")
    # 상장사만 필터 (stock_code 있는 것)
    listed = [c for c in corps if c["stock_code"].strip()]
    print(f"상장사 수: {len(listed)}")
    print("샘플:", listed[:3])