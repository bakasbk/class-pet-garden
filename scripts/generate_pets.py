#!/usr/bin/env python3
"""
宠物图片批量生成工具 - 使用 SiliconFlow FLUX.1-schnell 模型

用法:
    python generate_pets.py --preview --pet cat --level 3    # 预览Prompt
    python generate_pets.py --pet cat --level 3              # 生成单张
    python generate_pets.py --pet cat                       # 生成某宠物所有等级
    python generate_pets.py --all                           # 生成所有

"""

import argparse
import json
import os
import sys
import time
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


# ============ 配置 ============

MODELS = {
    "flux": "black-forest-labs/FLUX.1-schnell",
    "flux-dev": "black-forest-labs/FLUX.1-dev", 
    "flux-pro": "black-forest-labs/FLUX.1-pro",
}

DEFAULT_MODEL = "flux"
DEFAULT_SIZE = "512x512"
OUTPUT_DIR = Path("/root/.openclaw/workspace/projects/class-pet-garden/public/pets")

# ============ 宠物定义（测试用：cat, dog） ============

PETS = {
    "cat": {
        "name": "小猫",
        "base_prompt": "cute fluffy cat with big round eyes, pink nose, soft fur",
        "color": "orange and white",
        "features": "fluffy tail, whiskers"
    },
    "dog": {
        "name": "小狗",
        "base_prompt": "cute friendly dog with floppy ears, wagging tail",
        "color": "golden brown",
        "features": "floppy ears, shiny eyes"
    }
}

# ============ 优化后的等级定义 - 强调形态变化 ============

LEVELS = {
    1: {
        "body": "tiny body, smallest size, chibi proportions 1:1 head-to-body ratio",
        "features": "round baby face, oversized head, tiny limbs, fluffy baby fur",
        "expression": "innocent curious eyes, small smile",
        "background": "peaceful meadow with small flowers, morning sunlight",
        "effects": "soft pastel colors"
    },
    2: {
        "body": "small body, slightly bigger, chibi proportions 1:1.5 head-to-body ratio",
        "features": "playful stance, developing muscles, energetic posture",
        "expression": "excited happy eyes, open mouth smile",
        "background": "colorful garden with butterflies, bright sunny day",
        "effects": "vibrant colors"
    },
    3: {
        "body": "medium body, adolescent build, proportions 1:2 head-to-body ratio",
        "features": "lean athletic build, confident stance, longer limbs",
        "expression": "confident determined eyes, smirk",
        "background": "enchanted forest with glowing mushrooms",
        "effects": "subtle magical aura, soft glow"
    },
    4: {
        "body": "medium-large body, young adult build, proportions 1:2.5 head-to-body ratio",
        "features": "strong muscular build, defined features, powerful stance",
        "expression": "focused intense eyes, determined expression",
        "background": "ancient forest with waterfall, magical atmosphere",
        "effects": "growing power aura, light particles"
    },
    5: {
        "body": "large body, fully developed, proportions 1:3 head-to-body ratio",
        "features": "muscular majestic build, impressive presence, full size",
        "expression": "wise commanding eyes, noble expression",
        "background": "mountain peak above clouds, rainbow",
        "effects": "power aura, glowing particles, energy effects"
    },
    6: {
        "body": "very large body, heroic build, proportions 1:3.5 head-to-body ratio",
        "features": "heavily muscular, heroic stance, shining coat",
        "expression": "heroic fierce eyes, commanding presence",
        "background": "floating islands in sky, golden sunset clouds",
        "effects": "golden halo, strong aura, floating particles"
    },
    7: {
        "body": "huge body, legendary build, proportions 1:4 head-to-body ratio",
        "features": "massive powerful build, regal posture, radiant appearance",
        "expression": "kingly majestic eyes, awe-inspiring presence",
        "background": "celestial temple in clouds, aurora borealis",
        "effects": "intense golden glow, crown-like halo, energy waves"
    },
    8: {
        "body": "massive body, divine proportions, 1:4.5 head-to-body ratio, largest size",
        "features": "god-like majestic build, ultimate form, divine radiance, floating above ground",
        "expression": "divine all-knowing eyes, transcendent presence, benevolent smile",
        "background": "cosmic realm with stars and nebula, heavenly gates",
        "effects": "radiant golden light beams, divine halo, floating sacred symbols, ethereal glow"
    }
}

STYLE = "flat cartoon style, kawaii, cute and friendly, big round eyes with highlights, soft rounded shapes, smooth outlines, no sharp edges, vibrant colors, high quality, detailed, masterpiece"
NEGATIVE = "ugly, deformed, noisy, blurry, distorted, bad anatomy, extra limbs, poorly drawn face, poorly drawn hands, realistic, scary, dark, violent, text, watermark"

def build_prompt(pet_id: str, level: int) -> str:
    """构建生成Prompt - 强调形态变化"""
    pet = PETS[pet_id]
    lvl = LEVELS[level]
    
    prompt = f"""A {pet['base_prompt']}, 
{lvl['body']},
{lvl['features']}, {pet['color']},
{lvl['expression']},
{STYLE},
standing pose, front view,
{lvl['background']},
{lvl['effects']},
8k, highly detailed"""
    
    return prompt

def get_api_key():
    with open("/root/.openclaw/openclaw.json") as f:
        config = json.load(f)
        return config.get('models', {}).get('providers', {}).get('siliconflow', {}).get('apiKey', '')

def generate(prompt: str):
    api_key = get_api_key()
    url = "https://api.siliconflow.cn/v1/images/generations"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": MODELS["flux"],
        "prompt": prompt,
        "negative_prompt": NEGATIVE,
        "image_size": "512x512",
        "num_images": 1,
        "seed": int(time.time()) % 1000000
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=60)
    return resp.json()

def download(url: str, path: Path):
    r = requests.get(url, stream=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true", help="预览Prompt")
    parser.add_argument("--pet", choices=["cat", "dog"], help="宠物")
    parser.add_argument("--level", type=int, choices=range(1,9), help="等级")
    args = parser.parse_args()
    
    if args.preview and args.pet and args.level:
        prompt = build_prompt(args.pet, args.level)
        print(f"\n📝 Prompt for {args.pet} Lv.{args.level}:\n")
        print(prompt)
        print()
        return
    
    if args.pet and args.level:
        prompt = build_prompt(args.pet, args.level)
        print(f"🎨 生成 {args.pet} Lv.{args.level}...")
        print(f"Prompt: {prompt[:100]}...")
        result = generate(prompt)
        if 'images' in result:
            url = result['images'][0]['url']
            path = OUTPUT_DIR / args.pet / f"lv{args.level}.png"
            download(url, path)
            print(f"✅ 已保存: {path}")
        else:
            print(f"❌ 失败: {result}")

if __name__ == "__main__":
    main()
