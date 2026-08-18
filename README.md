# Proxy-Fetcher 🔄

A lightweight and automated HTTP proxy fetcher that updates your proxy list every 3 hours using GitHub Actions. Get a fresh, validated list of working proxies without manual intervention.

![GitHub last commit](https://img.shields.io/github/last-commit/sayanpal514-hue/Proxy-Fetcher)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.7+-blue)

## ✨ Features

- **Automated Updates**: Fetches fresh proxies automatically every 3 hours
- **GitHub Actions Integration**: Runs completely on GitHub's free infrastructure
- **Multiple Sources**: Aggregates proxies from various public sources
- **Easy to Use**: Simple setup and straightforward usage
- **Low Maintenance**: Set it and forget it - automatic scheduling handles everything
- **Free & Open Source**: No paid subscriptions or API keys required
- **Always Available**: Accessible directly from your repository

## 📋 Prerequisites

- Python 3.7 or higher
- GitHub account
- Git

## 🚀 Quick Start

### Option 1: Fork & Use

1. **Fork this repository** to your GitHub account
2. The GitHub Actions workflow will **automatically enable** and start running
3. Access the proxy list at:
   ```
   https://raw.githubusercontent.com/sayanpal514-hue/Proxy-Fetcher/main/live.txt
   ```

### Option 2: Clone & Run Locally

```bash
# Clone the repository
git clone https://github.com/sayanpal514-hue/Proxy-Fetcher.git
cd Proxy-Fetcher

# Install dependencies (if any)
pip install -r requirements.txt

# Run the script manually
python main.py
```

## 📖 Usage

### Download Proxies with cURL

```bash
curl https://raw.githubusercontent.com/sayanpal514-hue/Proxy-Fetcher/main/live.txt
```

### Download with Python

```python
import requests

url = "https://raw.githubusercontent.com/sayanpal514-hue/Proxy-Fetcher/main/live.txt"
response = requests.get(url)

if response.status_code == 200:
    with open('live.txt', 'w') as f:
        f.write(response.text)
    print("Proxies downloaded successfully!")
else:
    print(f"Failed to fetch proxies: {response.status_code}")
```

### Using Proxies in Your Application

```python
import requests

# Read proxy list
with open('proxies.txt', 'r') as f:
    proxies_list = f.read().strip().split('\n')

# Use a random proxy
import random
proxy = random.choice(proxies_list)

proxies = {
    'http': f'http://{proxy}',
    'https': f'http://{proxy}',
}

response = requests.get('https://example.com', proxies=proxies, timeout=5)
print(response.text)
```

## 🔧 How It Works

### GitHub Actions Workflow

This project uses GitHub Actions to automate the proxy fetching process:

- **Schedule**: Runs every 3 hours (configurable)
- **Trigger**: Automated via workflow schedule
- **Process**:
  1. Fetches proxy lists from multiple public sources
  2. Validates proxy connectivity
  3. Removes duplicates and dead proxies
  4. Saves results to `live.txt`
  5. Auto-commits changes to the repository

### Proxy Sources

The fetcher aggregates proxies from multiple public sources including:
- Free proxy list databases
- Public proxy scrapers
- Community-contributed proxy lists

> **Note**: Quality and availability of proxies may vary. Always validate proxies before using them in production.

## 📋 File Structure

```
Proxy-Fetcher/
├── .github/
│   └── workflows/
│       └── main.yml    # GitHub Actions workflow configuration
├── main.py                       # Main proxy fetching script
├── live.txt                   # Generated proxy list (auto-updated)
├── requirements.txt              # Python dependencies
└── README.md                      # This file
```

## ⚙️ Configuration


### Customize Proxy Validation

Modify `main.py` to:
- Change timeout values
- Add proxy filtering criteria
- Include/exclude specific proxy types
- Adjust the number of proxies to fetch

## 📊 Proxy Format

The `live.txt` file contains proxies in the following format:

```
ip:port
192.168.1.1:8080
10.0.0.1:3128
203.0.113.42:9090
...
```

## ⚠️ Important Notes

### Legal & Ethical Considerations

- Use fetched proxies responsibly and legally
- Respect the terms of service of websites you access
- Don't use proxies for illegal activities
- Some websites may block or rate-limit proxy traffic
- Always verify you have permission to use these proxies

### Proxy Quality

- **Free Proxies**: Often unreliable and may be slow
- **Recommended Testing**: Test proxies before using them in production
- **Rotation**: Consider rotating proxies to avoid detection/blocking
- **Lifespan**: Proxies may stop working at any time

## 🛠️ Troubleshooting

### GitHub Actions Not Running

1. Check the "Actions" tab in your repository
2. Ensure the workflow file is correctly formatted (YAML syntax)
3. Verify GitHub Actions is enabled in Settings → Actions
4. Check the workflow logs for detailed error messages

### Empty Proxies List

- Public proxy sources may be temporarily unavailable
- Network connectivity issues
- Proxy validation may have filtered out all proxies
- Try re-running the workflow manually

### Accessing Proxies List

Make sure to replace `YOUR_USERNAME` with your actual GitHub username:
```
https://raw.githubusercontent.com/sayanpal514-hue/Proxy-Fetcher/main/live.txt
```

## 🔄 Manual Trigger

To manually run the proxy fetch workflow:

1. Go to your repository
2. Click on "Actions" tab
3. Select the workflow
4. Click "Run workflow" button

## 🤝 Contributing

Contributions are welcome! You can:

- Report issues or bugs
- Suggest improvements
- Add new proxy sources
- Improve proxy validation logic
- Optimize the fetching script

To contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit (`git commit -am 'Add improvement'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 💡 Use Cases

- **Web Scraping**: Rotate proxies to avoid IP bans
- **API Testing**: Test your API with different geographic locations
- **Data Collection**: Gather data from websites that restrict access
- **Bot Development**: Distribute requests across multiple IPs
- **Load Testing**: Simulate traffic from different sources
- **Research**: Analyze web content from different regions

## ⭐ Support

If you find this project useful, please consider:
- Giving it a star ⭐
- Forking and sharing with others
- Contributing improvements
- Opening issues for bugs or feature requests

## 📧 Contact & Support

For issues, questions, or suggestions:
- Open an issue in the GitHub repository
- Check existing issues for solutions
- Review the troubleshooting section above

## 🔐 Security Considerations

- **No Logging**: This script doesn't log your activities
- **No Personal Data**: No personal information is collected
- **Open Source**: All code is transparent and auditable
- **Local Execution**: GitHub Actions runs on GitHub's infrastructure only

## 🚀 Advanced Usage

### Integration with Other Tools

```bash
# Download and validate proxies
curl https://raw.githubusercontent.com/sayanpal514-hue/Proxy-Fetcher/main/live.txt| \
while read proxy; do
  curl -x "http://$proxy" https://httpbin.org/ip --max-time 5 && echo "✓ $proxy"
done
```


## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Python Requests Documentation](https://docs.python-requests.org/)
- [Proxy Protocol Information](https://en.wikipedia.org/wiki/Proxy_server)

---

**Last Updated**: 2026
**Status**: Active & Maintained

---

Made with ❤️ by [sayanpal514-hue](https://github.com/sayanpal514-hue)
