import requests
import time
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

def get_ai_recommendation(prompt, system_message=None, temperature=0.7, retries=3, backoff=2):
    """
    Get AI recommendation from DeepSeek-V3.1 via OpenRouter

    Args:
        prompt (str): Your question or request for recommendation
        system_message (str): Optional context/role for the AI
        temperature (float): Creativity level (0.0-1.0)
        retries (int): Number of retries if request fails
        backoff (int): Seconds to wait before retry

    Returns:
        str: AI's response text (stripped)

    Raises:
        ImproperlyConfigured: If API key is missing
        Exception: For API request failures
    """
    api_key = getattr(settings, 'OPENROUTER_API_KEY', None)
    if not api_key:
        raise ImproperlyConfigured("OPENROUTER_API_KEY not found in Django settings")

    url = "https://openrouter.ai/api/v1/chat/completions"
    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": "deepseek/deepseek-chat-v3.1:free",
        "messages": messages,
        "temperature": temperature,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    for attempt in range(retries):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            return content.strip()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                # Too many requests, wait and retry
                wait_time = backoff ** attempt
                time.sleep(wait_time)
                continue
            raise Exception(f"OpenRouter API HTTP error: {e} | Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                time.sleep(backoff ** attempt)
                continue
            raise Exception(f"OpenRouter API request failed: {str(e)}")
        except (KeyError, IndexError) as e:
            raise Exception(f"Failed to parse API response: {str(e)}")

    # If all retries fail, return empty string
    return ""
