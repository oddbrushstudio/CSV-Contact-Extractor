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

## How to Deploy to Streamlit Community Cloud (Free)

### Step 1: Create a GitHub Account
1. Go to https://github.com
2. Click "Sign up" and create a free account
3. Verify your email address

### Step 2: Create a New Repository
1. Click the "+" icon in the top right corner
2. Select "New repository"
3. Name it: `csv-contact-extractor`
4. Make it **Public** (required for free Streamlit hosting)
5. Click "Create repository"

### Step 3: Upload Files to GitHub
1. On your repository page, click "uploading an existing file"
2. Upload these two files:
   - `app.py`
   - `requirements.txt`
3. Click "Commit changes"

### Step 4: Deploy to Streamlit Community Cloud
1. Go to https://share.streamlit.io
2. Click "Sign in" and use your GitHub account
3. Click "New app"
4. Select your repository: `csv-contact-extractor`
5. Main file path: `app.py`
6. Click "Deploy!"

### Step 5: Get Your Live URL
- Wait 2-3 minutes for deployment to complete
- You'll get a URL like: `https://your-app-name.streamlit.app`
- Share this URL with anyone who needs to use the tool

## Local Development (Optional)

If you want to test locally before deploying:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Updating Your App

After deployment, any changes you push to GitHub will automatically update your live app:

1. Edit files locally
2. Push changes to GitHub
3. Streamlit will automatically redeploy (takes 1-2 minutes)

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
