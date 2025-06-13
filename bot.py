"""
XBot - An AI-Powered Social Media Agent for X (formerly Twitter)

A sophisticated autonomous bot that creates engaging, human-like content and 
interacts naturally within the X ecosystem. Built with advanced personality 
modeling and viral content strategies to maximize engagement and organic reach.

Key Features:
- Multi-personality content generation using Claude AI
- Viral topic targeting with trend-aware content creation
- Intelligent rate limiting and API management
- Automated community engagement through strategic replies
- Human-like conversational patterns and modern slang integration
- Comprehensive logging and error handling

Technical Stack:
- X API v2 (via Tweepy) for social media interactions
- Anthropic Claude API for natural language generation
- Advanced personality modeling with dynamic style switching
- Rate limiting compliance with X API guidelines

Author: Ricky Segura
Location: Los Angeles, CA
Date: June 2025
Contact: hello@rickysegura.dev
Website: https://www.rickysegura.dev

Version: 0.1.0-alpha
License: MIT
"""

# Imports
import tweepy
import anthropic
import os
import random
import time
import logging
from dotenv import load_dotenv
from typing import Optional, List, Any
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Config
TWEET_MAX_LENGTH = 280
MAX_REQUEST_PER_HOUR = 30
CHECK_INTERVAL = 3600 # 1 hour in seconds

# Init logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Main class
class XBot:
    def __init__(self):
        """ Init bot with API connections """
        self.setup_apis()
        self.last_request_time = datetime.now() - timedelta(hours=1)
        self.request_count = 0

        # Complex personality traits for more human-like content
        self.personality_styles = {
            "relatable_millennial": {
                "traits": "relatable, self-deprecating with humor, uses modern slang naturally, references current trends or memes, anxiety-ridden but makes it funny, perpetually tired but optimistic",
                "voice": "That friend who turns every mundane disaster into comedy gold while simultaneously having an existential crisis about it. Equal parts 'I'm fine' and 'everything is chaos' energy",
                "hooks": ["why is", "imagine being", "can we normalize", "tell me why", "nobody:", "brain at 3am:", "my anxiety said", "main character moment when"]
            },
            "philosophical_gen_z": {
                "traits": "deep thoughts in casual language, existential but funny, often about Gen Z life, chronically online wisdom, makes profound observations about mundane things, uses therapy speak casually",
                "voice": "That person who drops life-changing realizations in the middle of explaining why they cried at a TikTok. Accidentally wise while being completely unhinged",
                "hooks": ["no one prepared me for", "adulting is just", "society really said", "why did nobody tell me", "capitalism has us believing", "this is your reminder that", "plot twist:", "character development looks like", "the way we normalized"]
            },
            "chaotic_optimist": {
                "traits": "unhinged positivity, treats disasters like adventures, finds silver linings in everything, spontaneous energy, makes terrible decisions with full confidence",
                "voice": "That friend who shows up to your breakdown with snacks and a completely unhinged plan to fix your life. Radiates 'let's commit crimes but make it self-care' energy",
                "hooks": ["hear me out", "controversial opinion but", "plot armor activated", "main character energy:", "life hack nobody asked for:", "choosing violence today by", "the universe said", "intuition told me to"]
            },
            "anxious_overthinker": {
                "traits": "spirals about everything but makes it relatable, catastrophizes mundane situations, socially anxious but self-aware, turns internal monologue into content",
                "voice": "That person whose brain never stops running worst-case scenarios but somehow makes anxiety content that hits different. Professional overthinker with imposter syndrome",
                "hooks": ["tell me I'm not the only one who", "the way my brain immediately", "why do I always", "overthinking this but", "social anxiety really has me", "the mental gymnastics I just did", "brain said 'bet' and", "intrusive thoughts won today"]
            },
            "sarcastic_realist": {
                "traits": "dry humor, calls out absurdities, brutally honest but not mean, observational comedy, slightly cynical but not bitter, millennial exhaustion",
                "voice": "That friend who says what everyone's thinking but with perfect comedic timing. Equal parts 'I can't even' and 'but here we are anyway'",
                "hooks": ["the way society just", "imagine [situation] and thinking", "the bar is so low", "the audacity", "wild that we", "normalize calling out", "respectfully, what"]
            },
            "chronically_online": {
                "traits": "extremely online, references niche internet culture, speaks in memes, understands every platform's algorithm, digital native humor, irony poisoned but self-aware",
                "voice": "That person who treats real life like an extended meme and somehow makes it work. Lives in the space between sincere and ironic",
                "hooks": ["this app has me", "the algorithm said", "terminally online behavior:", "very demure very", "it's giving", "the way this", "core memory unlocked:", "no one asked but", "me to me:", "update: nobody cared", "live laugh love but make it", "pov: you're", "me when", "that's so"]
            }
        }

        # Viral content topics with high engagement potential
        self.viral_topics = {
            "everyday_struggles": [
                "monday morning energy",
                "weekend vs reality",
                "trying to adult",
                "social battery",
                "main character energy",
                "airport thoughts",
                "grocery store behavior"
            ],
            "tech_life": [
                "AI taking over",
                "phone addiction",
                "social media reality",
                "digital detox",
                "algorithm knows me",
                "AI Code Assistants"
            ],
            "gen_culture": [
                "plot armor in real life",
                "NPC behavior",
                "side quest energy",
                "character development",
                "memes and humor"
            ],
            "work_life": [
                "quiet quitting",
                "meeting culture",
                "email etiquette",
                "work from home",
                "corporate speak"
            ],
            "relationships": [
                "green flags",
                "red flags",
                "love languages",
                "attachment styles",
                "dating apps"
            ],
            "self_improvement": [
                "mental health",
                "boundaries",
                "therapy talk"
            ],
            "random_observations": [
                "airport thoughts",
                "grocery store behavior",
                "weather small talk",
                "public transport stories"
            ],
            "us_politics": [
                "California tensions",
                "Governor Newsom vs President Trump",
                "immigration debates",
                "National Guard deployment"
            ],
            "health_wellness": [
                "CBG Gummies",
                "Creatine Gummies",
                "natural supplements",
                "wellness trends"
            ],
            "entertainment_pop_culture": [
                "new music releases",
                "movie premieres",
                "celebrity news",
                "pop culture phenomena"
            ]
        }

        # Assign random personality on startup
        self.current_personality = random.choice(list(self.personality_styles.keys()))
    
    def setup_apis(self):
        """ Init X and Claude APIs """
        try:
            # Connect to X API
            self.client = tweepy.Client(
                bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
                consumer_key=os.getenv("TWITTER_CONSUMER_KEY"),
                consumer_secret=os.getenv("TWITTER_CONSUMER_SECRET"),
                access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
                access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
                wait_on_rate_limit=True
            )

            # Connect to Claude API
            self.claude = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

            # Test connections
            me = self.client.get_me()
            logger.info(f"Connected as: {me.data.username}")
        
        except Exception as e:
            logger.error(f"API init failed: {e}")
            raise
    
    def can_make_request(self) -> bool:
        """ Rate limit check """
        now = datetime.now()

        if now - self.last_request_time > timedelta(hours=1):
            self.request_count = 0
            self.last_request_time = now
        
        return self.request_count < MAX_REQUEST_PER_HOUR
    
    def create_tweet(self, tweet_type : str = "original", context : str = None) -> Optional[str]:
        """ Create a tweet using Claude """
        if not self.can_make_request():
            logger.warning("Rate limit reached")
            return None
        
        # Randomly switch personality for variety
        if random.random() < 0.15: # 15% chance
            self.current_personality = random.choice(list(self.personality_styles.keys()))
        
        current_style = self.personality_styles[self.current_personality]

        if tweet_type == "original":
            topic_category = random.choice(list(self.viral_topics.keys()))
            specific_topic = random.choice(self.viral_topics[topic_category])

            # Set system prompt for original tweets
            prompt = f"""
                Create an engaging original tweet about "{specific_topic}" in the {topic_category} category.

                PERSONALITY: {self.current_personality}
                Style: {current_style['traits']}
                Voice: {current_style['voice']}
                Preferred hooks: {', '.join(current_style['hooks'])}

                Viral content strategies:
                - Use conversational tone like texting a friend
                - Reference shared experiences everyone relates to
                - Include subtle self-deprecating humor
                - Make observations about everyday life
                - Use modern slang naturally (don't force it)
                - Create "main character" or "side quest" energy
                - Aim to evoke emotions like humor, surprise, or relatability
                - Reference current trends or popular topics if relevant to the specific topic
                - NO emojis - keep it purely text-based for authentic human feel
            
                Requirements:
                - Under {TWEET_MAX_LENGTH} characters
                - Highly relatable and shareable
                - Natural, conversational language
                - Sound like a friend would say it

                Return only the tweet text.
            """
        
        elif tweet_type == "reply" and context:
            prompt = f"""
                Someone tweeted: "{context}"
                PERSONALITY: {self.current_personality}
                Style: {current_style['traits']}
                Voice: {current_style['voice']}
                
                Create a thoughtful reply that:
                - Adds genuine value to the conversation
                - Shows authentic interest or shared experience
                - Under {TWEET_MAX_LENGTH} characters
                - Natural response from a friend
                - Encourages further engagement
                - Uses conversational tone
                - NO emojis - text only
                
                Return only the reply text.
            """
    
        else:
            return None
        
        # Attempt to generate tweet with prompt
        try:
            response = self.claude.messages.create(
                model = "claude-3-5-sonnet-20241022",
                max_tokens = 100,
                messages = [{"role" : "user", "content" : prompt}]
            )
            
            tweet = response.content[0].text.strip().strip('"')
            self.request_count += 1
            
            if len(tweet) > TWEET_MAX_LENGTH:
                tweet = tweet[:277] + "..."
            
            return tweet
            
        except Exception as e:
            logger.error(f"Content generation failed: {e}")
            return None
    
    def post_tweet(self, text : str) -> bool:
        """ Post a tweet """
        if not self.can_make_request():
            return False
        
        try:
            self.client.create_tweet(text = text)
            self.request_count += 1
            logger.info(f"Posted: {text}")
            return True
        except Exception as e:
            logger.error(f"Tweet posting failed: {e}")
            return False
    
    def check_mentions(self):
        """ Check for mentions and reply to them """
        if not self.can_make_request():
            logger.warning("Rate limit reached for mentions check")
            return
        
        try:
            # Get bot's user information
            me = self.client.get_me()
            my_username = me.data.username
            my_user_id = me.data.id
            
            # Search for mentions using search_recent_tweets with the bot's username
            query = f"@{my_username} -is:retweet -from:{my_username}"
            mentions = self.client.search_recent_tweets(
                query=query,
                max_results=10,
                tweet_fields=['conversation_id', 'created_at', 'public_metrics', 'referenced_tweets', 'author_id'],
                expansions=['author_id']
            )
            
            self.request_count += 1
            
            if not mentions.data:
                logger.info("No new mentions found")
                return
            
            logger.info(f"Found {len(mentions.data)} recent mentions")
            
            # Process each mention
            for mention in mentions.data:
                try:
                    # Skip if it's our own tweet
                    if mention.author_id == my_user_id:
                        continue
                    
                    # Skip if it's too old (older than 24 hours)
                    mention_time = mention.created_at.replace(tzinfo=None)
                    if datetime.now() - mention_time > timedelta(hours=24):
                        logger.info(f"Skipping old mention from {mention.created_at}")
                        continue
                    
                    # Skip if it's a reply to someone else (contains multiple @mentions)
                    if mention.text.count('@') > 1:
                        continue
                    
                    logger.info(f"Processing mention from user {mention.author_id}: {mention.text[:50]}...")
                    
                    # Create and post reply
                    if self.reply_to_tweet(mention.id, mention.text):
                        time.sleep(30)  # Small delay between replies to avoid spam
                    else:
                        logger.warning(f"Failed to reply to mention {mention.id}")
                        
                except Exception as e:
                    logger.error(f"Error processing mention {mention.id}: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Mentions check failed: {e}")
    
    def find_tweets_to_engage(self, count : int = 5) -> List[Any]:
        """ Find tweets to reply to using viral topics """
        if not self.can_make_request():
            return []
        
        try:
            topic_category = random.choice(list(self.viral_topics.keys()))
            topic = random.choice(self.viral_topics[topic_category])
            query = f"{topic} -is:retweet -is:reply lang:en"
            
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=10,
                tweet_fields=['public_metrics']
            )
            
            self.request_count += 1
            
            if not tweets.data:
                return []
            
            # Filter for good engagement potential
            good_tweets = [
                tweet for tweet in tweets.data
                if 5 <= tweet.public_metrics['like_count'] <= 100
                and tweet.public_metrics['reply_count'] <= 20
            ]
            
            return good_tweets[:count]
            
        except Exception as e:
            logger.error(f"Tweet search failed: {e}")
            return []
    
    def reply_to_tweet(self, tweet_id : str, tweet_text : str) -> bool:
        """ Reply to a specific tweet """
        reply_text = self.create_tweet("reply", tweet_text)
        
        if not reply_text or not self.can_make_request():
            return False
        
        try:
            self.client.create_tweet(
                text = reply_text,
                in_reply_to_tweet_id = tweet_id
            )
            self.request_count += 1
            logger.info(f"Replied to {tweet_id}: {reply_text}")
            return True
        except Exception as e:
            logger.error(f"Reply failed: {e}")
            return False
    
    def run_cycle(self):
        """ Run one complete bot cycle """
        logger.info("Starting bot cycle...")
        
        # Check and reply to mentions first
        logger.info("Checking mentions...")
        self.check_mentions()

        # Small delay before posting an original tweet
        time.sleep(60)

        # Post original tweet
        tweet = self.create_tweet("original")
        if tweet:
            self.post_tweet(tweet)
        
        # Small delay before community engagement
        time.sleep(60)
        
        # Engage with community
        tweets = self.find_tweets_to_engage(2)
        for tweet in tweets:
            if self.reply_to_tweet(tweet.id, tweet.text):
                time.sleep(30)  # Small delay between replies
        
        logger.info("Cycle completed")
    
    def run_automated(self):
        """ Run the bot in automated mode """
        logger.info("Starting automated mode...")
        
        try:
            while True:
                self.run_cycle()
                logger.info(f"Waiting {CHECK_INTERVAL} seconds until next cycle...")
                time.sleep(CHECK_INTERVAL)
                
        except KeyboardInterrupt:
            logger.info("Automated mode stopped")
            logger.info("Application closed")

def main():
    """ Main function with simple menu """
    program_info = "🤖 XBot | v0.1.0-alpha | Developed by Ricky Segura"
    logger.info(program_info)
    logger.info("=" * (len(program_info) + 1))
    
    try:
        bot = XBot()
        bot.run_automated()
    
    except Exception as e:
        logger.error(f"Application error: {e}")
        raise

if __name__ == "__main__":
    main()
