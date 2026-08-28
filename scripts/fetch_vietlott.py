import json
import os
import re
import urllib.request

GAME_CODES = {
    'mega645': '645',
    'power655': '655',
    'lotto535': '535',
    'max3d': '3d',
    'max3dplus': '3dplus',
    'max3dpro': '3dpro',
}

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
        ' like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ),
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://vietlott.vn/',
}


def parse_numbers(num_str):
  if not num_str:
    return []
  if isinstance(num_str, list):
    return num_str
  parts = re.split(r'[\s,|-]+', str(num_str).strip())
  return [int(p) if p.isdigit() else p for p in parts if p]


def fetch_game(game_type, code):
  url = f'https://vietlott.vn/api/front/kew-result-game-list?gameType={code}&page=1&limit=50'
  try:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
      data = json.loads(resp.read().decode('utf-8'))
      if isinstance(data, dict) and 'resultList' in data:
        return [
            {
                'id': f"#{item.get('DrawId', '0000')}",
                'date': item.get(
                    'DrawDate', item.get('DrawDateStr', 'Trực tiếp')
                ),
                'numbers': parse_numbers(item.get('ResultNumbers', '')),
            }
            for item in data['resultList']
        ]
  except Exception as e:
    print(f'Lỗi khi tải {game_type}: {e}')
    return None


def main():
  os.makedirs('data', exist_ok=True)
  for game_type, code in GAME_CODES.items():
    print(f'Đang tải {game_type}...')
    draws = fetch_game(game_type, code)
    if draws:
      out_path = f'data/{game_type}.json'
      with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(draws, f, ensure_ascii=False, indent=2)
      print(f'Đã lưu thành công: {out_path}')


if __name__ == '__main__':
  main()
