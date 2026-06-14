# -*- coding: utf-8 -*-
"""
package.py — 소유권 이전용 ZIP 생성
=================================
필요한 것만 추려서 재빌드 가능한 완전 패키지를 만든다.
  - 소스: build_wiki / wiki_template / geo_japan / translate_lorebook /
          classify_relations / battles / package
  - 데이터·캐시: lorebook_export, lorebook_ko, relation_types, battle_scenes, japan_pref
  - 산출물: lorebook-wiki.html, index.html
  - 문서: README, CLAUDE, design, tonemanner, lesson
  - 캐릭터 이미지: images/*.webp  (build_wiki 가 ./images 를 우선 인식)
중간 산출물(_ko_work 등)·임시 파일은 제외.
"""
import os
import sys
import shutil
import zipfile

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
STAGE = os.path.join(HERE, "_dist", "lorebook-wiki")
ZIP = os.path.join(HERE, "lorebook-wiki-package.zip")

FILES = [
    # 소스
    "build_wiki.py", "wiki_template.py", "geo_japan.py",
    "translate_lorebook.py", "classify_relations.py", "battles.py", "package.py",
    # 데이터·캐시
    "lorebook_export.json", "lorebook_ko.json", "relation_types.json",
    "battle_scenes.json", "japan_pref.geojson",
    # 산출물
    "lorebook-wiki.html", "index.html",
    # 문서
    "README.md", "CLAUDE.md", "design.md", "tonemanner.md", "lesson.md", ".gitignore",
]


def build_stage():
    if os.path.exists(STAGE):
        shutil.rmtree(STAGE)
    os.makedirs(STAGE)
    missing = []
    for f in FILES:
        src = os.path.join(HERE, f)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(STAGE, f))
        else:
            missing.append(f)
    # 이미지 동봉 -> ./images
    import build_wiki
    img_dir = build_wiki.IMG_DIR
    out_img = os.path.join(STAGE, "images")
    os.makedirs(out_img, exist_ok=True)
    n_img = 0
    if os.path.isdir(img_dir):
        for fn in os.listdir(img_dir):
            if fn.lower().endswith(".webp"):
                shutil.copy2(os.path.join(img_dir, fn), os.path.join(out_img, fn))
                n_img += 1
    return missing, n_img


def make_zip():
    if os.path.exists(ZIP):
        os.remove(ZIP)
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(STAGE):
            for fn in files:
                full = os.path.join(root, fn)
                arc = os.path.relpath(full, os.path.dirname(STAGE))
                z.write(full, arc)
    return os.path.getsize(ZIP)


if __name__ == "__main__":
    missing, n_img = build_stage()
    size = make_zip()
    shutil.rmtree(os.path.join(HERE, "_dist"), ignore_errors=True)
    print("패키지 생성: %s" % ZIP)
    print("  파일: %d, 이미지: %d장, 크기: %.1f MB"
          % (len(FILES) - len(missing), n_img, size / 1024 / 1024))
    if missing:
        print("  누락(무시): %s" % missing)
