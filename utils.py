# Importing necessary modules and libraries
from flask import Flask, request, jsonify
import ipywidgets as widgets
from IPython.display import display
import json
import logging
import os
import re
import requests
import threading
import markdown
from typing import List, Dict, Any, Union
from together import Together
from contextlib import contextmanager
import subprocess
from weaviate.classes.query import Filter
import joblib
import pandas as pd
import time
import httpx
from openai import OpenAI, DefaultHttpxClient
from opentelemetry.trace import Status, StatusCode






def generate_with_single_input(
    prompt: str,
    role: str = 'user',
    top_p: float = None,
    temperature: float = None,
    max_tokens: int = 500,
    model: str = "meta-llama/Llama-3.2-3B-Instruct-Turbo",
    together_api_key=None,
    **kwargs
):
    """
    calls Together if TOGETHER_API_KEY is set; otherwise
    falls back to OpenAI if OPENAI_API_KEY is set. Returns the same JSON shape
    your code expects (client.chat.completions.create(...).model_dump()).
    """
    payload = {
        "model": model,
        "messages": [{'role': role, 'content': prompt}],
        "top_p": top_p,
        "temperature": temperature,
        "max_tokens": max_tokens,
        **kwargs
    }

    # Together, else fallback to OpenAI.
    try:
        if together_api_key:
            client = Together(api_key=together_api_key)
            return client.chat.completions.create(**payload).model_dump()

        if os.environ.get("TOGETHER_API_KEY"):
            client = Together(api_key=os.environ["TOGETHER_API_KEY"])
            return client.chat.completions.create(**payload).model_dump()

        # Fallback to OpenAI if set (map to a compatible chat model)
        if os.environ.get("OPENAI_API_KEY"):
            from openai import OpenAI  # import here to avoid hard dep if unused
            oai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
            oai_payload = {
                "model": "gpt-4o-mini",      # reasonable default
                "messages": payload["messages"],
                "max_tokens": max_tokens,
            }
            return oai.chat.completions.create(**oai_payload).model_dump()

        raise RuntimeError("No API key found. Set TOGETHER_API_KEY or OPENAI_API_KEY.")

    except Exception as e:
        raise Exception(f"Failed to get correct output from LLM call.\nException: {e}")



def generate_params_dict(
    prompt: str, 
    temperature: float = None, 
    role = 'user',
    top_p: float = None,
    max_tokens: int = 500,
    model: str = "meta-llama/Llama-3.2-3B-Instruct-Turbo"
):
    """
    Call an LLM with different sampling parameters to observe their effects.
    
    Args:
        prompt: The text prompt to send to the model
        temperature: Controls randomness (lower = more deterministic)
        top_p: Controls diversity via nucleus sampling
        max_tokens: Maximum number of tokens to generate
        model: The model to use
        
    Returns:
        The LLM response
    """
    
    # Create the dictionary with the necessary parameters
    kwargs = {"prompt": prompt, 'role':role, "temperature": temperature, "top_p": top_p, "max_tokens": max_tokens, 'model': model} 

    return kwargs


def generate_embedding(
    prompt: Union[str, List[str]],
    model: str = "BAAI/bge-base-en-v1.5",
    together_api_key=None,
    **kwargs
):
    """
    Embeddings via Together or OpenAI fallback.
    Returns a single vector for str input, or a list of vectors for list input—
    matching how your Flask /vectors endpoint uses it.
    """
    is_batch = isinstance(prompt, list)
    payload = {"model": model, "input": prompt, **kwargs}

    try:
        if together_api_key:
            client = Together(api_key=together_api_key)
            res = client.embeddings.create(**payload).model_dump()
            vectors = [d["embedding"] for d in res["data"]]
            return vectors if is_batch else vectors[0]

        if os.environ.get("TOGETHER_API_KEY"):
            client = Together(api_key=os.environ["TOGETHER_API_KEY"])
            res = client.embeddings.create(**payload).model_dump()
            vectors = [d["embedding"] for d in res["data"]]
            return vectors if is_batch else vectors[0]

        if os.environ.get("OPENAI_API_KEY"):
            from openai import OpenAI
            oai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
            # Use a solid OpenAI embedding model
            res = oai.embeddings.create(model="text-embedding-3-small", input=prompt).model_dump()
            vectors = [d["embedding"] for d in res["data"]]
            return vectors if is_batch else vectors[0]

        raise RuntimeError("No API key found. Set TOGETHER_API_KEY or OPENAI_API_KEY.")

    except Exception as e:
        raise Exception(f"Failed to get correct output from LLM call.\nException: {e}")





def print_object_properties(obj: Union[dict, list]) -> None:
    t = ''
    if isinstance(obj, dict):
        for x, y in obj.items():
            if x == 'article_content':
                t += f'{x}: {y[:100]}...(truncated)\n'
            elif x == 'main_vector':
                t += f'{x}: {y[:30]}...(truncated)\n'
            elif x == 'chunk':
                t += f'{x}: {y[:100]}...(truncated)\n'
            else:
                t += f'{x}: {y}\n'
    else:
        for l in obj:
            for x, y in l.items():
                if x == 'article_content':
                    t += f'{x}: {y[:100]}...(truncated)\n'
                elif x == 'main_vector':
                    t += f'{x}: {y[:30]}...(truncated)\n'
                elif x == 'chunk':
                    t += f'{x}: {y[:100]}...(truncated)\n'
                else:
                    t += f'{x}: {y}\n'
            t += "\n\n"
    print(t)







