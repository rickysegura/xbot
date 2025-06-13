# XBot 🤖

An AI-powered social media agent for X (formerly Twitter) that creates engaging, human-like content and interacts naturally within the X ecosystem.

## 🌟 Features

- **Multi-Personality Content Generation**: Six distinct personality styles using Claude AI for diverse, human-like content
- **Viral Topic Targeting**: Trend-aware content creation across multiple categories
- **Intelligent Rate Limiting**: Built-in API management and compliance with X API guidelines
- **Automated Community Engagement**: Strategic replies and mentions handling
- **Human-like Conversational Patterns**: Modern slang integration and authentic interactions
- **Comprehensive Logging**: Detailed error handling and activity tracking

## 🏗️ Technical Stack

- **X API v2** (via Tweepy) - Social media interactions
- **Anthropic Claude API** - Natural language generation
- **Python 3.8+** - Core application
- **Advanced Personality Modeling** - Dynamic style switching
- **Rate Limiting Compliance** - X API guidelines adherence

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- X API Developer Account with API keys
- Anthropic Claude API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/xbot.git
   cd xbot
   ```

2. **Install dependencies**
   ```bash
   pip install tweepy anthropic python-dotenv
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   # X API Credentials
   TWITTER_BEARER_TOKEN=your_bearer_token_here
   TWITTER_CONSUMER_KEY=your_consumer_key_here
   TWITTER_CONSUMER_SECRET=your_consumer_secret_here
   TWITTER_ACCESS_TOKEN=your_access_token_here
   TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
   
   # Anthropic Claude API
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

4. **Run the bot**
   ```bash
   python bot.py
   ```

## 🎭 Personality Styles

XBot features six distinct personality types that create varied, engaging content:

- **Relatable Millennial**: Self-deprecating humor with modern slang and trending references
- **Philosophical Gen Z**: Deep thoughts in casual language with existential humor
- **Chaotic Optimist**: Unhinged positivity that treats disasters like adventures
- **Anxious Overthinker**: Relatable spiraling about everyday situations
- **Sarcastic Realist**: Dry humor with observational comedy
- **Chronically Online**: Extremely online behavior with meme-speak fluency

## 📊 Content Categories

The bot generates content across multiple viral topic categories:

- **Everyday Struggles**: Monday energy, adulting, social battery
- **Tech Life**: AI, phone addiction, algorithm awareness
- **Gen Culture**: Main character energy, NPC behavior, side quests
- **Work Life**: Remote work, meeting culture, corporate speak
- **Relationships**: Dating apps, green/red flags, love languages
- **Self Improvement**: Mental health, boundaries, therapy talk
- **Random Observations**: Airport thoughts, grocery store behavior
- **US Politics**: Current political tensions and debates
- **Health & Wellness**: Natural supplements, wellness trends
- **Entertainment**: Pop culture, music, celebrity news

## ⚙️ Configuration

### Rate Limiting
- Maximum 30 requests per hour (configurable)
- Automatic rate limit compliance
- 1-hour check intervals (configurable)

### Content Parameters
- Tweet length: 280 characters maximum
- Personality switching: 15% chance per tweet
- Engagement targeting: 5-100 likes, ≤20 replies

### Timing
- 60-second delays between major operations
- 30-second delays between replies
- 1-hour cycles in automated mode

## 🛡️ Safety & Compliance

- **API Rate Limiting**: Built-in compliance with X API guidelines
- **Content Filtering**: Appropriate content generation
- **Error Handling**: Comprehensive exception management
- **Logging**: Detailed activity and error logging
- **Respectful Engagement**: Strategic, value-adding interactions

## 📝 Usage Examples

### Manual Single Tweet
```python
from bot import XBot

bot = XBot()
tweet = bot.create_tweet("original")
if tweet:
    bot.post_tweet(tweet)
```

### Check and Reply to Mentions
```python
bot = XBot()
bot.check_mentions()
```

### Automated Mode
```python
bot = XBot()
bot.run_automated()  # Runs continuously
```

## 🔧 Customization

### Adding New Personalities
Extend the `personality_styles` dictionary in the `XBot` class:

```python
"your_personality": {
    "traits": "description of traits",
    "voice": "description of voice/tone",
    "hooks": ["common", "phrases", "used"]
}
```

### Adding New Topics
Extend the `viral_topics` dictionary:

```python
"your_category": [
    "topic one",
    "topic two",
    "topic three"
]
```

## 📊 Monitoring

The bot provides comprehensive logging:
- API connection status
- Content generation success/failure
- Rate limiting status
- Engagement metrics
- Error tracking

## ⚠️ Important Notes

- **Compliance**: Ensure compliance with X's Terms of Service and API policies
- **Rate Limits**: The bot respects API rate limits - modify `MAX_REQUEST_PER_HOUR` if needed
- **Content Review**: Monitor generated content to ensure it aligns with your brand/values
- **API Costs**: Claude API usage incurs costs - monitor your usage
- **Account Safety**: Use responsibly to avoid account restrictions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Ricky Segura**
- Website: [https://www.rickysegura.dev](https://www.rickysegura.dev)
- Email: hello@rickysegura.dev
- Location: Los Angeles, CA

## 🔮 Version

Current Version: **0.1.0-alpha**

## ⭐ Acknowledgments

- Built with [Tweepy](https://www.tweepy.org/) for X API integration
- Powered by [Anthropic Claude](https://www.anthropic.com/) for content generation
- Inspired by the need for authentic, engaging social media automation

---

**Disclaimer**: This bot is for educational and legitimate social media automation purposes. Users are responsible for ensuring compliance with platform terms of service and applicable laws.