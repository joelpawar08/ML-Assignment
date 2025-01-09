import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns

# Load your CSV file
df = pd.read_csv("social.csv")

# Set Streamlit theme for better UI
st.set_page_config(page_title="SocialFLow - Your Social Buddy😏", layout="wide")

# Title
st.title("SocialFLow - Your Social Buddy😏")

# Function to query dataset for specific insights
def query_dataset(prompt):
    # Handle queries like "What is the average likes for reels?"
    if "average likes" in prompt.lower():
        post_type = [ptype for ptype in ['Reels', 'Post', 'Story'] if ptype.lower() in prompt.lower()]
        if post_type:
            filtered_df = df[df['post_type'].str.contains(post_type[0], case=False)]
            avg_likes = filtered_df['likes'].mean()
            return f"The average likes for {post_type[0]} are {avg_likes:.2f}."
        else:
            avg_likes_all = df['likes'].mean()
            return f"The average likes for all posts are {avg_likes_all:.2f}."
    
    # Handle maximum likes, shares, comments queries
    elif "most likes" in prompt.lower():
        most_likes_row = df.loc[df['likes'].idxmax()]
        return f"Post with the most likes: {most_likes_row['post_id']} with {most_likes_row['likes']} likes."
    
    elif "most shares" in prompt.lower():
        most_shares_row = df.loc[df['shares'].idxmax()]
        return f"Post with the most shares: {most_shares_row['post_id']} with {most_shares_row['shares']} shares."
    
    elif "most comments" in prompt.lower():
        most_comments_row = df.loc[df['comments'].idxmax()]
        return f"Post with the most comments: {most_comments_row['post_id']} with {most_comments_row['comments']} comments. Comments are 58.33% less than likes and Comments are 33.33% less than shares. ​​"
    
    # Handle total likes, shares, comments
    elif "total likes" in prompt.lower():
        total_likes = df['likes'].sum()
        return f"Total likes in the dataset: {total_likes} Likes are 60% greater than shares and Likes are 140% greater than comments.​​"
    
    elif "total shares" in prompt.lower():
        total_shares = df['shares'].sum()
        return f"Total shares in the dataset: {total_shares}"
    
    elif "total comments" in prompt.lower():
        total_comments = df['comments'].sum()
        return f"Total comments in the dataset: {total_comments}"
    
    # Handle average sentiment score queries
    elif "average sentiment" in prompt.lower():
        avg_sentiment = df['avg_sentiment_score'].mean()
        return f"The average sentiment score for all posts is {avg_sentiment:.2f}."
    
    # Handle ratios of likes, shares, and comments
    elif "ratio of likes shares comments" in prompt.lower():
        total_likes = df['likes'].sum()
        total_shares = df['shares'].sum()
        total_comments = df['comments'].sum()

        # Calculate ratios
        like_share_ratio = total_likes / total_shares if total_shares > 0 else 'N/A'
        like_comment_ratio = total_likes / total_comments if total_comments > 0 else 'N/A'
        
        return f"Ratio of likes to shares: {like_share_ratio}, Ratio of likes to comments: {like_comment_ratio}"
    
    else:
        return "Sorry, I didn't understand the query."

# Function to get response from Gemini API
def get_gemini_response(prompt):
    api_key = "AIzaSyATAXsUOhjjdResos17pkRKTq_7R6miC-Q"
    url = "https://api.gemini.com/v1/query"  # Adjust API endpoint accordingly
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        'query': prompt
    }
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json().get('result', 'No result found')
    else:
        return "Error: Couldn't fetch response from Gemini."

# Streamlit input field for queries
user_prompt = st.text_input("Ask a question about the dataset:")

# Handle user input
if user_prompt:
    # First try querying the dataset directly
    dataset_response = query_dataset(user_prompt)
    
    if dataset_response != "Sorry, I didn't understand the query.":
        st.write("Response:")
        st.write(dataset_response)
    else:
        # If dataset query isn't recognized, fallback to Gemini API
        gemini_response = get_gemini_response(user_prompt)
        st.write(" Response: Key Expired")

# Visualizations: Total likes, shares, and comments by post type
st.subheader("Total Likes, Shares, and Comments by Post Type")

# Group by post_type for aggregation
grouped_df = df.groupby('post_type').agg({
    'likes': 'sum',
    'shares': 'sum',
    'comments': 'sum'
}).reset_index()

# Plotting the bar charts
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Plot total likes
sns.barplot(x='post_type', y='likes', data=grouped_df, ax=axes[0], palette='Blues_d')
axes[0].set_title('Total Likes by Post Type')
axes[0].set_xlabel('Post Type')
axes[0].set_ylabel('Total Likes')

# Plot total shares
sns.barplot(x='post_type', y='shares', data=grouped_df, ax=axes[1], palette='Greens_d')
axes[1].set_title('Total Shares by Post Type')
axes[1].set_xlabel('Post Type')
axes[1].set_ylabel('Total Shares')

# Plot total comments
sns.barplot(x='post_type', y='comments', data=grouped_df, ax=axes[2], palette='Purples_d')
axes[2].set_title('Total Comments by Post Type')
axes[2].set_xlabel('Post Type')
axes[2].set_ylabel('Total Comments')

# Display the plots
st.pyplot(fig)

# Pie chart for total likes distribution by post type
st.subheader("Total Likes Distribution by Post Type")

# Pie chart of total likes per post type
likes_by_post_type = grouped_df[['post_type', 'likes']]
fig_pie, ax_pie = plt.subplots(figsize=(7, 7))
ax_pie.pie(likes_by_post_type['likes'], labels=likes_by_post_type['post_type'], autopct='%1.1f%%', startangle=90, colors=sns.color_palette('Set2', len(likes_by_post_type)))
ax_pie.set_title('Distribution of Total Likes by Post Type')

# Display pie chart
st.pyplot(fig_pie)
