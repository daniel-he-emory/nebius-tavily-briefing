# Topic Briefing CLI

Enter a topic, get a short briefing with cited sources — built from Tavily (web search + extraction) and Nebius Token Factory (hosted LLM synthesis).

## How it works

1. [Tavily Search](https://tavily.com) finds current sources on your topic.
2. [Tavily Extract](https://tavily.com) pulls full text from the top results.
3. A [Nebius Token Factory](https://tokenfactory.nebius.com) model synthesizes a short briefing, citing which source each claim came from.
4. The briefing and a numbered source list print to your terminal.

## Setup

### 1. Get API keys

- **Tavily**: sign up at https://app.tavily.com (free tier: 1,000 credits/month, no card required) and copy your API key from the dashboard.
- **Nebius Token Factory**: create an account at https://tokenfactory.nebius.com (sign in with Google or GitHub) and get an API key from the console's authentication section.

The default model in this script (`nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`) was verified against a live account's model list and satisfies the Nebius x NVIDIA Global AI Hackathon requirement that submissions use at least one NVIDIA open source model. It reasons internally before answering, so the script requests a generous `max_tokens` budget. Override with `--model` or a `NEBIUS_MODEL` env var if you'd rather use something else; run `client.models.list()` to see what's currently available on your account.

### 2. Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure keys

```bash
cp .env.example .env
```

Edit `.env` and fill in `TAVILY_API_KEY` and `NEBIUS_API_KEY`. Never commit `.env` or paste real keys into chat — it's already excluded via `.gitignore`.

## Usage

```bash
python3 briefing.py "recent developments in fusion energy"
```

Or run with no argument to be prompted interactively:

```bash
python3 briefing.py
```

Options:

- `--max-results N` — number of Tavily search results to fetch (default: 5)
- `--top-n N` — number of top results to extract full text from (default: 3)
- `--model MODEL_ID` — override the Nebius model used for synthesis

## Cost notes

This app has no persistent server or provisioned resources — it only makes per-request API calls, billed as Tavily credits (search + extract) and Nebius tokens (chat completion). There's nothing to shut down between runs; just watch your credit/token balance in each product's console.
