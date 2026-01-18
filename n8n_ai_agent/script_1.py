
# Create a setup guide
setup_guide = """# N8N Workflow Setup Guide: QS Ranking 2026 Lookup

## Overview
This workflow reads your CSV file, extracts affiliations, uses OpenAI API to fetch QS World University Rankings 2026, and saves the results with a new "qs rank 2026" column.

## Prerequisites
1. Self-hosted n8n on Docker (✓ You have this)
2. OpenAI API key (you'll need to obtain this)
3. CSV file accessible to n8n

## Step-by-Step Setup Instructions

### 1. Get OpenAI API Key
- Go to: https://platform.openai.com/api-keys
- Sign up or log in
- Click "Create new secret key"
- Copy and save the key securely

### 2. Configure OpenAI Credentials in n8n
1. Open your n8n interface (typically http://localhost:5678)
2. Go to Settings → Credentials
3. Click "Create New Credential"
4. Select "OpenAI API"
5. Enter your API key
6. Save with a name like "OpenAI account"

### 3. Import the Workflow
1. In n8n, click "Add Workflow" → "Import from File"
2. Select the `qs_ranking_workflow.json` file
3. The workflow will be imported

### 4. Update File Path
In the "Read CSV File" node:
- Change the file path to match your CSV location in Docker
- Example: `/data/scopus_finlit_with_country.csv`
- If you mounted a volume, adjust the path accordingly

### 5. Link OpenAI Credentials
1. Click on the "OpenAI - Get QS Ranking" node
2. In the "Credential to connect with" dropdown
3. Select the OpenAI credential you created in Step 2

### 6. Configure Output Path
In the "Write CSV File" node:
- Set the output path where you want the result saved
- Default: `scopus_finlit_with_qs_ranking.csv`

## Workflow Details

### Node Breakdown:
1. **Read CSV File**: Loads your CSV file into n8n
2. **Convert to Text**: Converts binary data to readable text
3. **Extract CSV Data**: Prepares data for parsing
4. **Parse CSV**: Splits CSV into individual rows
5. **Split In Batches**: Processes 10 rows at a time (prevents API rate limits)
6. **OpenAI - Get QS Ranking**: Queries OpenAI for each affiliation's QS ranking
7. **Add Ranking to Row**: Adds the ranking to the row data
8. **Collect Results**: Accumulates all processed rows
9. **Create Final CSV**: Builds the final CSV with new column
10. **Write CSV File**: Saves the result

### API Prompt Design:
The workflow sends this prompt to OpenAI:
```
System: You are a helpful assistant that looks up QS World University Rankings 2026. 
        When given a university or institution name, respond with ONLY the numeric ranking.
        
User: What is the QS World University Ranking 2026 for [Affiliation Name]? 
      Reply with only the number or 'NR' if not ranked.
```

This ensures you get clean numeric responses like "25", "150", or "NR".

## Docker Volume Mounting (Important!)

To access your CSV file, you need to mount it in your n8n Docker container:

```bash
docker run -it --rm \\
  --name n8n \\
  -p 5678:5678 \\
  -v ~/.n8n:/home/node/.n8n \\
  -v /path/to/your/csv:/data \\
  n8nio/n8n
```

Or in docker-compose.yml:
```yaml
version: '3.8'

services:
  n8n:
    image: n8nio/n8n
    ports:
      - 5678:5678
    volumes:
      - ~/.n8n:/home/node/.n8n
      - /path/to/your/csv:/data
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=admin
```

## Cost Estimation

With ~80,000+ rows in your CSV:
- Using GPT-4-turbo-preview
- ~10 tokens per request
- Rate: ~$0.01 per 1K tokens (input)
- Estimated cost: **$8-15** for the entire dataset

To reduce costs:
- Change model to "gpt-3.5-turbo" in the OpenAI node (cheaper, still accurate)
- Process in smaller batches if testing

## Running the Workflow

1. Click "Execute Workflow" button
2. Monitor progress in the execution log
3. The workflow processes in batches of 10 to respect API rate limits
4. Completion time: ~2-4 hours for 80K rows (depends on API response time)
5. Output file will be saved to your specified location

## Troubleshooting

### Error: "File not found"
- Check the file path in "Read CSV File" node
- Ensure the volume is correctly mounted in Docker

### Error: "OpenAI API error"
- Verify your API key is correct
- Check you have credits in your OpenAI account
- Ensure rate limits aren't exceeded (batch size helps with this)

### Error: "Invalid credential"
- Re-link the OpenAI credential in the workflow node
- Ensure the credential name matches

### Workflow stops unexpectedly
- Check n8n logs: `docker logs n8n`
- May need to increase Docker memory allocation
- Consider reducing batch size in "Split In Batches" node

## Modifications

### To change batch size:
- Edit "Split In Batches" node
- Adjust "Batch Size" parameter (default: 10)
- Smaller = slower but safer for API limits
- Larger = faster but may hit rate limits

### To use different AI model:
- Edit "OpenAI - Get QS Ranking" node
- Change "Model" dropdown to:
  - "gpt-3.5-turbo" (cheaper)
  - "gpt-4" (more accurate but expensive)

### To add error handling:
- Add an "IF" node after OpenAI response
- Check if response is valid
- Route invalid responses to a separate error log

## Testing First

Before processing all 80K+ rows:
1. Create a test CSV with 10-20 rows
2. Run the workflow on the test file
3. Verify the output is correct
4. Then run on the full dataset

## Output Format

The output CSV will have all original columns PLUS:
- `qs rank 2026` - containing the ranking number or "NR" (Not Ranked)

Example:
```
EID,Authors,Affiliations,Title,Year,country,qs rank 2026
2-s2.0-123,John Doe,Harvard University,Study Title,2022,United States,3
2-s2.0-456,Jane Smith,Unknown College,Another Study,2022,USA,NR
```

## Support

If you encounter issues:
1. Check n8n community forum: https://community.n8n.io/
2. OpenAI API documentation: https://platform.openai.com/docs
3. Review n8n logs for specific error messages

---

Good luck with your research! This workflow will save you countless hours of manual lookup.
"""

with open('SETUP_GUIDE.md', 'w', encoding='utf-8') as f:
    f.write(setup_guide)

print("Setup guide created: SETUP_GUIDE.md")
print("\nFiles ready for use:")
print("1. qs_ranking_workflow.json - Import this into n8n")
print("2. SETUP_GUIDE.md - Complete setup instructions")
