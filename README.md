# CSV Contact Extractor

A simple web application that extracts first names and email addresses from CSV files.

## Features

- 📤 Upload multiple CSV files at once (batch processing)
- 🔍 Automatically detects first name and email columns
- ✅ Validates email addresses
- 📊 Provides detailed statistics and reports
- 💾 Download results in clean text format
- 🚀 Free to host and use

## Output Format

Each line contains: `FirstName Email`

Example:
```
John john@example.com
Sarah sarah@example.com
Michael michael@example.com
```
## CSV Requirements

Your CSV files should:
- Have a header row
- Contain a column for first names (e.g., "First Name", "Given Name", "Name")
- Contain a column for emails (e.g., "Email", "Email Address")
- Use valid email formats (name@domain.com)

The app automatically recognizes common column name variations.

## Support

If you encounter issues:
- Check that your CSV has proper headers
- Ensure email addresses are valid
- Verify columns contain the expected data
- Try with a smaller test file first

## License

Free to use and modify for any purpose.
