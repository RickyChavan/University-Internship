
# Create a quick reference card
quick_ref = """# Quick Reference Card

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
docker run -it --rm \\
  --name n8n \\
  -p 5678:5678 \\
  -v ~/.n8n:/home/node/.n8n \\
  -v ~/your-csv-folder:/data \\
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
"""

with open('QUICK_REFERENCE.md', 'w', encoding='utf-8') as f:
    f.write(quick_ref)

print("✅ All files created successfully!\n")
print("=" * 60)
print("YOUR N8N WORKFLOW PACKAGE IS READY")
print("=" * 60)
print("\n📦 Files created:")
print("  1. qs_ranking_workflow.json    - Main workflow file")
print("  2. SETUP_GUIDE.md              - Detailed setup instructions")
print("  3. QUICK_REFERENCE.md          - Quick reference card")
print("\n🚀 Next Steps:")
print("  1. Get your OpenAI API key")
print("  2. Import the workflow into n8n")
print("  3. Configure the file paths")
print("  4. Test with a small sample")
print("  5. Run on full dataset")
print("\n💡 Important Notes:")
print("  • Your CSV has ~80,000+ rows")
print("  • Processing will take 2-4 hours")
print("  • Estimated cost: $2-15 (depends on model choice)")
print("  • Always test with sample data first!")
print("\n📚 Read SETUP_GUIDE.md for complete instructions")
