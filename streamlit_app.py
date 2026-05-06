import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Library Recommender",
    page_icon="📚",
    layout="wide"
)

st.title("Library Recommendation System")
st.write("Welcome to our personalized book recommender.")

@st.cache_data
def load_data():
    recommendations = pd.read_csv("data/item_prediction_hybrid.csv")
    items = pd.read_csv("data/items_enriched_api.csv")
    return recommendations, items

recommendations, items = load_data()


# Start user entry
st.subheader("Get book recommendations")

user_input = st.text_input("Enter your user ID")

if user_input == "":
    st.info("Please enter a user ID to see recommendations.")

else:
    try:
        selected_user = int(user_input)

        user_row = recommendations[recommendations["user_id"] == selected_user]

        if user_row.empty:
            st.warning("No recommendation found for this user.")

        else:
            rec_string = user_row.iloc[0]["recommendation"]
            recommended_item_ids = [int(x) for x in str(rec_string).split()]

            recommended_books = items[items["i"].isin(recommended_item_ids)].copy()

            recommended_books["rank"] = recommended_books["i"].apply(
                lambda x: recommended_item_ids.index(x) + 1
            )

            recommended_books = recommended_books.sort_values("rank")

            st.subheader(f"Top 10 recommended books for user {selected_user}")

            for _, book in recommended_books.iterrows():
                title = book.get("api_title") if pd.notna(book.get("api_title")) else book.get("Title")
                author = book.get("api_authors") if pd.notna(book.get("api_authors")) else book.get("Author")
                description = book.get("api_description") if pd.notna(book.get("api_description")) else book.get("description_x")
                thumbnail = book.get("api_thumbnail") 
                #categories = book.get("api_categories")
                categories = None
                if pd.notna(book.get("api_categories")):
                    categories = book.get("api_categories")
                elif pd.notna(book.get("Subjects")):
                    categories = book.get("Subjects")
                elif pd.notna(book.get("categories")):
                    categories = book.get("categories")

                published_date = book.get("api_published_date")

                col1, col2 = st.columns([1, 4])

                with col1:
                    if pd.notna(thumbnail):
                        st.image(thumbnail, width=120)
                    else:
                        st.write("No image")

                with col2:
                    st.markdown(f"### #{book['rank']} — {title}")

                    if pd.notna(author):
                        st.write(f"Author: {author}")

                    if pd.notna(published_date):
                        st.write(f"Published: {published_date}")
                    if pd.notna(categories):
                        st.write(f"Categories: {categories}")
                    if pd.notna(description):
                        st.write(description[:500] + "..." if len(description) > 500 else description)

                st.divider()

    except ValueError:
        st.error("Please enter a valid numeric user ID.")