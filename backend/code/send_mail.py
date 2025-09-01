import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import markdown
from dotenv import load_dotenv
import os
import re

load_dotenv()

def add_inline_styles(html_content):
    """Add inline CSS styles to HTML elements for better email compatibility"""
    
    # Font stack with Verdana as primary choice
    font_stack = "Verdana, Geneva, Arial, sans-serif"
    
    # Style headings
    html_content = re.sub(r'<h1>(.*?)</h1>', 
                         f'<h1 style="font-family: {font_stack}; font-size: 28px; font-weight: bold; color: #333; margin: 20px 0 15px 0; line-height: 1.3;">\\1</h1>', 
                         html_content)
    html_content = re.sub(r'<h2>(.*?)</h2>', 
                         f'<h2 style="font-family: {font_stack}; font-size: 24px; font-weight: bold; color: #333; margin: 18px 0 12px 0; line-height: 1.3;">\\1</h2>', 
                         html_content)
    html_content = re.sub(r'<h3>(.*?)</h3>', 
                         f'<h3 style="font-family: {font_stack}; font-size: 20px; font-weight: bold; color: #333; margin: 16px 0 10px 0; line-height: 1.3;">\\1</h3>', 
                         html_content)
    
    # Style bold text
    html_content = re.sub(r'<strong>(.*?)</strong>', 
                         f'<strong style="font-family: {font_stack}; font-weight: bold; color: #333;">\\1</strong>', 
                         html_content)
    
    # Style lists
    html_content = re.sub(r'<ul>', 
                         f'<ul style="font-family: {font_stack}; margin: 10px 0; padding-left: 30px; line-height: 1.6;">', 
                         html_content)
    html_content = re.sub(r'<ol>', 
                         f'<ol style="font-family: {font_stack}; margin: 10px 0; padding-left: 30px; line-height: 1.6;">', 
                         html_content)
    html_content = re.sub(r'<li>', 
                         f'<li style="font-family: {font_stack}; margin: 5px 0;">', 
                         html_content)
    
    # Style blockquotes
    html_content = re.sub(r'<blockquote>', 
                         f'<blockquote style="font-family: {font_stack}; border-left: 4px solid #007acc; margin: 15px 0; padding-left: 15px; color: #666; font-style: italic; background-color: #f9f9f9; padding: 10px 15px;">', 
                         html_content)
    
    # Style paragraphs
    html_content = re.sub(r'<p>', 
                         f'<p style="font-family: {font_stack}; margin: 10px 0; line-height: 1.6; color: #333;">', 
                         html_content)
    
    # Style code blocks
    code_font_stack = "Monaco, Consolas, 'Courier New', monospace"
    html_content = re.sub(r'<code>', 
                         f'<code style="font-family: {code_font_stack}; background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px; color: #d14;">', 
                         html_content)
    
    return html_content

def send_an_email(text, send_to):
    # Gmail credentials
    sender_email = "starmaker.dileepnaidu@gmail.com"
    receiver_email = send_to
    password = os.getenv("GMAIL_MAIL_APP_PASSWORD")
    
    if not password:
        print("❌ Error: Gmail app password not found in environment variables")
        return

    # Convert Markdown → HTML with extensions
    html_content = markdown.markdown(text, extensions=['extra', 'nl2br'])
    
    # Add inline styles for better email compatibility
    html_content = add_inline_styles(html_content)
    
    # Wrap in a proper HTML structure with Verdana font
    html_content = f"""
    <html>
    <body style="font-family: Verdana, Geneva, Arial, sans-serif; font-size: 14px; line-height: 1.6; color: #333; margin: 20px;">
        {html_content}
    </body>
    </html>
    """

    # Create email
    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Mail from StarMaker!"

    # Attach plain text + HTML version
    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    server = None
    try:
        # Connect to Gmail SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Start TLS encryption
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("✅ Email sent successfully via Gmail!")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if server:
            server.quit()


if __name__ == "__main__":
    context = """
# Hello from Python! 🎉

This is a **Markdown email** sent via Gmail SMTP with proper formatting.

## Features that work:

- ✅ **Bold text** formatting
- ✅ Large headings and subheadings  
- ✅ Bulleted lists with proper spacing
- ✅ `Inline code` styling
- ✅ Emojis and special characters

### Code Example:
```python
print("Hello, World!")
```

> This blockquote should have a nice left border and background!

**Try it out** - the formatting should now display properly in your email client! 🚀
"""

    send_an_email(context, "dile2107@gmail.com")