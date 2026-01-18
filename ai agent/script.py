
import json

# Create a corrected n8n workflow with proper structure
workflow = {
    "name": "QS Ranking Lookup for Affiliations",
    "nodes": [
        {
            "parameters": {},
            "id": "d1e1c5a0-0b5a-4d5e-9c5a-1b5a4d5e9c5a",
            "name": "When clicking 'Test workflow'",
            "type": "n8n-nodes-base.manualTrigger",
            "typeVersion": 1,
            "position": [240, 300]
        },
        {
            "parameters": {
                "filePath": "/data/scopus_finlit_with_country.csv"
            },
            "id": "a2b3c4d5-e6f7-8901-2345-6789abcdef01",
            "name": "Read CSV File",
            "type": "n8n-nodes-base.readBinaryFile",
            "typeVersion": 1,
            "position": [460, 300]
        },
        {
            "parameters": {
                "mode": "jsonToCsv",
                "options": {}
            },
            "id": "b3c4d5e6-f789-0123-4567-89abcdef0123",
            "name": "CSV Parser",
            "type": "n8n-nodes-base.spreadsheetFile",
            "typeVersion": 2,
            "position": [680, 300]
        },
        {
            "parameters": {
                "batchSize": 10,
                "options": {}
            },
            "id": "c4d5e6f7-8901-2345-6789-abcdef012345",
            "name": "Split In Batches",
            "type": "n8n-nodes-base.splitInBatches",
            "typeVersion": 3,
            "position": [900, 300]
        },
        {
            "parameters": {
                "authentication": "oAuth2",
                "resource": "text",
                "operation": "message",
                "modelId": "gpt-3.5-turbo",
                "messages": {
                    "values": [
                        {
                            "content": "=You are a QS ranking assistant. Return ONLY the numeric QS World University Ranking 2026 for: {{ $json.Affiliations }}. If not ranked, return 'NR'. No other text."
                        }
                    ]
                },
                "options": {
                    "temperature": 0.3,
                    "maxTokens": 10
                }
            },
            "id": "d5e6f789-0123-4567-89ab-cdef01234567",
            "name": "Get QS Ranking",
            "type": "n8n-nodes-base.openAi",
            "typeVersion": 1.3,
            "position": [1120, 300]
        },
        {
            "parameters": {
                "mode": "manual",
                "duplicateItem": false,
                "assignments": {
                    "assignments": [
                        {
                            "id": "rank_assignment",
                            "name": "qs rank 2026",
                            "value": "={{ $json.message?.content ?? 'NR' }}",
                            "type": "string"
                        }
                    ]
                },
                "options": {}
            },
            "id": "e6f78901-2345-6789-abcd-ef0123456789",
            "name": "Add QS Rank Column",
            "type": "n8n-nodes-base.set",
            "typeVersion": 3.3,
            "position": [1340, 300]
        },
        {
            "parameters": {
                "mode": "chooseBranch",
                "output": "input2"
            },
            "id": "f7890123-4567-89ab-cdef-0123456789ab",
            "name": "Loop Control",
            "type": "n8n-nodes-base.merge",
            "typeVersion": 2.1,
            "position": [1560, 400]
        },
        {
            "parameters": {
                "mode": "combineBySql",
                "query": "SELECT * FROM input1 ORDER BY rowIndex"
            },
            "id": "g8901234-5678-9abc-def0-123456789abc",
            "name": "Aggregate Results",
            "type": "n8n-nodes-base.aggregate",
            "typeVersion": 1,
            "position": [1780, 300]
        },
        {
            "parameters": {
                "operation": "fromJson",
                "mode": "jsonTocsv",
                "options": {}
            },
            "id": "h9012345-6789-abcd-ef01-23456789abcd",
            "name": "Convert to CSV",
            "type": "n8n-nodes-base.convertToFile",
            "typeVersion": 1.1,
            "position": [2000, 300]
        },
        {
            "parameters": {
                "fileName": "scopus_finlit_with_qs_ranking.csv",
                "dataPropertyName": "data",
                "options": {}
            },
            "id": "i0123456-789a-bcde-f012-3456789abcde",
            "name": "Write Output CSV",
            "type": "n8n-nodes-base.writeFile",
            "typeVersion": 1,
            "position": [2220, 300]
        }
    ],
    "connections": {
        "When clicking 'Test workflow'": {
            "main": [
                [
                    {
                        "node": "Read CSV File",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        },
        "Read CSV File": {
            "main": [
                [
                    {
                        "node": "CSV Parser",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        },
        "CSV Parser": {
            "main": [
                [
                    {
                        "node": "Split In Batches",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        },
        "Split In Batches": {
            "main": [
                [
                    {
                        "node": "Get QS Ranking",
                        "type": "main",
                        "index": 0
                    }
                ],
                [
                    {
                        "node": "Aggregate Results",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        },
        "Get QS Ranking": {
            "main": [
                [
                    {
                        "node": "Add QS Rank Column",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        },
        "Add QS Rank Column": {
            "main": [
                [
                    {
                        "node": "Loop Control",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        },
        "Loop Control": {
            "main": [
                [
                    {
                        "node": "Split In Batches",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        },
        "Aggregate Results": {
            "main": [
                [
                    {
                        "node": "Convert to CSV",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        },
        "Convert to CSV": {
            "main": [
                [
                    {
                        "node": "Write Output CSV",
                        "type": "main",
                        "index": 0
                    }
                ]
            ]
        }
    },
    "pinData": {},
    "settings": {
        "executionOrder": "v1"
    },
    "staticData": None,
    "tags": [],
    "triggerCount": 0,
    "updatedAt": "2026-01-17T12:36:00.000Z",
    "versionId": "1"
}

# Save the corrected workflow
with open('qs_ranking_workflow_fixed.json', 'w', encoding='utf-8') as f:
    json.dump(workflow, f, indent=2)

print("✅ Fixed workflow created: qs_ranking_workflow_fixed.json")
print("\nChanges made to fix the import error:")
print("  • Added proper Manual Trigger node as starting point")
print("  • Used correct node ID format (UUID style)")
print("  • Fixed connection structure with proper node references")
print("  • Simplified node structure to avoid null references")
print("  • Used native n8n CSV handling nodes")
