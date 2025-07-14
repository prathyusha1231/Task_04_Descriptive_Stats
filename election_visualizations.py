import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

def setup_plot_style():
    """
    Configure professional plot styling for executive presentations
    """
    plt.style.use('default')
    sns.set_palette("husl")
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 11
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 12

def plot_engagement_inequality(fb_posts_df, twitter_df):
    """
    Visualize the extreme inequality in social media engagement
    
    Args:
        fb_posts_df (DataFrame): Facebook posts data
        twitter_df (DataFrame): Twitter posts data
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Facebook engagement distribution (log scale)
    fb_likes = fb_posts_df['Likes'].replace(0, 1)  
    ax1.hist(np.log10(fb_likes), bins=50, alpha=0.7, color='#1f77b4', edgecolor='black')
    ax1.set_xlabel('Log10(Likes)')
    ax1.set_ylabel('Number of Posts')
    ax1.set_title('Facebook Posts: Engagement Inequality\n(Most posts get <1000 likes, few go viral)')
    ax1.grid(True, alpha=0.3)
    
    # Twitter engagement distribution (log scale)  
    twitter_likes = twitter_df['likeCount'].replace(0, 1)
    ax2.hist(np.log10(twitter_likes), bins=50, alpha=0.7, color='#ff7f0e', edgecolor='black')
    ax2.set_xlabel('Log10(Likes)')
    ax2.set_ylabel('Number of Posts')
    ax2.set_title('Twitter Posts: Engagement Inequality\n(Winner-take-all viral content)')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('engagement_inequality.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_advertising_scale(ads_df):
    """
    Show the massive scale of political advertising
    
    Args:
        ads_df (DataFrame): Facebook ads data
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Top advertisers by volume
    top_advertisers = ads_df['bylines'].value_counts().head(10)
    ax1.barh(range(len(top_advertisers)), top_advertisers.values, color='steelblue')
    ax1.set_yticks(range(len(top_advertisers)))
    ax1.set_yticklabels([name[:30] + '...' if len(name) > 30 else name for name in top_advertisers.index])
    ax1.set_xlabel('Number of Ads')
    ax1.set_title('Political Advertising Dominance: Top 10 Advertisers by Volume')
    ax1.grid(True, alpha=0.3, axis='x')
    
    # Spending distribution
    spending = ads_df['estimated_spend']
    ax2.hist(spending, bins=50, alpha=0.7, color='green', edgecolor='black')
    ax2.set_xlabel('Estimated Spend ($)')
    ax2.set_ylabel('Number of Ads')
    ax2.set_title(f'Ad Spending Distribution\nTotal: ${spending.sum():,.0f} | Average: ${spending.mean():,.0f}')
    ax2.axvline(spending.mean(), color='red', linestyle='--', label=f'Average: ${spending.mean():,.0f}')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('advertising_scale.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_political_topics(ads_df, posts_df, twitter_df):
    """
    Compare political topic focus across platforms
    
    Args:
        ads_df (DataFrame): Facebook ads data
        posts_df (DataFrame): Facebook posts data  
        twitter_df (DataFrame): Twitter data
    """
    # Define topic columns
    topic_cols = [col for col in ads_df.columns if 'topic_illuminating' in col and col != 'freefair_illuminating']
    
    # Calculate topic percentages for each platform
    topic_data = []
    for col in topic_cols:
        topic_name = col.replace('_topic_illuminating', '').replace('_', ' ').title()
        
        ads_pct = ads_df[col].mean() * 100 if col in ads_df.columns else 0
        posts_pct = posts_df[col].mean() * 100 if col in posts_df.columns else 0
        twitter_pct = twitter_df[col].mean() * 100 if col in twitter_df.columns else 0
        
        topic_data.append({
            'Topic': topic_name,
            'Facebook Ads': ads_pct,
            'Facebook Posts': posts_pct,
            'Twitter': twitter_pct
        })
    
    topic_df = pd.DataFrame(topic_data)
    topic_df = topic_df.set_index('Topic')
    
    # Create grouped bar chart
    ax = topic_df.plot(kind='bar', figsize=(16, 8), width=0.8)
    ax.set_title('Political Topic Focus Across Platforms\n(Percentage of content addressing each topic)')
    ax.set_xlabel('Political Topics')
    ax.set_ylabel('Percentage of Content (%)')
    ax.legend(title='Platform')
    ax.grid(True, alpha=0.3, axis='y')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('political_topics.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_platform_comparison(posts_df, ads_df, twitter_df):
    """
    Compare engagement patterns across platforms
    
    Args:
        posts_df (DataFrame): Facebook posts data
        ads_df (DataFrame): Facebook ads data
        twitter_df (DataFrame): Twitter data
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Platform scales
    platforms = ['FB Posts\n(19K)', 'FB Ads\n(247K)', 'Twitter\n(27K)']
    counts = [len(posts_df), len(ads_df), len(twitter_df)]
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    
    ax1.bar(platforms, counts, color=colors, alpha=0.7)
    ax1.set_title('Content Volume by Platform')
    ax1.set_ylabel('Number of Posts/Ads')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Average engagement
    fb_avg_engagement = posts_df['Total Interactions'].mean()
    twitter_avg_engagement = twitter_df['likeCount'].mean()
    
    engagement_platforms = ['Facebook Posts', 'Twitter Posts']
    engagement_avgs = [fb_avg_engagement, twitter_avg_engagement]
    
    ax2.bar(engagement_platforms, engagement_avgs, color=['#1f77b4', '#2ca02c'], alpha=0.7)
    ax2.set_title('Average Engagement by Platform')
    ax2.set_ylabel('Average Interactions/Likes')
    ax2.grid(True, alpha=0.3, axis='y')
    

def create_executive_dashboard():
    """
    Create a comprehensive dashboard for executive presentation
    """
    print("Creating Election Social Media Analytics Dashboard...")
    
    # Load data
    try:
        print("Loading datasets...")
        posts_df = pd.read_csv("period_03/2024_fb_posts_president_scored_anon.csv")
        ads_df = pd.read_csv("period_03/2024_fb_ads_president_scored_anon.csv")
        twitter_df = pd.read_csv("period_03/2024_tw_posts_president_scored_anon.csv")
        
        print(f"Loaded: {len(posts_df):,} FB posts, {len(ads_df):,} ads, {len(twitter_df):,} tweets")
        
        
        setup_plot_style()
        
        # Generate visualizations
        print("Generating engagement inequality analysis...")
        plot_engagement_inequality(posts_df, twitter_df)
        
        print("Analyzing advertising scale...")
        plot_advertising_scale(ads_df)
        
        print("Mapping political topics...")
        plot_political_topics(ads_df, posts_df, twitter_df)
        
        print("Creating platform comparison...")
        plot_platform_comparison(posts_df, ads_df, twitter_df)
        
        print("Dashboard complete! Check generated PNG files.")
        print("\nFiles created:")
        print("   - engagement_inequality.png")
        print("   - advertising_scale.png") 
        print("   - political_topics.png")
        print("   - platform_comparison.png")
        
    except FileNotFoundError as e:
        print(f"Dataset file not found: {e}")
        print("Ensure CSV files are in the period_03/ directory")
    except Exception as e:
        print(f"Error creating visualizations: {e}")

if __name__ == "__main__":
    create_executive_dashboard()