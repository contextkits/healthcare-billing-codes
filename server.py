#!/usr/bin/env python3
"""
MCP Server: Healthcare Billing Codes
Provides lookup and information about medical billing codes (CPT, ICD-10, HCPCS)
"""

import asyncio
import json
from mcp.server import Server
from mcp.types import Tool, TextContent

# Sample billing codes data - in production, this would connect to a real database
BILLING_CODES = {
    "CPT": {
        "99213": {
            "description": "Office/outpatient visit, established patient, 20-29 minutes",
            "category": "Evaluation and Management",
            "typical_reimbursement": "$93-$130"
        },
        "99214": {
            "description": "Office/outpatient visit, established patient, 30-39 minutes",
            "category": "Evaluation and Management",
            "typical_reimbursement": "$131-$184"
        },
        "90837": {
            "description": "Psychotherapy, 60 minutes",
            "category": "Mental Health",
            "typical_reimbursement": "$120-$170"
        }
    },
    "ICD10": {
        "E11.9": {
            "description": "Type 2 diabetes mellitus without complications",
            "category": "Endocrine/Metabolic"
        },
        "I10": {
            "description": "Essential (primary) hypertension",
            "category": "Circulatory"
        },
        "M25.511": {
            "description": "Pain in right shoulder",
            "category": "Musculoskeletal"
        }
    },
    "HCPCS": {
        "J3490": {
            "description": "Unclassified drugs",
            "category": "Drug Administration"
        },
        "Q4081": {
            "description": "Injection, epoetin alfa, biosimilar",
            "category": "Biologics"
        }
    }
}

# Create MCP server
app = Server("healthcare-billing-codes")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="lookup_billing_code",
            description="Look up information about a medical billing code (CPT, ICD-10, HCPCS)",
            inputSchema={
                "type": "object",
                "properties": {
                    "code_type": {
                        "type": "string",
                        "enum": ["CPT", "ICD10", "HCPCS"],
                        "description": "Type of billing code"
                    },
                    "code": {
                        "type": "string",
                        "description": "The billing code to look up"
                    }
                },
                "required": ["code_type", "code"]
            }
        ),
        Tool(
            name="search_codes_by_description",
            description="Search for billing codes by description keyword",
            inputSchema={
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Keyword to search for in code descriptions"
                    },
                    "code_type": {
                        "type": "string",
                        "enum": ["CPT", "ICD10", "HCPCS", "ALL"],
                        "description": "Type of billing code to search (or ALL)"
                    }
                },
                "required": ["keyword"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls"""
    
    if name == "lookup_billing_code":
        code_type = arguments["code_type"]
        code = arguments["code"]
        
        if code_type in BILLING_CODES and code in BILLING_CODES[code_type]:
            code_info = BILLING_CODES[code_type][code]
            result = f"**{code_type} Code: {code}**\n\n"
            result += f"Description: {code_info['description']}\n"
            result += f"Category: {code_info['category']}\n"
            if 'typical_reimbursement' in code_info:
                result += f"Typical Reimbursement: {code_info['typical_reimbursement']}\n"
            result += "\n*Note: This is a reference tool. Verify all codes with official sources before use.*"
            return [TextContent(type="text", text=result)]
        else:
            return [TextContent(type="text", text=f"Code {code} not found in {code_type} database. This is a sample database with limited codes.")]
    
    elif name == "search_codes_by_description":
        keyword = arguments["keyword"].lower()
        code_type_filter = arguments.get("code_type", "ALL")
        
        results = []
        search_types = BILLING_CODES.keys() if code_type_filter == "ALL" else [code_type_filter]
        
        for code_type in search_types:
            if code_type in BILLING_CODES:
                for code, info in BILLING_CODES[code_type].items():
                    if keyword in info["description"].lower():
                        results.append(f"**{code_type}: {code}** - {info['description']}")
        
        if results:
            result_text = "**Search Results:**\n\n" + "\n".join(results)
            result_text += "\n\n*Note: This is a sample database. Use official sources for complete code information.*"
            return [TextContent(type="text", text=result_text)]
        else:
            return [TextContent(type="text", text=f"No codes found matching '{keyword}'")]
    
    return [TextContent(type="text", text="Unknown tool")]

async def main():
    """Run the MCP server"""
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
