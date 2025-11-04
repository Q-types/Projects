# AI Domain Finder 🔍

A Python tool that identifies 1-2 syllable English words and checks if adding 'AI' to them results in available domain names (.ai and .com) that cost less than $100 each.

## Features

✅ **Syllable Detection**: Identifies English words with 1 or 2 syllables  
✅ **Domain Availability**: Checks both `.ai` and `.com` domain availability  
✅ **Price Verification**: Ensures domains are under $100 budget  
✅ **Concurrent Processing**: Multi-threaded domain checking for speed  
✅ **Multiple Fallbacks**: Works with or without optional libraries  
✅ **Detailed Reports**: JSON and text output formats  

## Requirements

- Python 3.7+
- Internet connection for domain checks

## Installation

1. **Clone or download the script**

2. **Install dependencies**:
```bash
pip install -r requirements_ai_domain.txt
```

Optional but recommended for best results:
```bash
pip install syllables nltk python-whois
```

3. **Download NLTK words corpus** (if using NLTK):
```python
import nltk
nltk.download('words')
```

## Usage

### Basic Usage

Check all 1-2 syllable words with default settings:
```bash
python ai_domain_finder.py
```

### Advanced Usage

**Test with limited words**:
```bash
python ai_domain_finder.py --limit 50
```

**Adjust maximum syllables**:
```bash
python ai_domain_finder.py --max-syllables 3
```

**Change price threshold**:
```bash
python ai_domain_finder.py --max-price 150.0
```

**Increase concurrent workers for faster checking**:
```bash
python ai_domain_finder.py --workers 10
```

**Custom output filename**:
```bash
python ai_domain_finder.py --output my_domains.json
```

**Combined options**:
```bash
python ai_domain_finder.py --max-syllables 2 --max-price 100 --workers 5 --limit 100
```

## Command Line Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--max-syllables` | int | 2 | Maximum syllables per word |
| `--max-price` | float | 100.0 | Maximum price per domain (USD) |
| `--workers` | int | 5 | Number of concurrent workers |
| `--limit` | int | None | Limit words to check (for testing) |
| `--output` | string | ai_domains_results.json | Output filename |

## Output

The script generates two files:

### 1. JSON Report (`ai_domains_results.json`)
Detailed machine-readable results including:
- Timestamp
- Search parameters
- Full domain data (availability, pricing, errors)

### 2. Text Report (`ai_domains_results.txt`)
Human-readable summary with:
- Available domain pairs
- Individual and total pricing
- Easy-to-scan format

## Example Output

```
==============================================================
AI Domain Finder
==============================================================

1. Loading English words...
   Loaded 15234 English words

2. Filtering by syllables (<= 2)...
   Found 4821 words with 2 or fewer syllables

3. Generating domain combinations...
   Generated 4821 domain pairs to check

4. Checking domain availability and pricing...
   (Max price: $100.0 per domain)
   (Using 5 workers)
   Progress: 10/4821
   Progress: 20/4821
   ...

5. Results Summary:
   Total words checked: 4821
   Available domain pairs: 127

==============================================================
Top 10 Available Domains:
==============================================================

glow:
  • glowai.ai - $89.99
  • glowai.com - $12.99
  → Total: $102.98

spark:
  • sparkai.ai - $89.99
  • sparkai.com - $12.99
  → Total: $102.98
```

## How It Works

### 1. Word Collection
- Uses NLTK word corpus (236,000+ words) if available
- Falls back to built-in word list if NLTK not installed
- Filters for alphabetic words between 3-10 characters

### 2. Syllable Counting
- Primary: Uses `syllables` library for accurate counting
- Fallback: Custom vowel-based algorithm
- Filters words by syllable count (default: ≤2)

### 3. Domain Generation
- Combines word + "ai" (e.g., "spark" → "sparkai")
- Generates both `.ai` and `.com` variants

### 4. Availability Check
- Primary: WHOIS lookup using `python-whois`
- Fallback: DNS resolution check
- Handles rate limiting with delays

### 5. Price Estimation
- Uses typical retail pricing for common TLDs:
  - `.com`: ~$12.99
  - `.ai`: ~$89.99
  - Other TLDs: Estimated
- Note: Actual prices vary by registrar

## Important Notes

### Pricing Accuracy
⚠️ **Domain prices are estimates** based on typical retail pricing. Actual prices vary by:
- Registrar (GoDaddy, Namecheap, etc.)
- Promotions and discounts
- Premium domain status
- Renewal vs. initial registration

Always verify pricing with your chosen registrar before purchase.

### Rate Limiting
The script includes built-in delays to avoid overwhelming WHOIS servers. Checking thousands of domains may take time.

### False Positives
Domain availability checks may occasionally have false positives/negatives due to:
- WHOIS server inconsistencies
- Recently registered domains not yet in WHOIS
- Registry-specific policies

Always verify availability through a registrar before attempting to purchase.

## Troubleshooting

### Missing Dependencies
```bash
pip install --upgrade requests python-whois syllables nltk
```

### NLTK Data Not Found
```python
import nltk
nltk.download('words')
```

### WHOIS Errors
If you encounter frequent WHOIS errors:
1. Reduce `--workers` to 1 or 2
2. Add delays between requests
3. Check your internet connection

### Permission Errors
On Unix systems, make the script executable:
```bash
chmod +x ai_domain_finder.py
```

## Performance Tips

1. **Start with `--limit`**: Test with 50-100 words first
2. **Adjust workers**: More workers = faster but may trigger rate limits
3. **Filter aggressively**: Use `--max-syllables 1` for very short words
4. **Cache results**: Save and reuse previous checks

## Customization

### Add Custom Word Lists
Modify the `get_english_words()` method to include custom words:

```python
def get_english_words(self) -> List[str]:
    custom_words = ['tech', 'code', 'data', 'cloud', 'cyber']
    return custom_words
```

### Change Domain Extensions
Modify the `generate_ai_domains()` method to check other TLDs:

```python
def generate_ai_domains(self, words: List[str]):
    domains = []
    for word in words:
        base = f"{word}ai"
        domains.append((word, f"{base}.ai", f"{base}.io"))  # Check .io instead
    return domains
```

### Adjust Price Estimates
Update the `typical_prices` dictionary in `check_domain_price()`:

```python
typical_prices = {
    'com': 15.00,  # Update prices
    'ai': 95.00,
    'io': 45.00,
}
```

## Use Cases

- 🚀 **Startup founders**: Find brandable domain names
- 💼 **Domain investors**: Identify available premium domains
- 🎨 **Branding agencies**: Generate domain ideas for clients
- 🤖 **AI companies**: Secure AI-themed domains
- 📊 **Market research**: Analyze domain availability trends

## Contributing

Contributions welcome! Areas for improvement:
- Integration with registrar APIs for real-time pricing
- Advanced syllable counting algorithms
- Support for more TLDs
- Database caching for faster re-runs
- Web interface

## License

This tool is provided as-is for educational and research purposes. Always comply with WHOIS server terms of service and registrar policies.

## Disclaimer

This tool provides estimates and availability information. Always verify:
- Domain availability through official registrars
- Current pricing and fees
- Trademark conflicts
- Domain history and reputation

Domain registration and ownership are subject to registrar terms and ICANN policies.

---

**Happy domain hunting! 🎯**
