# Quick Reference Card

## Before You Start
☐ Get OpenAI API key from https://platform.openai.com/api-keys
☐ Add OpenAI credentials in n8n (Settings → Credentials)
☐ Mount CSV file in Docker volume
☐ Import workflow into n8n

## Key Settings to Update

### In n8n Workflow:
1. **Read CSV File node**
   - File Path: `/data/scopus_finlit_with_country.csv`

2. **OpenAI node**
   - Select your OpenAI credential
   - Model: `gpt-4-turbo-preview` or `gpt-3.5-turbo` (cheaper)

3. **Write CSV File node**
   - Output filename: `scopus_finlit_with_qs_ranking.csv`
   - Output path: `/data/` (or your preferred location)

## Docker Command (If not already running)

```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  -v ~/your-csv-folder:/data \
  n8nio/n8n
```

## Workflow Flow
```
CSV File → Parse → Batch (10 rows) → OpenAI Query → Add Ranking → Repeat → Save CSV
```

## Expected Runtime
- ~80,000 rows in your file
- Processing 10 rows at a time
- ~1-2 seconds per batch
- **Total: ~2-4 hours**

## Cost Estimate
- Model: GPT-4-turbo: ~$8-15 for full dataset
- Model: GPT-3.5-turbo: ~$2-4 for full dataset

## Output
Your original CSV + new column: **qs rank 2026**
- Contains: Numeric rank (e.g., "25", "150") or "NR" (Not Ranked)

## Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| File not found | Check volume mount and file path |
| API error | Verify OpenAI API key and credits |
| Slow processing | Normal for large dataset, let it run |
| Workflow stops | Check Docker logs, increase memory |
| Wrong results | Test with small sample first |

## Pro Tips
✓ Test with 10-20 rows first
✓ Monitor first few batches to ensure accuracy
✓ Keep n8n tab open (or use n8n webhook trigger)
✓ Check OpenAI usage dashboard to monitor costs
✓ Backup your original CSV before running

## Access n8n
URL: http://localhost:5678
Default login: Set during first launch
