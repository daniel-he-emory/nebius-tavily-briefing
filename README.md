# Topic Briefing CLI

Enter a topic, get a short briefing with cited sources — built from Tavily (web search + extraction) and a hosted LLM (Nebius Token Factory by default, or OpenRouter) for synthesis.

## How it works

1. [Tavily Search](https://tavily.com) finds current sources on your topic.
2. [Tavily Extract](https://tavily.com) pulls full text from the top results.
3. An LLM synthesizes a short briefing, citing which source each claim came from.
4. The briefing and a numbered source list print to your terminal.

## Setup

### 1. Get API keys

- **Tavily**: sign up at https://app.tavily.com (free tier: 1,000 credits/month, no card required) and copy your API key from the dashboard.
- **Nebius Token Factory** (default provider): create an account at https://tokenfactory.nebius.com (sign in with Google or GitHub) and get an API key from the console's authentication section.
- **OpenRouter** (optional, `--provider openrouter`): sign up at https://openrouter.ai and get an API key from your dashboard. **Note: using OpenRouter does not satisfy the Nebius x NVIDIA Global AI Hackathon's eligibility rule** (submissions must run on Nebius Token Factory/AI Cloud with an NVIDIA model) — use the default `nebius` provider for that submission.

The default Nebius model (`nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`) was verified against a live account's model list and satisfies that hackathon's NVIDIA-model requirement. It reasons internally before answering, so the script requests a generous `max_tokens` budget. Override with `--model`, or `NEBIUS_MODEL`/`OPENROUTER_MODEL` env vars, if you'd rather use something else; run `client.models.list()` to see what's currently available on your account.

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

Edit `.env` and fill in `TAVILY_API_KEY` and `NEBIUS_API_KEY` (plus `OPENROUTER_API_KEY` if you'll use that provider). Never commit `.env` or paste real keys into chat — it's already excluded via `.gitignore`.

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
- `--provider {nebius,openrouter}` — which LLM provider to use (default: `nebius`)
- `--model MODEL_ID` — override the provider's default model

Example using OpenRouter instead:

```bash
python3 briefing.py "recent developments in fusion energy" --provider openrouter
```

## Cost notes

This app has no persistent server or provisioned resources — it only makes per-request API calls, billed as Tavily credits (search + extract) and LLM tokens (chat completion, via whichever provider you select). There's nothing to shut down between runs; just watch your credit/token balance in each product's console.
