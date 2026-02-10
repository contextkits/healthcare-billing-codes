# Healthcare Billing Codes MCP Server

An MCP (Model Context Protocol) server that provides lookup and search capabilities for medical billing codes including CPT, ICD-10, and HCPCS codes.

## Features

- **Lookup billing codes**: Get detailed information about specific CPT, ICD-10, or HCPCS codes
- **Search by description**: Find codes by searching keywords in descriptions
- **Category information**: View code categories and typical reimbursement rates (where applicable)

## Tools

### `lookup_billing_code`
Look up information about a specific medical billing code.

**Parameters:**
- `code_type` (string, required): Type of code - "CPT", "ICD10", or "HCPCS"
- `code` (string, required): The billing code to look up

**Example:**
```json
{
  "code_type": "CPT",
  "code": "99213"
}
```

### `search_codes_by_description`
Search for billing codes by keyword in description.

**Parameters:**
- `keyword` (string, required): Keyword to search for
- `code_type` (string, optional): Filter by code type or "ALL" (default: "ALL")

**Example:**
```json
{
  "keyword": "diabetes",
  "code_type": "ICD10"
}
```

## Installation

### Prerequisites
- Python 3.10 or higher
- pip

### Setup

1. Clone this repository:
```bash
git clone https://github.com/yourusername/healthcare-billing-codes.git
cd healthcare-billing-codes
```

2. Install dependencies:
```bash
pip install -e .
```

3. Run the server:
```bash
python server.py
```

## Usage with Claude Desktop

Add to your Claude Desktop config file (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "healthcare-billing-codes": {
      "command": "python",
      "args": ["/path/to/healthcare-billing-codes/server.py"]
    }
  }
}
```

## Extending the Database

The current implementation includes a small sample database. To add more codes:

1. Edit the `BILLING_CODES` dictionary in `server.py`
2. Or connect to an external database/API in the lookup functions

### Example: Adding a new CPT code
```python
"99215": {
    "description": "Office visit, established patient, 40-54 minutes",
    "category": "Evaluation and Management",
    "typical_reimbursement": "$185-$260"
}
```

## Data Sources (for expansion)

To build a complete database, consider these public sources:
- **CMS.gov**: Medicare fee schedules
- **AMA CPT**: CPT code descriptions (requires license for commercial use)
- **CDC ICD-10**: Free ICD-10 code database
- **CMS HCPCS**: HCPCS code lists

## Legal Disclaimer

This tool is provided for reference purposes only. Users must verify all billing codes with official sources before use in actual medical billing. The authors assume no liability for billing errors or claim denials resulting from use of this tool.

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please submit pull requests or open issues on GitHub.

## Monetization Options

This server can be monetized as:
1. **Freemium model**: Basic codes free, comprehensive database paid
2. **API access**: Charge per lookup for commercial users
3. **White-label licensing**: License to EHR vendors or billing companies
4. **Data partnerships**: Partner with coding databases for official data

## Contact

For commercial licensing or data partnerships: your-email@example.com
