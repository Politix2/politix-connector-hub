# Data Directory

This directory is used for storing text files to be imported into the `plenary_sessions` table in Supabase.

## Importing Data

1. Add your text files to this directory. The importer supports various formats:
   - `.txt` files
   - `.md` files
   - `.csv` files
   - `.json` files
   - `.xml` files
   - Other text-based files

2. Run the data importer tool:
   ```bash
   cd /Users/thomaswagner/Work/politix-connector-hub/backend
   
   # For a dry run (simulation without actually writing to the database)
   python tools/data_importer.py --dry-run
   
   # For actual import
   python tools/data_importer.py
   
   # With verbose logging
   python tools/data_importer.py --verbose
   ```

## Command-line Options

The data importer tool supports the following options:

- `--dry-run`: Simulate the import process without actually writing to the database
- `--verbose`: Enable more detailed logging

## Example Data Structure

When files are imported, each file will be processed as follows:
- The entire file content will be stored in the `content` column
- The title will be extracted from the content if possible, or the filename will be used
- The current date/time will be used for the `date` field
- A UUID will be generated for the `id` field
- Additional metadata including file path, size, and import date will be stored in the `metadata` field

## Troubleshooting

- Ensure your database credentials are properly set in the `.env` file
- Make sure the `plenary_sessions` table exists in your Supabase database
- Check the script output for any errors during the import process
- Use the `--dry-run` option to verify what would be imported without making actual changes
- For encoding issues, the tool will attempt to use Latin-1 encoding if UTF-8 fails 