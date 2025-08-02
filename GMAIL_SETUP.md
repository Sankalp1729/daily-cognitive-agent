# 📧 Gmail Setup Guide for Real Email Integration

## 🔐 Setting Up Gmail App Password

To connect this application to your Gmail account and fetch real emails, you need to set up an **App Password** (not your regular Gmail password).

### Step 1: Enable 2-Factor Authentication

1. Go to your [Google Account settings](https://myaccount.google.com/)
2. Click on **"Security"** in the left sidebar
3. Under **"Signing in to Google"**, click on **"2-Step Verification"**
4. Follow the steps to enable 2-factor authentication

### Step 2: Generate App Password

1. Go back to [Google Account settings](https://myaccount.google.com/)
2. Click on **"Security"** in the left sidebar
3. Under **"Signing in to Google"**, click on **"App passwords"**
4. You may need to sign in again
5. Select **"Mail"** as the app and **"Other"** as the device
6. Enter a name like **"Daily Cognitive Agent"**
7. Click **"Generate"**
8. **Copy the 16-character password** (it will look like: `abcd efgh ijkl mnop`)

### Step 3: Use the App Password in the Application

1. Open the Daily Cognitive Agent application
2. In the sidebar, check the box **"🔗 Connect to Real Gmail"**
3. Enter your **App Password** (not your regular Gmail password)
4. Click **"🔗 Test Connection"** to verify it works
5. Click **"📬 Fetch Real Emails"** to get actual emails from your inbox

## 🔒 Security Notes

- **Never share your App Password** with anyone
- **App Passwords are different** from your regular Gmail password
- **You can revoke App Passwords** anytime from your Google Account settings
- **Each App Password is unique** and can only be used for the specific application

## 🚨 Troubleshooting

### "Authentication failed" error
- Make sure you're using the **App Password**, not your regular Gmail password
- Ensure 2-factor authentication is enabled
- Check that the App Password was generated correctly

### "Connection failed" error
- Check your internet connection
- Make sure Gmail IMAP is enabled in your Gmail settings
- Try generating a new App Password

### "No emails found" error
- Make sure you have emails in your Gmail inbox
- Check that the email address is correct
- Try fetching fewer emails (the app fetches the most recent ones)

## 📧 Email Account: blackhole01729@gmail.com

This application is configured to work with the email address **blackhole01729@gmail.com**. 

### To use a different email:
1. Edit the `email_fetcher.py` file
2. Change the email address in the `RealEmailFetcher` initialization
3. Generate an App Password for that email account

## 🎯 Features with Real Emails

When connected to real Gmail:
- ✅ **Real email content** instead of simulated data
- ✅ **Actual sender information** and timestamps
- ✅ **Real attachments** and message IDs
- ✅ **Live inbox data** from your Gmail account
- ✅ **Agent learns from real email patterns**

## 🔄 Switching Between Real and Simulated Emails

You can easily switch between real and simulated emails:
- **Check "🔗 Connect to Real Gmail"** for real emails
- **Uncheck it** to use simulated emails
- **Both modes work** with the same AI agent and learning system

## 📊 Privacy and Data

- **Emails are processed locally** on your machine
- **No emails are stored permanently** in the application
- **Agent learning data** is saved locally in JSON files
- **Your email credentials** are not stored or transmitted

---

**Need help?** Check the troubleshooting section above or refer to the main README.md file. 