import streamlit as st
import pandas as pd
import io
import re

# Page configuration
st.set_page_config(
    page_title="CSV Contact Extractor",
    page_icon="📧",
    layout="centered"
)

# Title and description
st.title("📧 CSV Contact Extractor")
st.markdown("Upload one or multiple CSV files to extract first names and email addresses.")
st.markdown("---")

def find_column(df, possible_names):
    """Find a column by checking multiple possible header names (case-insensitive)"""
    df_columns_lower = {col.lower(): col for col in df.columns}
    
    for name in possible_names:
        if name.lower() in df_columns_lower:
            return df_columns_lower[name.lower()]
    return None

def is_valid_email(email):
    """Basic email validation"""
    if pd.isna(email) or not isinstance(email, str):
        return False
    # Basic regex pattern for email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))

def extract_contacts(uploaded_files):
    """Extract first names and emails from multiple CSV files"""
    
    all_contacts = []
    stats = {
        'total_files': len(uploaded_files),
        'total_rows': 0,
        'valid_entries': 0,
        'missing_firstname': 0,
        'missing_email': 0,
        'invalid_email': 0,
        'file_details': []
    }
    
    # Possible column names for first name
    firstname_variants = [
        'first name', 'firstname', 'first_name', 'given name', 
        'givenname', 'given_name', 'forename', 'name'
    ]
    
    # Possible column names for email
    email_variants = [
        'email', 'e-mail', 'email address', 'email_address', 
        'e-mail address', 'contact email', 'contact_email', 'mail'
    ]
    
    for idx, uploaded_file in enumerate(uploaded_files, 1):
        file_stats = {
            'filename': uploaded_file.name,
            'rows': 0,
            'valid': 0,
            'issues': []
        }
        
        try:
            # Read CSV file
            df = pd.read_csv(uploaded_file)
            file_stats['rows'] = len(df)
            stats['total_rows'] += len(df)
            
            # Find the appropriate columns
            firstname_col = find_column(df, firstname_variants)
            email_col = find_column(df, email_variants)
            
            if not firstname_col:
                file_stats['issues'].append("Could not identify first name column")
                stats['file_details'].append(file_stats)
                st.warning(f"⚠️ File '{uploaded_file.name}': Could not find first name column")
                continue
                
            if not email_col:
                file_stats['issues'].append("Could not identify email column")
                stats['file_details'].append(file_stats)
                st.warning(f"⚠️ File '{uploaded_file.name}': Could not find email column")
                continue
            
            # Extract data from each row
            for _, row in df.iterrows():
                firstname = row[firstname_col]
                email = row[email_col]
                
                # Handle missing first name
                if pd.isna(firstname) or str(firstname).strip() == '':
                    stats['missing_firstname'] += 1
                    continue
                
                # Handle missing or invalid email
                if pd.isna(email) or str(email).strip() == '':
                    stats['missing_email'] += 1
                    continue
                
                email_str = str(email).strip()
                
                if not is_valid_email(email_str):
                    stats['invalid_email'] += 1
                    continue
                
                # Add valid contact
                all_contacts.append({
                    'firstname': str(firstname).strip(),
                    'email': email_str,
                    'source_file': uploaded_file.name
                })
                stats['valid_entries'] += 1
                file_stats['valid'] += 1
            
            stats['file_details'].append(file_stats)
            
        except Exception as e:
            file_stats['issues'].append(f"Error reading file: {str(e)}")
            stats['file_details'].append(file_stats)
            st.error(f"❌ Error processing '{uploaded_file.name}': {str(e)}")
    
    return all_contacts, stats

def format_output(contacts):
    """Format contacts as 'FirstName Email' with one entry per line"""
    lines = []
    for contact in contacts:
        lines.append(f"{contact['firstname']} {contact['email']}")
    return '\n'.join(lines)

# File uploader
uploaded_files = st.file_uploader(
    "Choose CSV file(s)",
    type=['csv'],
    accept_multiple_files=True,
    help="Select one or more CSV files containing contact information"
)

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} file(s) uploaded")
    
    # Show uploaded file names
    with st.expander("📁 Uploaded Files"):
        for file in uploaded_files:
            st.text(f"• {file.name}")
    
    # Process button
    if st.button("🚀 Extract Contacts", type="primary", use_container_width=True):
        with st.spinner("Processing files..."):
            contacts, stats = extract_contacts(uploaded_files)
            
            if contacts:
                # Display statistics
                st.markdown("### 📊 Extraction Summary")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Files", stats['total_files'])
                with col2:
                    st.metric("Total Rows", stats['total_rows'])
                with col3:
                    st.metric("Valid Entries", stats['valid_entries'])
                
                if stats['missing_firstname'] > 0 or stats['missing_email'] > 0 or stats['invalid_email'] > 0:
                    st.markdown("#### ⚠️ Issues Found")
                    issue_col1, issue_col2, issue_col3 = st.columns(3)
                    with issue_col1:
                        if stats['missing_firstname'] > 0:
                            st.metric("Missing First Name", stats['missing_firstname'])
                    with issue_col2:
                        if stats['missing_email'] > 0:
                            st.metric("Missing Email", stats['missing_email'])
                    with issue_col3:
                        if stats['invalid_email'] > 0:
                            st.metric("Invalid Email", stats['invalid_email'])
                
                # Show per-file details
                with st.expander("📄 Details by File"):
                    for file_stat in stats['file_details']:
                        st.markdown(f"**{file_stat['filename']}**")
                        st.text(f"  Rows processed: {file_stat['rows']}")
                        st.text(f"  Valid entries: {file_stat['valid']}")
                        if file_stat['issues']:
                            for issue in file_stat['issues']:
                                st.text(f"  ⚠️ {issue}")
                        st.markdown("---")
                
                # Format output
                output_text = format_output(contacts)
                
                # Display preview
                st.markdown("### 👀 Preview (first 10 entries)")
                preview_lines = output_text.split('\n')[:10]
                st.code('\n'.join(preview_lines), language=None)
                
                if len(contacts) > 10:
                    st.info(f"... and {len(contacts) - 10} more entries")
                
                # Download button
                st.markdown("### 💾 Download Results")
                st.download_button(
                    label="⬇️ Download Contact List",
                    data=output_text,
                    file_name="extracted_contacts.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                
            else:
                st.error("❌ No valid contacts found in the uploaded files. Please check your CSV format.")
                st.info("💡 Make sure your CSV files contain columns with headers like 'First Name' and 'Email'")

else:
    # Instructions when no files are uploaded
    st.info("👆 Upload one or more CSV files to get started")
    
    st.markdown("### ℹ️ How it works")
    st.markdown("""
    1. **Upload** one or multiple CSV files containing contact information
    2. **Click** the Extract Contacts button
    3. **Download** your formatted contact list
    
    The tool will automatically identify columns containing:
    - First names (looks for: First Name, Given Name, Name, etc.)
    - Email addresses (looks for: Email, Email Address, E-mail, etc.)
    
    **Output format:** Each line contains `FirstName Email`
    """)
    
    st.markdown("### ✅ Requirements")
    st.markdown("""
    - CSV files must have header rows
    - Files must contain identifiable first name and email columns
    - Email addresses must be in valid format (e.g., name@domain.com)
    """)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")
