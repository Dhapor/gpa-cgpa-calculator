#!/usr/bin/env python3
"""
Update usage statistics from Supabase database
This script is run by GitHub Actions daily to auto-commit stats
"""

import os
import sys
import requests
from datetime import datetime, timedelta
from collections import Counter

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

def fetch_stats():
    """Fetch usage stats from Supabase"""
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Error: SUPABASE_URL or SUPABASE_KEY not set")
        sys.exit(1)
    
    headers = {
        "apikey": SUPABASE_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        # Get all usage logs
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/usage_logs?select=*&order=timestamp.desc",
            headers=headers
        )
        response.raise_for_status()
        logs = response.json()
        
        # Calculate statistics
        total_actions = len(logs)
        
        # Count by user type
        user_types = [l.get('user_type', 'unknown') for l in logs]
        guest_actions = user_types.count('guest')
        registered_actions = user_types.count('registered')
        
        # Last 7 days
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        recent_logs = [l for l in logs if l.get('timestamp', '') > week_ago]
        last_week = len(recent_logs)
        
        # Last 30 days
        month_ago = (datetime.now() - timedelta(days=30)).isoformat()
        monthly_logs = [l for l in logs if l.get('timestamp', '') > month_ago]
        last_month = len(monthly_logs)
        
        # Most popular actions
        actions = [l.get('action', 'unknown') for l in logs]
        action_counts = Counter(actions)
        top_actions = action_counts.most_common(3)
        
        # Most popular pages
        pages = [l.get('page', 'unknown') for l in logs]
        page_counts = Counter(pages)
        top_pages = page_counts.most_common(3)
        
        return {
            'total': total_actions,
            'guest': guest_actions,
            'registered': registered_actions,
            'last_week': last_week,
            'last_month': last_month,
            'top_actions': top_actions,
            'top_pages': top_pages,
            'last_updated': datetime.now().strftime('%B %d, %Y at %H:%M UTC')
        }
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching from Supabase: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

def format_number(num):
    """Format number with commas"""
    return f"{num:,}"

def update_stats_file(stats):
    """Update STATS.md file with current statistics"""
    
    # Build top actions section
    actions_list = "\n".join([
        f"   - {action}: {count:,} times"
        for action, count in stats['top_actions']
    ]) if stats['top_actions'] else "   - No data yet"
    
    # Build top pages section
    pages_list = "\n".join([
        f"   - {page}: {count:,} visits"
        for page, count in stats['top_pages']
    ]) if stats['top_pages'] else "   - No data yet"
    
    content = f"""# 📊 CGPA Calculator - Live Usage Statistics

> **Last Updated:** {stats['last_updated']}  
> *Automatically updated daily via GitHub Actions*

---

## 🎯 Overall Engagement

| Metric | Count |
|--------|-------|
| **Total Actions** | **{format_number(stats['total'])}** |
| **Guest Users** | {format_number(stats['guest'])} |
| **Registered Users** | {format_number(stats['registered'])} |

---

## 📅 Recent Activity

| Period | Actions |
|--------|---------|
| **Last 7 Days** | {format_number(stats['last_week'])} |
| **Last 30 Days** | {format_number(stats['last_month'])} |

---

## 🔥 Most Popular Features

**Top Actions:**
{actions_list}

**Most Visited Pages:**
{pages_list}

---

## 📈 Growth Insights

- **Average daily usage:** {format_number(stats['total'] // max(1, (stats['total'] // 100)))} actions/day
- **Guest to Registered ratio:** {stats['guest']}:{stats['registered']}
- **Engagement rate:** {((stats['registered'] / max(1, stats['total'])) * 100):.1f}% registered users

---

## 🎓 About This Project

The **CGPA Calculator** is a comprehensive academic planning tool designed for Nigerian university students. It provides:

### ✨ Key Features
- 🚀 **Guest Mode** - Try instantly without signup
- 🔐 **User Accounts** - Save your academic history forever
- 📊 **GPA/CGPA Calculator** - Accurate calculations using 5.0 and 4.0 scales
- 🎯 **Grade Planning Tool** - Plan future semesters to reach target CGPA
- 📥 **Export Reports** - Download your academic transcripts
- 📚 **History Tracking** - View all past semesters organized by year

### 🛠️ Technology Stack
- **Frontend:** Streamlit (Python)
- **Database:** SQLite + Supabase
- **Authentication:** SHA-256 password hashing
- **Deployment:** Streamlit Cloud
- **CI/CD:** GitHub Actions

### 🌟 Impact
This tool helps students:
- Track academic progress over multiple years
- Make informed decisions about grade planning
- Maintain organized academic records
- Reduce CGPA calculation errors

---

## 📞 Get Started

Try the calculator: [Your App URL Here]

### For Students:
1. Click "Try it Now" for guest mode
2. Calculate your GPA instantly
3. Sign up to save your records

### For Developers:
- View source code in this repository
- Contribute improvements
- Report issues

---

## 📜 License & Credits

**Built with ❤️ by Datapsalm & Victoria**

📧 Contact: datapsalm@gmail.com

---

*This statistics page is automatically updated every 24 hours using GitHub Actions and Supabase. All data is anonymized and aggregated.*
"""
    
    try:
        with open('STATS.md', 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Successfully updated STATS.md")
        print(f"   Total actions: {format_number(stats['total'])}")
        print(f"   Last week: {format_number(stats['last_week'])}")
        print(f"   Last month: {format_number(stats['last_month'])}")
    except Exception as e:
        print(f"❌ Error writing STATS.md: {e}")
        sys.exit(1)

if __name__ == '__main__':
    print("🔄 Fetching usage statistics from Supabase...")
    stats = fetch_stats()
    print("📝 Updating STATS.md...")
    update_stats_file(stats)
    print("🎉 Done!")
