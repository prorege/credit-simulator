import requests
import zipfile
import io
import xml.etree.ElementTree as ET
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("DART_API_KEY")

def get_corp_codes() -> list:
    url = "https://opendart.fss.or.kr/api/corpCode.xml"
    params = {"crtfc_key": API_KEY}
    res = requests.get(url, params=params)
    with zipfile.ZipFile(io.BytesIO(res.content)) as z:
        with z.open("CORPCODE.xml") as f:
            tree = ET.parse(f)
            root = tree.getroot()
    corps = []
    for item in root.findall("list"):
        corps.append({
            "corp_code": item.findtext("corp_code"),
            "corp_name": item.findtext("corp_name"),
            "stock_code": item.findtext("stock_code"),
        })
    return corps