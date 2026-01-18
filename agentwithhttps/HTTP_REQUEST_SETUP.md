# Setup Guide: QS Ranking Workflow (HTTP Request Method)

## Why This Version?

The OpenAI community node package doesn't exist or isn't compatible with your n8n version.
This workflow uses the built-in **HTTP Request node** instead - it works the same way!

## Step 1: Import the Workflow

1. Download **qs_ranking_http_request.json**
2. In n8n, click the **menu (...)** → **Import from File**
3. Select the file and import it

## Step 2: Add Your OpenAI API Key

You need to create a credential for the HTTP Request:

### Method A: Create HTTP Header Auth Credential

1. Go to **Settings** → **Credentials** (bottom left in n8n)
2. Click **"Create New Credential"**
3. Search for and select **"Header Auth"**
4. Fill in:
   - **Name**: `OpenAI API Key`
   - **Header Name**: `Authorization`
   - **Value**: `Bearer YOUR_API_KEY_HERE`
     - Replace `YOUR_API_KEY_HERE` with your actual OpenAI API key
     - Keep the word "Bearer " before your key!
5. Click **"Save"**

### Method B: Manually Add API Key to Node

1. Open the **"Query OpenAI API"** node in your workflow
2. Scroll to **Authentication** section
3. Select **"None"**
4. In **Headers** section, add:
   - Name: `Authorization`
   - Value: `Bearer YOUR_API_KEY_HERE`
5. Make sure **Content-Type** header is also there:
   - Name: `Content-Type`
   - Value: `application/json`

## Step 3: Get Your OpenAI API Key (If You Don't Have One)

1. Go to: https://platform.openai.com/api-keys
2. Sign up or log in
3. Click **"Create new secret key"**
4. Copy the key (starts with "sk-...")
5. Save it securely - you won't see it again!

## Step 4: Fix File Path

In the **"Read CSV"** node, the path is set to:
```
/home/node/.n8n-files/scopus_finlit_with_country.csv
```

Make sure your CSV file is there! If you haven't copied it yet:

```bash
# First, find your container name
docker ps

# Then copy the file (replace YOUR_CONTAINER with actual name)
docker exec YOUR_CONTAINER mkdir -p /home/node/.n8n-files
cd ~/Desktop/ADREA_FAZIO_STAGE
docker cp scopus_finlit_with_country.csv YOUR_CONTAINER:/home/node/.n8n-files/
```

## Step 5: Add Export Node

After the workflow processes, you need to export the results:

1. **Add "Spreadsheet File" node** at the end
2. Connect it after all batches complete
3. Set operation to **"Convert to CSV"**
4. After execution, click **"Download"** button to get your results

OR

1. **Add "Write Binary File" node**
2. Set filename: `/home/node/.n8n-files/output_with_rankings.csv`
3. After execution, retrieve file from Docker:
   ```bash
   docker cp YOUR_CONTAINER:/home/node/.n8n-files/output_with_rankings.csv ~/Desktop/
   ```

## How This Works

The HTTP Request node sends this to OpenAI:

```json
{
  "model": "gpt-3.5-turbo",
  "messages": [
    {
      "role": "user",
      "content": "Return ONLY the numeric QS World University Ranking 2026 for: [University Name]. Reply with just the number or NR if not ranked."
    }
  ],
  "temperature": 0.3,
  "max_tokens": 10
}
```

The response comes back with the ranking, which gets added to your "qs rank 2026" column.

## Testing

Before running on all 80,000 rows:

1. Create a test CSV with 5-10 rows
2. Copy it to `/home/node/.n8n-files/test.csv`
3. Update the "Read CSV" node path to `/home/node/.n8n-files/test.csv`
4. Run the workflow
5. Check the results
6. Once confirmed working, switch back to full file

## Troubleshooting

### Error: "Unauthorized" or "Invalid API Key"
- Check your API key is correct
- Make sure you included "Bearer " before the key
- Verify the key has credits in OpenAI dashboard

### Error: "Rate limit exceeded"
- Your OpenAI account has rate limits
- Reduce batch size to 5 in "Split In Batches" node
- Add a delay between requests (use Wait node)

### Error: "File not found"
- Verify file is in `/home/node/.n8n-files/`
- Run: `docker exec YOUR_CONTAINER ls -la /home/node/.n8n-files/`

## Cost Estimate

- ~80,000 API calls
- Using gpt-3.5-turbo
- ~10 tokens per request
- Cost: **$2-4 for entire dataset**

## Workflow Flow

```
Manual Trigger
    ↓
Read CSV File
    ↓
Parse CSV
    ↓
Split In Batches (10 rows)
    ↓
Query OpenAI API (HTTP Request)
    ↓
Add QS Rank Column
    ↓
Loop back to Split In Batches
    ↓
All done → Export results
```

---

This method is more reliable than community nodes and works on any n8n version!
