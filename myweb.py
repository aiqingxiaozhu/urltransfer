
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LibreTV 配置订阅 Web 服务
运行后访问 http://localhost:5000/config 即可获取配置 JSON
用法: python libretv_config_server.py
"""

import json
from flask import Flask, Response, jsonify
import requests

app = Flask(__name__)

# 你的配置数据
config = {
    "name": "我的源列表",
    "version": 2,
    "sources": [
        {
            "name": "示例点播源",
            "url": "https://example.com/api.php/provide/vod",
            "detail": "https://example.com",
            "isAdult": False
        }
    ],
    "liveSources": [
        {
            "name": "示例直播源",
            "url": "https://example.com/list.m3u",
            "epg": "https://example.com/epg.xml.gz"
        }
    ]
}

def getWebConfig(webLink="https://pz.v88.qzz.io?format=2&source=jin18"):
    resp = requests.get("https://pz.v88.qzz.io?format=0&source=jin18")
    data = resp.json()  # resp.json() 直接拿到字典
    api_site = data['api_site']  # 取 api_site 字典
    sources = []
    for key, item in api_site.items():
        sources.append({
            "name": item.get("name", key),
            "url": item.get("api", ""),
            "detail": item.get("detail", ""),
            "isAdult": False
        })

    config = {
        "name": "mylist",
        "version": 2,
        "sources": sources,
        "liveSources": []
    }


    config["sources"]=sources
    print(config)
    print(type(config))
    return config

@app.route("/config")
def get_config():
    """返回完整的 LibreTV 配置 JSON"""
    return jsonify(config)


@app.route("/sources")
def get_sources():
    """仅返回 sources（点播源）"""
    jsondata=getWebConfig()
    print(jsondata)
    print(type(jsondata))
    return jsondata


@app.route("/live")
def get_live():
    """仅返回 liveSources（直播源）"""
    return jsonify(config["liveSources"])


@app.route("/")
def index():
    """首页提示"""
    return json.dumps({
        "message": "LibreTV 配置订阅服务",
        "endpoints": {
            "/config": "获取完整配置（sources + liveSources）",
            "/sources": "仅获取点播源",
            "/live": "仅获取直播源"
        }
    }, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    print(f"服务已启动: http://localhost:{port}")
    print(f"  - http://localhost:{port}/config   (完整配置)")
    print(f"  - http://localhost:{port}/sources  (点播源)")
    print(f"  - http://localhost:{port}/live     (直播源)")
    app.run(host="0.0.0.0", port=port, debug=False)