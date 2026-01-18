# Troubleshooting: Import Error Solution

## The Error You're Seeing
**Error**: "Cannot read properties of null (reading 'node')"

This happens when:
- The JSON structure doesn't match n8n's expected format
- Node references in connections are incorrect
- Missing required fields in the workflow JSON

## Solution: Use the Simplified Workflow

I've created a new file: **qs_ranking_workflow_simple.json** 

This is a minimal, clean version that should import without errors.

## How to Import the Simplified Version

### Option 1: Import via File (Recommended)
1. Download **qs_ranking_workflow_simple.json**
2. In n8n, click the **menu (...)** in top-right
3. Select **"Import from File"**
4. Choose the simplified JSON file
5. Click Open

### Option 2: Manual Build (If import still fails)
If you still get errors, build it manually in n8n:

**Step 1: Start Fresh**
- Create a new workflow in n8n
- Drag nodes from the left panel

**Step 2: Add These Nodes in Order**

1. **Manual Trigger** (to start the workflow)
   - Search: "Manual Trigger"
   - Just add it, no configuration needed

2. **Read Binary File**
   - Search: "Read Binary File"
   - File Path: `/data/scopus_finlit_with_country.csv`

3. **Convert to File**
   - Search: "Convert to File"
   - Operation: "Binary to JSON"
   - Options → Check "Header Row"

4. **Split In Batches**
   - Search: "Split In Batches"
   - Batch Size: 10

5. **OpenAI**
   - Search: "OpenAI"
   - Resource: "Text"
   - Operation: "Message"
   - Model: gpt-3.5-turbo
   - Message: `Return ONLY the numeric QS World University Ranking 2026 for: {{ $json.Affiliations }}. Reply with just the number or NR.`
   - Add your OpenAI credential

6. **Set (Edit Fields)**
   - Search: "Set" or "Edit Fields"
   - Click "Add Assignment"
   - Name: `qs rank 2026`
   - Value: `{{ $json.message.content }}`

**Step 3: Connect the Nodes**
- Connect them in order: Manual Trigger → Read → Convert → Split → OpenAI → Set
- Connect Set back to Split In Batches (creates a loop)

**Step 4: Add Output Node**
- Add **"Spreadsheet File"** node at the end
- Operation: "To CSV"
- Connect it after the last batch completes

## Why the Original Failed

The error "Cannot read properties of null" typically means:
- ❌ Node IDs were not in the right format
- ❌ Connections referenced nodes that n8n couldn't parse
- ❌ Some node properties had null values

The simplified version fixes this by:
- ✅ Using simple node IDs
- ✅ Minimal, essential connections
- ✅ Only required parameters
- ✅ No complex node structures

## Testing Your Setup

Once imported/built:

1. **Update File Path**
   - In "Read Binary File" node
   - Change path to match your Docker volume

2. **Add OpenAI Credential**
   - Click the OpenAI node
   - Select your API credential

3. **Test with Small Sample**
   - Before running on 80K rows
   - Test with a CSV containing 5-10 rows
   - Check the output format

4. **Execute Workflow**
   - Click "Execute Workflow"
   - Monitor the first batch
   - Verify rankings appear correctly

## Alternative: Copy-Paste Method

If import fails, you can manually copy node configurations:

1. Create each node type in n8n
2. Copy the "parameters" from the JSON
3. Paste into the node's parameter fields
4. Connect nodes manually

## Getting Your Results Out

After processing, add one of these nodes to export:

**Method 1: Download Results**
- Add "Spreadsheet File" node
- Set to "Convert to CSV"
- Click download button after execution

**Method 2: Write to File**
- Add "Write Binary File" node
- Set output path in your Docker volume
- File will be saved automatically

**Method 3: Google Sheets**
- Add "Google Sheets" node
- Configure to append rows
- Results go directly to spreadsheet

## Need Help?

If you're still having issues:
1. Share the exact error message
2. Check your n8n version (older versions may not support all nodes)
3. Try the manual build method above
4. Verify Docker volume permissions

The simplified workflow should work, but manual building is the most reliable method if JSON import continues to fail.
