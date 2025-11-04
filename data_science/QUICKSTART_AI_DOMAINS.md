# Quick Start Guide - AI Domain Finder

## Installation (30 seconds)

```bash
cd /Users/q/Projects/data_science
pip install -r requirements_ai_domain.txt
```

## Run Your First Search (1 minute)

### Test with 20 words:
```bash
python ai_domain_finder.py --limit 20
```

### Test with 50 words:
```bash
python ai_domain_finder.py --limit 50 --workers 3
```

### Full search (may take 30-60 minutes):
```bash
python ai_domain_finder.py
```

## Quick Test

Run the test suite to verify everything works:
```bash
python test_ai_domain_finder.py
```

## Common Commands

```bash
# Find 1-syllable words only
python ai_domain_finder.py --max-syllables 1 --limit 100

# Higher budget ($150 per domain)
python ai_domain_finder.py --max-price 150 --limit 100

# Fast parallel checking (10 workers)
python ai_domain_finder.py --workers 10 --limit 100

# Custom output file
python ai_domain_finder.py --output my_domains.json --limit 50
```

## What You Get

After running, you'll have:
- **JSON file**: `ai_domains_results.json` (detailed data)
- **Text file**: `ai_domains_results.txt` (readable report)

## Example Output

```
word: spark
  → sparkai.ai: $89.99
  → sparkai.com: $12.99
  → Total: $102.98

word: glow  
  → glowai.ai: $89.99
  → glowai.com: $12.99
  → Total: $102.98
```

## Tips

✅ **Start small**: Use `--limit 20` to test  
✅ **Be patient**: Full search can take 30+ minutes  
✅ **Verify domains**: Always double-check availability with registrar  
✅ **Check prices**: Prices are estimates, verify before buying  

## Need Help?

```bash
python ai_domain_finder.py --help
```

Or read the full [README_AI_DOMAIN_FINDER.md](README_AI_DOMAIN_FINDER.md)
