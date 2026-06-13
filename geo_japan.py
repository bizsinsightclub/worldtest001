# -*- coding: utf-8 -*-
"""
geo_japan.py
============
일본 도도부현 GeoJSON -> 17개 가상 구역 + 시고쿠로 매핑하고, 등각투영하여
SVG path 데이터를 만든다. (오프라인 실측 벡터 지도용)

- 데이터 소스: dataofjapan/land japan.geojson (47 도도부현, lon/lat MultiPolygon)
- 캐시: japan_pref.geojson (1회 다운로드)
- 네트워크/캐시 실패 시 None 반환 -> 템플릿이 폴백.
"""
import os
import json
import math
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "japan_pref.geojson")
URL = "https://raw.githubusercontent.com/dataofjapan/land/master/japan.geojson"

# JIS 도도부현 id -> 가상 구역 키 (홋카이도는 단일 현 = 한 구역; 오키나와47 제외)
PREF_TO_DISTRICT = {
    1: "Hokkaido",
    2: "Northern Tohoku", 5: "Northern Tohoku", 3: "Northern Tohoku",
    6: "Southern Tohoku", 4: "Southern Tohoku", 7: "Southern Tohoku",
    8: "Eastern Kanto", 9: "Eastern Kanto", 12: "Eastern Kanto",
    10: "Western Kanto", 11: "Western Kanto", 14: "Western Kanto",
    13: "Tokyo",
    19: "Eastern Chubu", 20: "Eastern Chubu", 22: "Eastern Chubu", 23: "Eastern Chubu",
    15: "Western Chubu", 16: "Western Chubu", 17: "Western Chubu",
    18: "Western Chubu", 21: "Western Chubu",
    26: "Kyoto", 27: "Osaka",
    25: "Northern Kinki", 28: "Northern Kinki",
    24: "Southern Kinki", 29: "Southern Kinki", 30: "Southern Kinki",
    31: "Eastern Chugoku", 33: "Eastern Chugoku",
    32: "Western Chugoku", 34: "Western Chugoku", 35: "Western Chugoku",
    36: "Shikoku", 37: "Shikoku", 38: "Shikoku", 39: "Shikoku",
    40: "Northern Kyushu", 41: "Northern Kyushu", 42: "Northern Kyushu", 44: "Northern Kyushu",
    43: "Southern Kyushu", 45: "Southern Kyushu", 46: "Southern Kyushu",
    # 47 오키나와 -> 제외
}

# 구역 색 (지역 식별용, 무채/세피아·한류 계열; 시고쿠는 봉인)
DISTRICT_COLOR = {
    "Hokkaido": "#5b6e7a",
    "Northern Tohoku": "#5e7468", "Southern Tohoku": "#6d7c5c",
    "Eastern Kanto": "#7d7448", "Western Kanto": "#8a6d4a", "Tokyo": "#b89243",
    "Eastern Chubu": "#6f7a5a", "Western Chubu": "#5c7470",
    "Kyoto": "#a8743f", "Osaka": "#9c5f53",
    "Northern Kinki": "#6a7a6e", "Southern Kinki": "#7a6a78",
    "Eastern Chugoku": "#5f7280", "Western Chugoku": "#6b6f82",
    "Northern Kyushu": "#7c6a4e", "Southern Kyushu": "#84654a",
    "Shikoku": "#4a2230",
}

# 등각투영 윈도 (오키나와·오가사와라 제외, 본토 중심)
LON0, LON1 = 128.0, 146.5
LAT0, LAT1 = 30.0, 46.0
LATMID = 38.0
VIEW_W = 900.0


def fetch_geojson():
    if os.path.exists(CACHE):
        try:
            with open(CACHE, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    try:
        data = urllib.request.urlopen(URL, timeout=30).read()
        with open(CACHE, "wb") as f:
            f.write(data)
        return json.loads(data)
    except Exception as e:
        print("!! GeoJSON 다운로드 실패:", e)
        return None


def _proj(lon, lat, W, H):
    xspan = (LON1 - LON0) * math.cos(math.radians(LATMID))
    yspan = (LAT1 - LAT0)
    x = (lon - LON0) * math.cos(math.radians(LATMID)) / xspan * W
    y = (LAT1 - lat) / yspan * H
    return x, y


def build_map():
    gj = fetch_geojson()
    if not gj:
        return None
    xspan = (LON1 - LON0) * math.cos(math.radians(LATMID))
    yspan = (LAT1 - LAT0)
    W = VIEW_W
    H = W * yspan / xspan

    prefs = []
    pts_by_district = {}
    for ft in gj["features"]:
        pid = ft["properties"].get("id")
        district = PREF_TO_DISTRICT.get(pid)
        if not district:
            continue
        geom = ft["geometry"]
        polys = geom["coordinates"] if geom["type"] == "MultiPolygon" \
            else [geom["coordinates"]]
        d = []
        acc = pts_by_district.setdefault(district, [])
        for poly in polys:
            for ring in poly:
                # 작은 섬(점 수 적음)도 그리되, 윈도 밖은 SVG가 클립
                pathpts = []
                for lon, lat in ring:
                    x, y = _proj(lon, lat, W, H)
                    pathpts.append("%.1f,%.1f" % (x, y))
                    if LON0 <= lon <= LON1 and LAT0 <= lat <= LAT1:
                        acc.append((x, y))
                if len(pathpts) >= 3:
                    d.append("M" + "L".join(pathpts) + "Z")
        prefs.append({"id": pid, "district": district, "d": "".join(d)})

    # 구역 라벨 위치 = 윈도 내 점들의 중앙값 근사
    districts = []
    for key, color in DISTRICT_COLOR.items():
        pts = pts_by_district.get(key, [])
        if pts:
            xs = sorted(p[0] for p in pts)
            ys = sorted(p[1] for p in pts)
            lx = xs[len(xs) // 2]
            ly = ys[len(ys) // 2]
        else:
            lx = ly = 0
        districts.append({"key": key, "color": color,
                          "sealed": key == "Shikoku",
                          "labelX": round(lx, 1), "labelY": round(ly, 1)})

    return {"viewW": round(W, 1), "viewH": round(H, 1),
            "prefs": prefs, "districts": districts}


if __name__ == "__main__":
    m = build_map()
    if m:
        print("viewBox: %sx%s  prefs:%d  districts:%d"
              % (m["viewW"], m["viewH"], len(m["prefs"]), len(m["districts"])))
        import collections
        c = collections.Counter(p["district"] for p in m["prefs"])
        print(dict(c))
