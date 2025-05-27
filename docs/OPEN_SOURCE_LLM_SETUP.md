# Open Source LLM Setup Guide

This guide explains how to set up free, open-source LLMs as fallback options for the Slide Generator.

## Option 1: Ollama (Recommended - Fully Local)

Ollama runs completely on your local machine, ensuring privacy and no API costs.

### Installation

1. **Install Ollama**:
   - macOS: `brew install ollama`
   - Linux: `curl -fsSL https://ollama.ai/install.sh | sh`
   - Windows: Download from [ollama.ai](https://ollama.ai)

2. **Start Ollama service**:
   ```bash
   ollama serve
   ```

3. **Pull a model** (choose one):
   ```bash
   # Mistral 7B - Best balance of quality and speed
   ollama pull mistral
   
   # Llama 2 7B - Good general purpose
   ollama pull llama2
   
   # Phi-2 - Smaller, faster model
   ollama pull phi
   ```

4. **Test the installation**:
   ```bash
   ollama run mistral "Hello, world!"
   ```

The LLMClient will automatically detect and use Ollama if it's running on `http://localhost:11434`.

## Option 2: HuggingFace Inference API (Free Tier)

HuggingFace offers a free tier for their inference API.

### Setup

1. **Create a HuggingFace account**: 
   Visit [huggingface.co](https://huggingface.co) and sign up

2. **Get an API token**:
   - Go to Settings → Access Tokens
   - Create a new token with "read" permissions

3. **Add to your `.env` file**:
   ```
   HUGGINGFACE_API_KEY=your_token_here
   ```

Note: Free tier has rate limits (about 1000 requests/month).

## Option 3: Together AI (Free Credits)

Together AI provides $25 in free credits for new users.

### Setup

1. **Sign up at** [together.ai](https://together.ai)
2. **Get your API key** from the dashboard
3. **Update the LLMClient** to include Together AI provider

## Priority Order

The LLMClient tries providers in this order:
1. OpenAI (if API key is set and valid)
2. Ollama (if running locally)
3. HuggingFace (if API key is set)
4. Fallback template content

## Performance Comparison

| Provider | Model | Speed | Quality | Cost |
|----------|-------|-------|---------|------|
| OpenAI | GPT-3.5 | Fast | Excellent | Paid |
| Ollama | Mistral 7B | Medium | Very Good | Free |
| Ollama | Llama 2 7B | Medium | Good | Free |
| HuggingFace | Mistral 7B | Slow | Very Good | Free (limited) |

## Troubleshooting

### Ollama not detected
- Check if Ollama is running: `curl http://localhost:11434/api/tags`
- Ensure you've pulled at least one model
- Check firewall settings

### Slow generation
- Local models require decent hardware (8GB+ RAM recommended)
- Consider using smaller models like `phi` for faster responses
- GPU acceleration significantly improves speed

### JSON parsing errors
- Some open-source models may not follow JSON format perfectly
- The client includes error handling and retry logic
- Fallback content ensures the app always works 