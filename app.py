#!/usr/bin/env python3
"""Gradio web UI for generating sourced topic briefings."""

import os

import gradio as gr
from briefing import (
    PROVIDERS,
    BriefingError,
    extract_sources,
    generate_briefing,
    require_env,
    search_sources,
)
from dotenv import load_dotenv
from openai import OpenAI
from tavily import TavilyClient

load_dotenv()

provider = PROVIDERS["nebius"]


def generate_briefing_ui(topic, max_results, top_n):
    topic = (topic or "").strip()
    if not topic:
        return "Please enter a topic or question.", ""

    model = os.environ.get(provider["model_env"], provider["fallback_model"])

    try:
        tavily_key = require_env("TAVILY_API_KEY")
        llm_key = require_env(provider["api_key_env"])

        tavily_client = TavilyClient(api_key=tavily_key)
        openai_client = OpenAI(
            base_url=provider["base_url"],
            api_key=llm_key,
        )

        results = search_sources(tavily_client, topic, max_results)
        sources = extract_sources(tavily_client, results, top_n)
        briefing = generate_briefing(openai_client, model, topic, sources)
    except BriefingError as e:
        return str(e), ""

    sources_markdown = "\n".join(
        f"[{i}] [{source['url']}]({source['url']})"
        for i, source in enumerate(sources, start=1)
    )
    return briefing, sources_markdown


with gr.Blocks() as demo:
    gr.Markdown("# Topic Briefing")
    gr.Markdown("Powered by Nebius Token Factory + NVIDIA Nemotron + Tavily")

    topic_textbox = gr.Textbox(label="Topic or question")
    generate_button = gr.Button("Generate Briefing")

    with gr.Accordion("Advanced options", open=False):
        max_results_input = gr.Number(
            label="max_results",
            value=5,
            minimum=1,
            precision=0,
        )
        top_n_input = gr.Number(
            label="top_n",
            value=3,
            minimum=1,
            precision=0,
        )

    briefing_output = gr.Markdown()
    sources_output = gr.Markdown()

    generate_button.click(
        fn=generate_briefing_ui,
        inputs=[topic_textbox, max_results_input, top_n_input],
        outputs=[briefing_output, sources_output],
    )


if __name__ == "__main__":
    demo.queue()
    demo.launch()
