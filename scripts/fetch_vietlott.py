import requests
import json
import os

def fetch_data(game_code, file_name):
    url = f"https://vietlott.vn/api/front/kew-result-game-list?gameType={game_code}&page=1&limit=50"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
        "Accept": "application/json, text/plain, */*"
    }
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json()
            if "resultList" in data and len(data["resultList"]) > 0:
                os.makedirs("data", exist_ok=True)
                with open(f"data/{file_name}.json", "w", encoding="utf-8") as f:
                    json.dump(data["resultList"], f, ensure_ascii=False, indent=2)
                print(f"Đã lưu thành công {file_name}.json ({len(data['resultList'])} kỳ)")
    except Exception as e:
        print(f"Lỗi {file_name}: {e}")

fetch_data("645", "mega645")
fetch_data("655", "power655")
fetch_data("535", "lotto535")
fetch_data("3d", "max3d")
fetch_data("3dplus", "max3dplus")
fetch_data("3dpro", "max3dpro")
