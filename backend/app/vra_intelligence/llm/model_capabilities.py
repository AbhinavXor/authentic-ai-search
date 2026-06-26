"""
=========================================================
MODULE: Model Capabilities

Project:
Authentic AI Search

Engine:
VRA Intelligence

Purpose:
Central model capability registry.

Author:
Abhinav

Version:
1.0.0
=========================================================
"""


MODEL_CAPABILITIES = {

    "qwen3": {

        "type": "general",

        "strengths": [
            "chat",
            "reasoning",
            "qa"
        ],

        "priority": 1
    },

    "deepseek_r1": {

        "type": "reasoning",

        "strengths": [
            "reasoning",
            "math",
            "analysis"
        ],

        "priority": 1
    },

    "qwen2_5_coder": {

        "type": "coding",

        "strengths": [
            "coding",
            "debugging",
            "architecture"
        ],

        "priority": 1
    },

    "llava": {

        "type": "vision",

        "strengths": [
            "vision",
            "ocr",
            "image_analysis"
        ],

        "priority": 1
    },

    "gemini": {

        "type": "api",

        "strengths": [
            "research",
            "reasoning",
            "vision"
        ],

        "priority": 2
    },

    "openai": {

        "type": "api",

        "strengths": [
            "chat",
            "reasoning"
        ],

        "priority": 3
    },

    "claude": {

        "type": "api",

        "strengths": [
            "long_context",
            "reasoning"
        ],

        "priority": 4
    }
}