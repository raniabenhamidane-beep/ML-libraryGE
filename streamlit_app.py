import streamlit as st
import pandas as pd
import re
import html

st.set_page_config(
    page_title="Bibliothèque · Book Recommender",
    page_icon="📖",
    layout="wide"
)

# ─── GLOBAL STYLES ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@300;400;500;700&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #f5efe7;
    color: #2a211b;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header {
    visibility: hidden;
}

/* Same page margins everywhere */
.block-container {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    padding-left: 2.2rem !important;
    padding-right: 2.2rem !important;
    max-width: 100% !important;
}

/* Force columns to start from the top */
div[data-testid="column"] {
    align-self: flex-start !important;
}

            /* ── HERO HEADER ── */
.hero {
    background: #2f7163;
    border-bottom: 1px solid #dfd0c1;
    padding: 3rem 4rem 4.5rem;
    display: flex;
    align-items: flex-end;
    gap: 2rem;
    position: relative;
    overflow: hidden;
    border-radius: 18px 18px 0 0;
    margin: 1.3rem 0 0 0;
}

.hero::before {
    content: "BIBLIOTHÈQUE";
    position: absolute;
    top: -18px;
    right: -18px;
    font-family: 'Playfair Display', serif;
    font-size: 11rem;
    font-weight: 700;
    color: rgba(24, 82, 73, 0.65);
    letter-spacing: -4px;
    pointer-events: none;
    line-height: 1;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 4rem;
    font-weight: 700;
    color: #fff8ef;
    line-height: 1.05;
    margin: 0;
    letter-spacing: -1px;
    position: relative;
    z-index: 2;
}

.hero-title em {
    color: #f3b36e;
    font-style: italic;
    font-weight: 400;
}

.hero-subtitle {
    font-size: 0.85rem;
    color: #c7ddd7;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin: 0.5rem 0 4rem;
    position: relative;
    z-index: 2;
}

/* ── SEARCH AREA ── */
.search-shell {
    background: #eee7de;
    border-bottom: 1px solid #dfd0c1;
    padding: 1.75rem 0 2rem 0;
    margin: 0;
}

.search-title {
    color: #9b8b7d;
    font-size: 0.72rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    font-weight: 700;
    margin: 0 0 1rem 0;
}

/* Inputs */
.stTextInput > div > div > input {
    background: #ffffff !important;
    border: 1px solid #d9d1c8 !important;
    border-radius: 10px !important;
    color: #2a211b !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.85rem 1.1rem !important;
    caret-color: #2f7163;
}

.stTextInput > div > div > input::placeholder {
    color: #a9a4a0 !important;
}

.stTextInput > div > div > input:focus {
    border-color: #2f7163 !important;
    box-shadow: 0 0 0 2px rgba(47, 113, 99, 0.12) !important;
}

.stTextInput label {
    color: #9b8b7d !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.16em !important;
    text-transform: uppercase !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
}

/* ── SECTION HEADERS ── */
.section-header {
    padding: 3rem 0 1.25rem 0;
    border-bottom: 1px solid #dfd0c1;
    background: transparent;
    margin: 0 0 2rem 0;
}

.section-label {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    color: #2a211b;
    margin: 0 0 0.35rem 0;
    font-weight: 700;
}

.section-meta {
    font-size: 0.78rem;
    color: #aa9888;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin: 0;
    font-weight: 700;
}

/* ── BOOK CARD ── */
.book-card {
    background: #f3ede5;
    border: 1px solid #dfd0c1;
    border-radius: 14px;
    padding: 0;
    transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
    cursor: default;
    overflow: hidden;
    box-shadow: 0 8px 20px rgba(90, 65, 45, 0.08);
    margin-bottom: 0.7rem;
}

.book-card:hover {
    border-color: #c7ad98;
    transform: translateY(-4px);
    box-shadow: 0 14px 28px rgba(90, 65, 45, 0.14);
}

.book-cover-wrap {
    width: 100%;
    aspect-ratio: 2 / 3;
    overflow: hidden;
    background: #e7efe9;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}

.book-cover-wrap img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

/* ── PLACEHOLDER BOOK COVER ── */
.book-cover-placeholder {
    width: 100%;
    height: 100%;
    position: relative;
    background: linear-gradient(145deg, #6f8f83 0%, #456f63 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1rem;
}

/* Book spine */
.book-cover-placeholder::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 15%;
    height: 100%;
    background: linear-gradient(180deg, #2f7163 0%, #25594f 100%);
    border-right: 1px solid rgba(255, 248, 239, 0.22);
}

/* Inner cover frame */
.book-cover-placeholder::after {
    content: "";
    position: absolute;
    inset: 16px 16px 16px 22%;
    border: 1px solid rgba(255, 248, 239, 0.35);
    border-radius: 10px;
    pointer-events: none;
}

.cover-content {
    position: relative;
    z-index: 2;
    width: 70%;
    margin-left: 12%;
    text-align: center;
    padding: 1rem 0.8rem;
}

.book-cover-placeholder .cover-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.05rem;
    color: #f3b36e;
    text-align: center;
    line-height: 1.3;
    word-break: break-word;
    font-weight: 700;
}

.cover-subtle {
    margin-top: 0.85rem;
    font-size: 0.58rem;
    color: rgba(255, 248, 239, 0.72);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-weight: 500;
}

.rank-badge {
    position: absolute;
    top: 9px;
    left: 9px;
    background: #f3b36e;
    color: #2a211b;
    font-size: 0.72rem;
    font-weight: 700;
    padding: 4px 9px;
    border-radius: 7px;
    letter-spacing: 0.03em;
    font-family: 'DM Sans', sans-serif;
    z-index: 3;
}

.book-info {
    min-height: 88px;
    padding: 0.9rem 0.95rem;
    background: #fffdf9;
    border-top: 1px solid #dfd0c1;
}

.book-title {
    font-family: 'Playfair Display', serif;
    font-size: 0.95rem;
    color: #2a211b;
    line-height: 1.32;
    margin-bottom: 0.4rem;
    font-weight: 700;
    overflow: visible;
    display: block;
    white-space: normal;
    word-break: normal;
    overflow-wrap: anywhere;
}

.book-author {
    font-size: 0.74rem;
    color: #8b7b6d;
    letter-spacing: 0.03em;
    line-height: 1.35;
    overflow: visible;
    display: block;
    white-space: normal;
    word-break: normal;
    overflow-wrap: anywhere;
}

/* Overview button */
.stButton > button {
    width: 100%;
    background: #fffdf9 !important;
    color: #2f7163 !important;
    border: 1px solid #dfd0c1 !important;
    border-radius: 8px !important;
    padding: 0.55rem 0.75rem !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    font-family: 'DM Sans', sans-serif !important;
    margin-bottom: 1.4rem !important;
}

.stButton > button:hover {
    background: #eee7de !important;
    border-color: #c7ad98 !important;
    color: #25594f !important;
}

/* Dialog / popup */
div[data-testid="stDialog"] div[role="dialog"] {
    background: #fffdf9 !important;
    border: 1px solid #dfd0c1 !important;
    border-radius: 18px !important;
    box-shadow: 0 24px 60px rgba(42, 33, 27, 0.25) !important;
}

div[data-testid="stDialog"] h2 {
    font-family: 'Playfair Display', serif !important;
    color: #2a211b !important;
}

.dialog-author {
    color: #8b7b6d;
    font-size: 0.85rem;
    margin-top: -0.4rem;
    margin-bottom: 1.3rem;
    letter-spacing: 0.03em;
}

.dialog-description {
    color: #2a211b;
    font-size: 1rem;
    line-height: 1.75;
    max-height: 55vh;
    overflow-y: auto;
    padding-right: 0.5rem;
}

/* Info banner */
.info-banner {
    margin: 1.5rem 0;
    padding: 1rem 1.5rem;
    background: #eee7de;
    border-left: 4px solid #2f7163;
    border-radius: 8px;
    color: #6f6258;
    font-size: 0.85rem;
    letter-spacing: 0.02em;
}

/* Divider before footer */
.bottom-divider {
    border-top: 1px solid #dfd0c1;
    margin-top: 1.2rem;
}

/* Footer */
.footer-custom {
    padding: 2rem 0 1.5rem 0;
    background: #f5efe7;
}

.footer-custom p {
    font-size: 0.7rem;
    color: #aa9888;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin: 0;
}
</style>
""", unsafe_allow_html=True)

# ─── DATA ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    recommendations = pd.read_csv("data/item_prediction_hybrid.csv")
    items = pd.read_csv("data/items_enriched_api.csv")
    interactions = pd.read_csv("data/interactions_train.csv")
    return recommendations, items, interactions

recommendations, items, interactions = load_data()

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def clean_title(title):
    if pd.isna(title):
        return "Unknown Title"

    title = str(title).strip()

    if title.endswith("/"):
        title = title[:-1].strip()

    return title


def clean_author(author):
    if pd.isna(author):
        return None

    author = str(author).strip()

    author = author.replace("[", "").replace("]", "")
    author = author.replace("'", "").replace('"', "")
    author = " ".join(author.split())

    # Remove isolated hyphens often found between first and last names
    author = re.sub(r"\s*-\s*", " ", author)

    # Clean spaces again after removing hyphens
    author = " ".join(author.split())

    # Remove dates like 1916- or 1916-2010
    author = re.sub(r",?\s*\b\d{4}-?\d{0,4}\b", "", author)

    # Clean spaces again after removing dates
    author = " ".join(author.split())

    if ";" in author:
        authors = [a.strip() for a in author.split(";") if a.strip()]
        cleaned = []

        for a in authors:
            parts = [p.strip() for p in a.split(",") if p.strip()]

            if len(parts) == 2:
                last, first = parts
                cleaned.append(f"{first} {last}")
            else:
                cleaned.append(a)

        return ", ".join(cleaned)

    parts = [p.strip() for p in author.split(",") if p.strip()]

    if len(parts) > 2 and len(parts) % 2 == 0:
        cleaned = []

        for i in range(0, len(parts), 2):
            last = parts[i]
            first = parts[i + 1]
            cleaned.append(f"{first} {last}")

        return ", ".join(cleaned)

    if len(parts) == 2:
        first_part, second_part = parts

        if len(first_part.split()) >= 2 and len(second_part.split()) >= 2:
            return f"{first_part}, {second_part}"

        return f"{second_part} {first_part}"

    return author


def safe_text(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    if value == "" or value.lower() == "nan":
        return None

    return value


def safe_thumbnail(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    if value == "" or value.lower() == "nan":
        return None

    return value.replace("http://", "https://")


def render_section_header(title, meta):
    st.markdown(f"""
    <div class="section-header">
        <h2 class="section-label">{html.escape(title)}</h2>
        <p class="section-meta">{html.escape(meta)}</p>
    </div>
    """, unsafe_allow_html=True)


@st.dialog("Book overview")
def show_book_overview(title, author, description):
    st.markdown(f"""
    <h2 style="font-family:'Playfair Display', serif; margin-bottom:0.4rem;">
        {html.escape(title)}
    </h2>
    """, unsafe_allow_html=True)

    if author:
        st.markdown(f"""
        <p class="dialog-author">
            {html.escape(author)}
        </p>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="dialog-description">
        {html.escape(description)}
    </div>
    """, unsafe_allow_html=True)


def render_book_card(book, rank=None):
    raw_title = book.get("Title") if pd.notna(book.get("Title")) else book.get("api_title")
    title = clean_title(raw_title)

    raw_author = book.get("Author") if pd.notna(book.get("Author")) else book.get("api_authors")
    author = clean_author(raw_author)

    thumbnail = safe_thumbnail(book.get("api_thumbnail"))

    description = (
        book.get("api_description")
        if pd.notna(book.get("api_description"))
        else book.get("description_x")
    )
    description = safe_text(description)

    rank_html = f'<div class="rank-badge">#{rank}</div>' if rank else ""
    safe_title = html.escape(title)

    if thumbnail:
        cover_html = (
            f'<div class="book-cover-wrap">'
            f'{rank_html}'
            f'<img src="{html.escape(thumbnail)}" alt="{safe_title}" loading="lazy">'
            f'</div>'
        )
    else:
        cover_title = title
        cover_html = (
            f'<div class="book-cover-wrap">'
            f'{rank_html}'
            f'<div class="book-cover-placeholder">'
            f'<div class="cover-content">'
            f'<div class="cover-title">{html.escape(cover_title)}</div>'
            f'<div class="cover-subtle">Cover unavailable</div>'
            f'</div>'
            f'</div>'
            f'</div>'
        )

    if author:
        author_html = f'<div class="book-author">{html.escape(author)}</div>'
    else:
        author_html = '<div class="book-author">Unknown author</div>'

    card_html = (
        f'<div class="book-card">'
        f'{cover_html}'
        f'<div class="book-info">'
        f'<div class="book-title">{html.escape(title)}</div>'
        f'{author_html}'
        f'</div>'
        f'</div>'
    )

    return card_html, description, title, author


def render_book_grid(books_df, show_description=False, ranked=True, cols_per_row=5):
    cols = st.columns(cols_per_row, gap="medium")

    for idx, (_, book) in enumerate(books_df.iterrows()):
        with cols[idx % cols_per_row]:
            rank = idx + 1 if ranked else None
            card_html, description, title, author = render_book_card(book, rank=rank)
            st.markdown(card_html, unsafe_allow_html=True)

            if show_description and description:
                button_key = f"overview_{rank}_{idx}_{str(title)[:30]}"
                if st.button("Overview", key=button_key):
                    show_book_overview(title, author, description)

        if (idx + 1) % cols_per_row == 0 and idx + 1 < len(books_df):
            cols = st.columns(cols_per_row, gap="medium")


# ─── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-content">
        <p class="hero-subtitle">University Library · Personalized Discovery</p>
        <h1 class="hero-title">Your next<br><em>great read</em><br>awaits.</h1>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── SEARCH AREA ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="search-shell">
    <p class="search-title">Find your recommendations</p>
</div>
""", unsafe_allow_html=True)

col_name, col_id, _ = st.columns([2, 2, 5])

with col_name:
    name_input = st.text_input("Your name", placeholder="e.g. Sophie")

with col_id:
    user_input = st.text_input("User ID", placeholder="e.g. 1042")

# ─── MAIN CONTENT ─────────────────────────────────────────────────────────────
if not user_input:
    st.markdown("""
    <div class="info-banner">
        Enter your user ID above to receive personalised book recommendations based on your reading history.
    </div>
    """, unsafe_allow_html=True)

else:
    try:
        selected_user = int(user_input)
        display_name = name_input.strip() if name_input.strip() else "reader"

        user_row = recommendations[recommendations["user_id"] == selected_user]

        if user_row.empty:
            st.markdown(f"""
            <div class="info-banner">
                No recommendations found for user <strong>{selected_user}</strong>. Please check the ID.
            </div>
            """, unsafe_allow_html=True)

        else:
            rec_string = user_row.iloc[0]["recommendation"]
            recommended_item_ids = [int(x) for x in str(rec_string).split()]

            recommended_books = items[items["i"].isin(recommended_item_ids)].copy()

            recommended_books["rank"] = recommended_books["i"].apply(
                lambda x: recommended_item_ids.index(x) + 1
            )

            recommended_books = recommended_books.sort_values("rank").head(10)

            render_section_header(
                f"Welcome {display_name}! Discover the books recommended just for you.",
                "Personalised recommendations · based on your reading history"
            )

            render_book_grid(
                recommended_books,
                show_description=True,
                ranked=True,
                cols_per_row=5
            )

            user_interactions = interactions[interactions["u"] == selected_user]

            if not user_interactions.empty:
                read_item_ids = user_interactions["i"].drop_duplicates().tolist()
                read_books = items[items["i"].isin(read_item_ids)].copy()

                if not read_books.empty:
                    render_section_header(
                        "Your reading history",
                        f"{len(read_books)} books · all-time rentals"
                    )

                    render_book_grid(
                        read_books,
                        show_description=False,
                        ranked=True,
                        cols_per_row=5
                    )

    except ValueError:
        st.markdown("""
        <div class="info-banner">
            Please enter a valid numeric user ID.
        </div>
        """, unsafe_allow_html=True)

# ─── MOST POPULAR ─────────────────────────────────────────────────────────────
top_items = (
    interactions["i"]
    .value_counts()
    .head(10)
    .index
    .tolist()
)

top_books = items[items["i"].isin(top_items)].copy()

top_books["rank"] = top_books["i"].apply(
    lambda x: top_items.index(x) + 1
)

top_books = top_books.sort_values("rank")

render_section_header(
    "Most borrowed",
    "The 10 most popular titles across the entire library"
)

render_book_grid(
    top_books,
    show_description=False,
    ranked=True,
    cols_per_row=5
)

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown('<div class="bottom-divider"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer-custom">
    <p>
        University Library · Recommendation Engine · Built with collaborative filtering &amp; hybrid models
    </p>
</div>
""", unsafe_allow_html=True)