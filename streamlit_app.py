import streamlit as st
import pandas as pd
import re
import html
import ast
import random
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import TfidfVectorizer


# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────


st.set_page_config(
   page_title="Bibliothèque · Book Recommender",
   page_icon="📖",
   layout="wide"
)




# ─── GLOBAL STYLES ────────────────────────────────────────────────────────────


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Outfit:wght@300;400;500;600;700&display=swap');


:root {
   --bg-main: #F7F2EC;
   --bg-soft: #FFF9F3;
   --bg-panel: #F1E8DF;
   --border-soft: #E3D8CE;


   --text-main: #6D5A4B;
   --text-soft: #8D7C71;
   --text-faint: #AB9A8F;


   --olive: #818546;
   --pink: #F5B1B8;
   --terracotta: #E68A58;
   --peach: #FFE4D2;
   --blue-soft: #9BC0CC;
   --blue-mid: #7BA9B8;
   --mustard: #C3A05B;
   --sage: #99B7A4;


   --white-cream: #FFF8F2;
}


html, body, [class*="css"] {
   font-family: 'Outfit', sans-serif;
}


.stApp {
   background: var(--bg-main);
   color: var(--text-main);
}


#MainMenu, footer, header { visibility: hidden; }


.block-container {
   max-width: 1500px !important;
   margin: 0 auto !important;
   padding-top: 0 !important;
   padding-bottom: 2rem !important;
   padding-left: 2rem !important;
   padding-right: 2rem !important;
}


div[data-testid="column"] {
   align-self: flex-start !important;
}


/* ══════════════════════════════════════════
  HERO
══════════════════════════════════════════ */


.hero-outer {
   position: relative;
   background: var(--bg-soft);
   border-radius: 24px;
   margin: 1.4rem 0 0 0;
   overflow: hidden;
   border: 1px solid var(--border-soft);
   display: flex;
   flex-direction: column;
}


.hero-outer::before {
   content: "";
   position: absolute;
   inset: 0;
   background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
   pointer-events: none;
   z-index: 0;
   opacity: 0.45;
}


.hero-shelf-row {
   display: flex;
   align-items: stretch;
   position: relative;
   z-index: 1;
   min-height: 460px;
}


.hero-shelf-left,
.hero-shelf-right {
   width: 250px;
   flex-shrink: 0;
   padding: 2.5rem 0 0 0;
   display: flex;
   flex-direction: column;
   gap: 0;
   box-sizing: border-box;
}


.hero-shelf-left {
   align-items: flex-start;
}


.hero-shelf-right {
   align-items: flex-end;
}


.hero-shelf-unit {
   width: var(--shelf-width);
   display: flex;
   flex-direction: column;
   align-items: flex-start;
   margin-bottom: 20px;
}


.hero-shelf-right .hero-shelf-unit {
   align-items: flex-end;
}


.shelf-row-books {
   width: var(--shelf-width);
   display: flex;
   align-items: flex-end;
   gap: 3px;
   margin-bottom: 0;
   box-sizing: border-box;
   overflow: visible;
}


.shelf-row-books.right-side {
   justify-content: flex-end;
}


.shelf-plank {
   width: var(--shelf-width);
   height: 14px;
   background: linear-gradient(180deg, #D9B579 0%, #C79A60 50%, #A97847 100%);
   box-shadow: 0 8px 18px rgba(140, 110, 80, 0.18), inset 0 2px 0 rgba(255,255,255,0.30);
   border-radius: 3px;
   margin: 0;
   box-sizing: border-box;
}


.spine {
   display: inline-block;
   border-radius: 3px 4px 4px 3px;
   position: relative;
   flex-shrink: 0;
   box-shadow: 3px 4px 8px rgba(120, 100, 85, 0.20), inset -3px 0 6px rgba(0,0,0,0.10);
   transition: transform 0.25s ease;
}


.spine::after {
   content: "";
   position: absolute;
   left: 0; top: 0; bottom: 0;
   width: 5px;
   background: rgba(0,0,0,0.12);
   border-radius: 3px 0 0 3px;
}


.spine:hover { transform: translateY(-8px); }


.hero-center {
   flex: 1;
   display: flex;
   flex-direction: column;
   align-items: center;
   justify-content: center;
   padding: 3rem 2rem 2.5rem;
   text-align: center;
}


.hero-eyebrow {
   display: inline-flex;
   align-items: center;
   gap: 0.5rem;
   font-size: 0.68rem;
   letter-spacing: 0.2em;
   text-transform: uppercase;
   color: var(--olive);
   font-weight: 600;
   margin-bottom: 1.5rem;
   background: rgba(129, 133, 70, 0.10);
   border: 1px solid rgba(129, 133, 70, 0.20);
   padding: 0.4rem 1rem;
   border-radius: 999px;
}


.hero-eyebrow span { opacity: 0.6; }


.hero-title {
   font-family: 'Cormorant Garamond', serif;
   font-size: 5rem;
   font-weight: 700;
   color: var(--text-main);
   line-height: 0.95;
   letter-spacing: -2px;
   margin: 0 0 0.6rem 0;
}


.hero-title em {
   color: var(--terracotta);
   font-style: italic;
   font-weight: 600;
}


.hero-subtitle {
   font-size: 0.97rem;
   color: var(--text-soft);
   line-height: 1.8;
   max-width: 440px;
   margin: 1.2rem auto 0;
   font-weight: 300;
}


.hero-stats {
   display: flex;
   align-items: center;
   gap: 0;
   margin-top: 2.2rem;
   background: linear-gradient(135deg, var(--sage) 0%, var(--olive) 100%);
   border-radius: 14px;
   overflow: hidden;
   border: 1px solid rgba(255,255,255,0.20);
}


.stat-item {
   padding: 1rem 2rem;
   text-align: center;
   flex: 1;
   position: relative;
}


.stat-item + .stat-item::before {
   content: "";
   position: absolute;
   left: 0; top: 20%;
   height: 60%; width: 1px;
   background: rgba(255,255,255,0.22);
}


.stat-number {
   font-family: 'Cormorant Garamond', serif;
   font-size: 2rem;
   font-weight: 700;
   color: var(--white-cream);
   line-height: 1;
   display: block;
}


.stat-label {
   font-size: 0.62rem;
   text-transform: uppercase;
   letter-spacing: 0.16em;
   color: rgba(255,248,242,0.85);
   font-weight: 600;
   margin-top: 0.3rem;
   display: block;
}


.hero-ribbon {
   background: var(--terracotta);
   padding: 0.75rem 2rem;
   text-align: center;
   position: relative;
   z-index: 2;
}


.hero-ribbon p {
   margin: 0;
   font-size: 0.72rem;
   letter-spacing: 0.18em;
   text-transform: uppercase;
   color: rgba(255,255,255,0.84);
   font-weight: 600;
}


.hero-ribbon strong { color: #fff; }


/* ══════════════════════════════════════════
  LANDING CHOICE
══════════════════════════════════════════ */


.path-wrapper-fixed {
   max-width: 980px !important;
   width: 100% !important;
   margin: 2rem auto 1.6rem auto !important;
   padding: 2rem 2.2rem 1.9rem 2.2rem !important;
   background: var(--bg-panel) !important;
   border: 1px solid var(--border-soft) !important;
   border-radius: 24px !important;
   box-shadow: 0 14px 30px rgba(120, 95, 80, 0.07) !important;
   text-align: center !important;
   box-sizing: border-box !important;
}


.path-kicker-fixed {
   color: var(--terracotta) !important;
   font-size: 0.66rem !important;
   letter-spacing: 0.22em !important;
   text-transform: uppercase !important;
   font-weight: 700 !important;
   margin: 0 auto 0.8rem auto !important;
   text-align: center !important;
}


.path-title-fixed {
   font-family: 'Cormorant Garamond', serif !important;
   color: var(--text-main) !important;
   font-size: 2.35rem !important;
   font-weight: 700 !important;
   text-align: center !important;
   margin: 0 auto !important;
   line-height: 1.12 !important;
   max-width: 760px !important;
   letter-spacing: -0.4px !important;
}


.path-subtitle-fixed {
   color: var(--text-soft) !important;
   text-align: center !important;
   max-width: 620px !important;
   margin: 1rem auto 0 auto !important;
   line-height: 1.65 !important;
   font-weight: 300 !important;
   font-size: 0.95rem !important;
}


.path-options-fixed {
   max-width: 980px !important;
   width: 100% !important;
   margin: 0 auto !important;
}


.choice-card {
   background: #FFFDF9;
   border: 1.5px solid #DDCEC2;
   border-radius: 24px;
   padding: 2rem 1.7rem;
   min-height: 210px;
   text-align: center;
   box-shadow: 0 12px 24px rgba(120, 95, 80, 0.07);
   transition: all 0.2s ease;
}


.choice-card:hover {
   transform: translateY(-5px);
   box-shadow: 0 18px 34px rgba(120, 95, 80, 0.11);
   border-color: #E0B79F;
}


.choice-icon {
   font-size: 2.2rem;
   margin-bottom: 0.7rem;
}


.choice-card-title {
   font-family: 'Cormorant Garamond', serif;
   font-size: 1.8rem;
   font-weight: 700;
   color: var(--text-main);
   margin-bottom: 0.45rem;
}


.choice-card-text {
   color: var(--text-soft);
   font-size: 0.86rem;
   line-height: 1.65;
   font-weight: 300;
   max-width: 420px;
   margin: 0 auto;
}


/* ══════════════════════════════════════════
  TOP ACTION BAR
══════════════════════════════════════════ */


.top-action-bar {
   margin-top: 1.5rem;
   padding: 1.2rem 1.5rem;
   background: var(--bg-panel);
   border: 1px solid var(--border-soft);
   border-radius: 18px;
}


.mode-label {
   font-size: 0.67rem;
   letter-spacing: 0.18em;
   text-transform: uppercase;
   color: var(--text-faint);
   font-weight: 700;
   margin-bottom: 0.3rem;
}


.mode-title {
   font-family: 'Cormorant Garamond', serif;
   font-size: 2rem;
   color: var(--text-main);
   font-weight: 700;
   line-height: 1;
   margin: 0;
}


.mode-description {
   color: var(--text-soft);
   font-size: 0.86rem;
   line-height: 1.6;
   margin-top: 0.5rem;
   font-weight: 300;
}


/* ══════════════════════════════════════════
  INPUTS
══════════════════════════════════════════ */


.search-shell {
   background: var(--bg-panel);
   border: 1px solid var(--border-soft);
   padding: 1.2rem 2rem 0.9rem 2rem;
   margin: 1.4rem 0 0.4rem 0;
   border-radius: 20px;
   position: relative;
}


.search-title {
   color: var(--text-soft);
   font-size: 0.68rem;
   letter-spacing: 0.18em;
   text-transform: uppercase;
   font-weight: 700;
   margin: 0;
}


.stTextInput {
   margin-top: -0.1rem !important;
}


.stTextInput label {
   color: var(--text-soft) !important;
   font-size: 0.68rem !important;
   letter-spacing: 0.16em !important;
   text-transform: uppercase !important;
   font-family: 'Outfit', sans-serif !important;
   font-weight: 700 !important;
   padding-bottom: 0.35rem !important;
}


.stTextInput div[data-baseweb="input"] {
   background: #FFFDF9 !important;
   border: 1.5px solid #D8CCC0 !important;
   border-radius: 13px !important;
   box-shadow: none !important;
   outline: none !important;
   transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}


.stTextInput div[data-baseweb="input"]:hover {
   border-color: #D0BFB2 !important;
}


.stTextInput div[data-baseweb="input"]:focus-within {
   border-color: var(--terracotta) !important;
   box-shadow: 0 0 0 3px rgba(230, 138, 88, 0.14) !important;
   outline: none !important;
}


.stTextInput input {
   background: transparent !important;
   border: none !important;
   outline: none !important;
   box-shadow: none !important;
   color: var(--text-main) !important;
   font-family: 'Outfit', sans-serif !important;
   font-size: 0.97rem !important;
   padding: 0.88rem 1.2rem !important;
   caret-color: var(--terracotta) !important;
}


.stTextInput input::placeholder {
   color: #B0A39A !important;
}


input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus {
   -webkit-box-shadow: 0 0 0px 1000px #FFFDF9 inset !important;
   -webkit-text-fill-color: var(--text-main) !important;
   caret-color: var(--terracotta) !important;
}


/* ══════════════════════════════════════════
  SEARCH RESULTS
══════════════════════════════════════════ */


.search-result-item {
   padding: 0.7rem 1rem;
   border-radius: 10px;
   background: #FFFDF9;
   border: 1px solid #EDE4DA;
   margin-bottom: 0.4rem;
   transition: all 0.15s ease;
}


.search-result-item:hover {
   background: #FFF0E7;
   border-color: #E0B79F;
}


.search-result-title {
   font-family: 'Cormorant Garamond', serif;
   font-size: 1rem;
   font-weight: 700;
   color: var(--text-main);
   line-height: 1.2;
}


.search-result-author {
   font-size: 0.75rem;
   color: var(--text-soft);
   margin-top: 0.2rem;
}


.selected-card {
   background: rgba(153,183,164,0.24);
   border: 1px solid rgba(129,133,70,0.25);
   border-radius: 12px;
   padding: 0.6rem 0.75rem;
   margin-bottom: 0.5rem;
}


.selected-card-title {
   font-family: 'Cormorant Garamond', serif;
   font-size: 0.9rem;
   color: var(--text-main);
   font-weight: 700;
   line-height: 1.2;
}


.selected-card-author {
   font-size: 0.7rem;
   color: var(--text-soft);
   margin-top: 0.2rem;
}


/* ══════════════════════════════════════════
  RECOMMENDATION BANNER
══════════════════════════════════════════ */


.rec-banner {
   margin: 2.5rem 0 0 0;
   padding: 2rem 2.5rem;
   background: linear-gradient(135deg, rgba(255,228,210,0.95) 0%, rgba(245,177,184,0.50) 100%);
   border: 1px solid #E7D3C6;
   border-radius: 20px;
   display: flex;
   align-items: center;
   gap: 2rem;
   overflow: hidden;
   position: relative;
}


.rec-banner-icon {
   font-size: 2.5rem;
   flex-shrink: 0;
}


.rec-banner-kicker {
   font-size: 0.65rem;
   letter-spacing: 0.2em;
   text-transform: uppercase;
   color: var(--olive);
   font-weight: 700;
   margin-bottom: 0.4rem;
}


.rec-banner-headline {
   font-family: 'Cormorant Garamond', serif;
   font-size: 1.75rem;
   font-weight: 700;
   color: var(--text-main);
   line-height: 1.1;
   margin-bottom: 0.5rem;
}


.rec-banner-body {
   font-size: 0.85rem;
   color: var(--text-soft);
   line-height: 1.7;
   max-width: 650px;
}


.rec-pills {
   display: flex;
   gap: 0.5rem;
   flex-wrap: wrap;
   margin-top: 0.8rem;
}


.rec-pill {
   background: rgba(153, 183, 164, 0.24);
   border: 1px solid rgba(129, 133, 70, 0.22);
   color: var(--olive);
   font-size: 0.62rem;
   padding: 0.28rem 0.75rem;
   border-radius: 999px;
   font-weight: 600;
   letter-spacing: 0.08em;
   text-transform: uppercase;
}


/* ══════════════════════════════════════════
  SECTION HEADERS
══════════════════════════════════════════ */


.section-header {
   padding: 3rem 0 1.5rem 0;
   border-bottom: 1px solid #DDD1C5;
   margin: 0 0 2.2rem 0;
   display: flex;
   align-items: baseline;
   gap: 1.2rem;
}


.section-label {
   font-family: 'Cormorant Garamond', serif;
   font-size: 2.4rem;
   color: var(--text-main);
   margin: 0;
   font-weight: 700;
   line-height: 1;
}


.section-meta {
   font-size: 0.7rem;
   color: var(--text-faint);
   letter-spacing: 0.14em;
   text-transform: uppercase;
   margin: 0;
   font-weight: 600;
}


/* ══════════════════════════════════════════
  SHELF
══════════════════════════════════════════ */


.shelf-board {
   height: 22px;
   margin: -0.4rem 0 0.5rem 0;
   border-radius: 6px;
   background: linear-gradient(180deg, #D9B579 0%, #C79A60 50%, #A97847 100%);
   box-shadow:
       0 16px 28px rgba(160, 125, 90, 0.18),
       inset 0 3px 0 rgba(255,255,255,0.30),
       inset 0 -4px 8px rgba(130, 95, 65, 0.18);
   position: relative;
}


.shelf-board::before,
.shelf-board::after {
   content: "";
   position: absolute;
   bottom: -22px;
   width: 20px;
   height: 22px;
   background: linear-gradient(180deg, #B88456, #96683D);
   border-radius: 0 0 4px 4px;
   box-shadow: 0 6px 10px rgba(150, 110, 75, 0.18);
}


.shelf-board::before { left: 5%; }
.shelf-board::after  { right: 5%; }


/* ══════════════════════════════════════════
  BOOK COVERS
══════════════════════════════════════════ */


.book-cover-wrap {
   width: 82%;
   margin: 0 auto;
   aspect-ratio: 2 / 3;
   overflow: hidden;
   border-radius: 3px 10px 10px 3px;
   box-shadow:
       8px 14px 22px rgba(120, 95, 80, 0.18),
       inset -6px 0 10px rgba(0,0,0,0.08),
       inset 4px 0 6px rgba(255,255,255,0.08);
   transition: transform 0.25s ease, box-shadow 0.25s ease;
   position: relative;
}


.book-cover-wrap::before {
   content: "";
   position: absolute;
   left: 0; top: 0; bottom: 0;
   width: 8px;
   background: rgba(0,0,0,0.16);
   z-index: 2;
   border-radius: 3px 0 0 3px;
}


.book-cover-wrap:hover {
   transform: translateY(-9px) rotate(-0.8deg);
   box-shadow:
       12px 22px 32px rgba(120, 95, 80, 0.24),
       inset -6px 0 10px rgba(0,0,0,0.08),
       inset 4px 0 6px rgba(255,255,255,0.08);
}


.book-cover-wrap img {
   width: 100%;
   height: 100%;
   object-fit: cover;
   display: block;
}


.book-cover-placeholder {
   width: 100%;
   height: 100%;
   position: relative;
   display: flex;
   flex-direction: column;
   align-items: center;
   justify-content: center;
   padding: 1rem 0.75rem;
   overflow: hidden;
}


.bcp-0 { background: linear-gradient(160deg, #818546 0%, #9A9E5B 100%); }
.bcp-1 { background: linear-gradient(160deg, #F5B1B8 0%, #E79BA4 100%); }
.bcp-2 { background: linear-gradient(160deg, #E68A58 0%, #D9784B 100%); }
.bcp-3 { background: linear-gradient(160deg, #9BC0CC 0%, #86AFBC 100%); }
.bcp-4 { background: linear-gradient(160deg, #99B7A4 0%, #89A994 100%); }
.bcp-5 { background: linear-gradient(160deg, #C3A05B 0%, #B28F4E 100%); }
.bcp-6 { background: linear-gradient(160deg, #F0C6AE 0%, #E5B59A 100%); }
.bcp-7 { background: linear-gradient(160deg, #A8C8D3 0%, #93B8C6 100%); }


.bcp-bar {
   position: absolute;
   top: 0; left: 0; right: 0;
   height: 6px;
   background: rgba(255,255,255,0.22);
}


.bcp-frame {
   position: absolute;
   inset: 16px 12px 16px 12px;
   border: 1px solid rgba(255,255,255,0.23);
   border-radius: 4px;
   pointer-events: none;
}


.bcp-ornament {
   position: absolute;
   width: 18px;
   height: 18px;
   opacity: 0.45;
}


.bcp-ornament.tl {
   top: 20px;
   left: 14px;
   border-top: 2px solid rgba(255,255,255,0.78);
   border-left: 2px solid rgba(255,255,255,0.78);
   border-radius: 2px 0 0 0;
}


.bcp-ornament.tr {
   top: 20px;
   right: 14px;
   border-top: 2px solid rgba(255,255,255,0.78);
   border-right: 2px solid rgba(255,255,255,0.78);
   border-radius: 0 2px 0 0;
}


.bcp-ornament.bl {
   bottom: 20px;
   left: 14px;
   border-bottom: 2px solid rgba(255,255,255,0.78);
   border-left: 2px solid rgba(255,255,255,0.78);
   border-radius: 0 0 0 2px;
}


.bcp-ornament.br {
   bottom: 20px;
   right: 14px;
   border-bottom: 2px solid rgba(255,255,255,0.78);
   border-right: 2px solid rgba(255,255,255,0.78);
   border-radius: 0 0 2px 0;
}


.bcp-content {
   position: relative;
   z-index: 2;
   text-align: center;
   padding: 0 0.5rem;
}


.bcp-title {
   font-family: 'Cormorant Garamond', serif;
   font-size: 0.9rem;
   color: #FFF8F2;
   line-height: 1.25;
   font-weight: 700;
   overflow-wrap: anywhere;
   text-shadow: 0 1px 4px rgba(0,0,0,0.20);
}


.bcp-divider {
   width: 28px;
   height: 1px;
   background: rgba(255,255,255,0.45);
   margin: 0.6rem auto;
}


.bcp-author {
   font-size: 0.58rem;
   color: rgba(255,248,242,0.80);
   line-height: 1.3;
   overflow-wrap: anywhere;
   font-weight: 500;
   letter-spacing: 0.04em;
}


.rank-badge {
   position: absolute;
   top: 10px;
   right: 10px;
   background: #FFF6EE;
   color: var(--terracotta);
   font-size: 0.62rem;
   font-weight: 700;
   padding: 3px 7px;
   border-radius: 6px;
   letter-spacing: 0.03em;
   font-family: 'Outfit', sans-serif;
   z-index: 3;
   line-height: 1.4;
   box-shadow: 0 4px 10px rgba(120,90,70,0.10);
}


/* ══════════════════════════════════════════
  BOOK META
══════════════════════════════════════════ */


.book-meta {
   text-align: center;
   padding: 1rem 0.3rem 1.5rem 0.3rem;
   min-height: 95px;
}


.book-title {
   font-family: 'Cormorant Garamond', serif;
   font-size: 1.02rem;
   color: var(--text-main);
   line-height: 1.2;
   margin-bottom: 0.3rem;
   font-weight: 700;
   overflow-wrap: anywhere;
}


.book-author {
   font-size: 0.75rem;
   color: var(--text-soft);
   line-height: 1.35;
   overflow-wrap: anywhere;
   font-weight: 400;
}


/* ══════════════════════════════════════════
  BUTTONS
══════════════════════════════════════════ */


.stButton > button {
   width: 100%;
   background: rgba(255, 251, 246, 0.95) !important;
   color: var(--terracotta) !important;
   border: 1.5px solid #DDCEC2 !important;
   border-radius: 999px !important;
   padding: 0.58rem 0.9rem !important;
   font-size: 0.7rem !important;
   font-weight: 700 !important;
   letter-spacing: 0.1em !important;
   text-transform: uppercase !important;
   font-family: 'Outfit', sans-serif !important;
   box-shadow: 0 4px 12px rgba(120, 95, 80, 0.06);
   transition: all 0.18s ease !important;
}


.stButton > button:hover {
   background: #FFF0E7 !important;
   border-color: #E0B79F !important;
   color: #D9784B !important;
   transform: translateY(-1px);
   box-shadow: 0 6px 16px rgba(120, 95, 80, 0.10) !important;
}


.add-book-btn > button {
   background: var(--olive) !important;
   color: #fff !important;
   border-color: var(--olive) !important;
}


.add-book-btn > button:hover {
   background: #6e7239 !important;
   color: #fff !important;
   border-color: #6e7239 !important;
}


.get-recs-btn > button {
   background: var(--terracotta) !important;
   color: #fff !important;
   border-color: var(--terracotta) !important;
   font-size: 0.75rem !important;
   padding: 0.75rem 1rem !important;
}


.get-recs-btn > button:hover {
   background: #D9784B !important;
   color: #fff !important;
   border-color: #D9784B !important;
}


/* ══════════════════════════════════════════
  DIALOG
══════════════════════════════════════════ */


div[data-testid="stDialog"] div[role="dialog"] {
   background: var(--bg-soft) !important;
   border: 1px solid var(--border-soft) !important;
   border-radius: 22px !important;
   box-shadow: 0 24px 60px rgba(120, 95, 80, 0.18) !important;
   width: min(1080px, 92vw) !important;
   max-width: min(1080px, 92vw) !important;
   padding: 1rem 1.1rem 1.4rem 1.1rem !important;
}


.dialog-cover {
   width: 100%;
   aspect-ratio: 2 / 3;
   border-radius: 4px 12px 12px 4px;
   overflow: hidden;
   box-shadow: 10px 16px 32px rgba(120, 95, 80, 0.18);
   position: relative;
}


.dialog-cover::before {
   content: "";
   position: absolute;
   left: 0; top: 0; bottom: 0;
   width: 10px;
   background: rgba(0,0,0,0.14);
   z-index: 2;
}


.dialog-cover img {
   width: 100%;
   height: 100%;
   object-fit: cover;
}


.dialog-cover-placeholder {
   width: 100%;
   height: 100%;
   background: linear-gradient(160deg, var(--sage) 0%, var(--blue-soft) 100%);
   display: flex;
   align-items: center;
   justify-content: center;
   text-align: center;
   padding: 2rem;
   color: #FFF8F2;
   font-family: 'Cormorant Garamond', serif;
   font-size: 1.4rem;
   line-height: 1.3;
   font-weight: 700;
   overflow-wrap: anywhere;
}


.dialog-cover-placeholder span {
   display: block;
   margin-top: 0.8rem;
   font-family: 'Outfit', sans-serif;
   font-size: 0.82rem;
   color: rgba(255, 248, 242, 0.72);
   line-height: 1.4;
   font-weight: 400;
}


.dialog-title {
   font-family: 'Cormorant Garamond', serif;
   font-size: 2.1rem;
   line-height: 1.1;
   color: var(--text-main);
   margin-bottom: 0.3rem;
   font-weight: 700;
}


.dialog-author {
   color: var(--text-soft);
   font-size: 0.93rem;
   margin-bottom: 1.4rem;
   font-weight: 400;
}


.detail-block {
   padding: 0.85rem 0 1rem 0;
   border-top: 1px solid #E9DED4;
}


.detail-label {
   color: var(--text-faint);
   font-size: 0.66rem;
   letter-spacing: 0.18em;
   text-transform: uppercase;
   font-weight: 700;
   margin-bottom: 0.35rem;
}


.detail-value {
   color: var(--text-main);
   font-size: 0.93rem;
   line-height: 1.6;
   overflow-wrap: anywhere;
}


.detail-description {
   color: var(--text-main);
   font-size: 0.97rem;
   line-height: 1.85;
   max-height: 44vh;
   overflow-y: auto;
   padding-right: 0.4rem;
   overflow-wrap: anywhere;
   font-weight: 300;
}


/* ══════════════════════════════════════════
  INFO BANNER + FOOTER
══════════════════════════════════════════ */


.info-banner {
   margin: 2rem 0;
   padding: 1.2rem 1.8rem;
   background: #FBF1E8;
   border-left: 4px solid var(--terracotta);
   border-radius: 12px;
   color: var(--text-soft);
   font-size: 0.9rem;
   line-height: 1.6;
}


.bottom-divider {
   border-top: 1px solid #DDD1C5;
   margin-top: 1.5rem;
}


.footer-custom {
   padding: 2rem 0 1.5rem 0;
   display: flex;
   align-items: center;
   justify-content: space-between;
}


.footer-custom p {
   font-size: 0.68rem;
   color: var(--text-faint);
   letter-spacing: 0.1em;
   text-transform: uppercase;
   margin: 0;
   font-weight: 600;
}


.footer-mark {
   font-size: 1.2rem;
   color: var(--olive);
}


@media (max-width: 900px) {
   .hero-shelf-left, .hero-shelf-right { display: none; }
   .hero-title { font-size: 3.5rem; }
   .hero-stats { flex-direction: column; }
   .stat-item + .stat-item::before { display: none; }
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




@st.cache_data
def build_content_similarity_matrix(_items_df):
   items_sorted = _items_df.sort_values("i").reset_index(drop=True)


   titles = items_sorted.get("Title", pd.Series([""] * len(items_sorted))).fillna("")
   authors = items_sorted.get("Author", pd.Series([""] * len(items_sorted))).fillna("")
   subjects = items_sorted.get("Subjects", pd.Series([""] * len(items_sorted))).fillna("")


   api_titles = items_sorted.get("api_title", pd.Series([""] * len(items_sorted))).fillna("")
   api_authors = items_sorted.get("api_authors", pd.Series([""] * len(items_sorted))).fillna("")
   api_cats = items_sorted.get("api_categories", pd.Series([""] * len(items_sorted))).fillna("")
   api_desc = items_sorted.get("api_description", pd.Series([""] * len(items_sorted))).fillna("")


   text_data = (
       "Title: " + titles.where(titles != "", api_titles) + ". "
       "Author: " + authors.where(authors != "", api_authors) + ". "
       "Subjects: " + subjects + " " + api_cats + ". "
       "Description: " + api_desc
   )


   tfidf = TfidfVectorizer(max_features=5000)
   tfidf_matrix = tfidf.fit_transform(text_data)
   tfidf_norm = normalize(tfidf_matrix, norm="l2", axis=1)


   return tfidf_norm, items_sorted["i"].tolist()




recommendations, items, interactions = load_data()


num_books = len(items)
num_users = interactions["u"].nunique() if "u" in interactions.columns else 0




# ─── HELPERS ──────────────────────────────────────────────────────────────────


def html_block(raw):
   return "\n".join(line.strip() for line in raw.strip().splitlines() if line.strip())




def safe_text(value):
   if value is None or pd.isna(value):
       return None
   value = str(value).strip()
   if value == "" or value.lower() in ["nan", "none"]:
       return None
   return value




def clean_title(title):
   title = safe_text(title)
   if not title:
       return "Unknown Title"
   if title.endswith("/"):
       title = title[:-1].strip()
   return re.sub(r"\s+", " ", title)




def parse_possible_list(value):
   value = safe_text(value)
   if not value:
       return []
   if value.startswith("[") and value.endswith("]"):
       try:
           parsed = ast.literal_eval(value)
           if isinstance(parsed, list):
               return [str(x).strip() for x in parsed if safe_text(x)]
       except Exception:
           pass
   return [value]




def clean_single_author(author):
   author = safe_text(author)
   if not author:
       return None


   author = html.unescape(author)
   author = author.replace("[", "").replace("]", "").replace("'", "").replace('"', "")
   author = re.sub(r"\.{2,}", " ", author)
   author = re.sub(r"\s*-\s*", " ", author)
   author = re.sub(r",?\s*\b\d{4}-?\d{0,4}\b", "", author)
   author = " ".join(author.split())


   parts = [p.strip() for p in author.split(",") if p.strip()]
   if len(parts) == 2:
       return f"{parts[1]} {parts[0]}".strip()


   return author




def clean_author(author):
   values = parse_possible_list(author)


   if not values:
       return None


   cleaned_authors = []


   for value in values:
       value = safe_text(value)


       if not value:
           continue


       chunks = [x.strip() for x in value.split(";")] if ";" in value else [value]


       for chunk in chunks:
           parts = [p.strip() for p in chunk.split(",") if p.strip()]


           if len(parts) > 2 and len(parts) % 2 == 0:
               for i in range(0, len(parts), 2):
                   cleaned = clean_single_author(f"{parts[i]}, {parts[i + 1]}")
                   if cleaned:
                       cleaned_authors.append(cleaned)
           else:
               cleaned = clean_single_author(chunk)
               if cleaned:
                   cleaned_authors.append(cleaned)


   unique = []
   for author_name in cleaned_authors:
       if author_name not in unique:
           unique.append(author_name)


   return ", ".join(unique) if unique else None




def safe_thumbnail(value):
   value = safe_text(value)


   if not value:
       return None


   return value.replace("http://", "https://")




def first_available(book, columns):
   for col in columns:
       if col in book.index:
           value = safe_text(book.get(col))
           if value:
               return value
   return None




def prettify_field(value):
   value = safe_text(value)


   if not value:
       return None


   if value.startswith("[") and value.endswith("]"):
       try:
           parsed = ast.literal_eval(value)
           if isinstance(parsed, list):
               parsed = [str(x).strip() for x in parsed if safe_text(x)]
               return ", ".join(parsed)
       except Exception:
           pass


   value = html.unescape(value)
   return re.sub(r"\s+", " ", value).strip().replace(" ;", ";")




def get_book_fields(book):
   return {
       "title": clean_title(first_available(book, ["Title", "api_title"])),
       "author": clean_author(first_available(book, ["Author", "api_authors"])),
       "thumbnail": safe_thumbnail(first_available(book, ["api_thumbnail", "thumbnail"])),
       "description": prettify_field(first_available(book, ["api_description", "description_x", "description_y", "description"])),
       "categories": prettify_field(first_available(book, ["api_categories", "categories"])),
       "subjects": prettify_field(first_available(book, ["Subjects", "subjects"])),
       "published_date": prettify_field(first_available(book, ["api_published_date", "published_date", "PublishDate", "publishDate"])),
       "publisher": prettify_field(first_available(book, ["api_publisher", "Publisher", "publisher"])),
   }




def render_section_header(title, meta):
   st.markdown(html_block(f"""
   <div class="section-header">
       <h2 class="section-label">{html.escape(title)}</h2>
       <p class="section-meta">{html.escape(meta)}</p>
   </div>
   """), unsafe_allow_html=True)




def make_cover_html(fields, rank=None, dialog=False, cover_index=0):
   title = fields["title"]
   author = fields["author"]
   thumbnail = fields["thumbnail"]


   rank_html = f'<div class="rank-badge">#{rank}</div>' if rank and not dialog else ""
   palette_class = f"bcp-{cover_index % 8}"


   if thumbnail:
       if dialog:
           return html_block(f"""
           <div class="dialog-cover">
               <img src="{html.escape(thumbnail)}" alt="{html.escape(title)}">
           </div>
           """)


       return html_block(f"""
       <div class="book-cover-wrap">
           {rank_html}
           <img src="{html.escape(thumbnail)}" alt="{html.escape(title)}" loading="lazy">
       </div>
       """)


   if dialog:
       author_html = f"<span>{html.escape(author)}</span>" if author else ""
       return html_block(f"""
       <div class="dialog-cover">
           <div class="dialog-cover-placeholder">
               <div>{html.escape(title)}{author_html}</div>
           </div>
       </div>
       """)


   author_html = f'<div class="bcp-divider"></div><div class="bcp-author">{html.escape(author)}</div>' if author else ""


   return html_block(f"""
   <div class="book-cover-wrap">
       {rank_html}
       <div class="book-cover-placeholder {palette_class}">
           <div class="bcp-bar"></div>
           <div class="bcp-frame"></div>
           <div class="bcp-ornament tl"></div>
           <div class="bcp-ornament tr"></div>
           <div class="bcp-ornament bl"></div>
           <div class="bcp-ornament br"></div>
           <div class="bcp-content">
               <div class="bcp-title">{html.escape(title)}</div>
               {author_html}
           </div>
       </div>
   </div>
   """)




def render_book_meta_html(fields):
   author = fields["author"] if fields["author"] else "Unknown author"


   return html_block(f"""
   <div class="book-meta">
       <div class="book-title">{html.escape(fields["title"])}</div>
       <div class="book-author">{html.escape(author)}</div>
   </div>
   """)




@st.dialog("Book details")
def show_book_details(fields, cover_index=0):
   left, right = st.columns([1, 1.5], gap="large")


   with left:
       st.markdown(make_cover_html(fields, dialog=True, cover_index=cover_index), unsafe_allow_html=True)


   with right:
       st.markdown(f'<div class="dialog-title">{html.escape(fields["title"])}</div>', unsafe_allow_html=True)


       if fields["author"]:
           st.markdown(f'<div class="dialog-author">{html.escape(fields["author"])}</div>', unsafe_allow_html=True)


       meta_items = [
           (label, value)
           for label, value in [
               ("Publication date", fields["published_date"]),
               ("Publisher", fields["publisher"]),
               ("Categories", fields["categories"]),
               ("Subjects", fields["subjects"]),
           ]
           if value
       ]


       for i in range(0, len(meta_items), 2):
           cols = st.columns(2, gap="large")


           for j, (label, value) in enumerate(meta_items[i:i + 2]):
               with cols[j]:
                   st.markdown(html_block(f"""
                   <div class="detail-block">
                       <div class="detail-label">{html.escape(label)}</div>
                       <div class="detail-value">{html.escape(value)}</div>
                   </div>
                   """), unsafe_allow_html=True)


       if fields["description"]:
           st.markdown(html_block(f"""
           <div class="detail-block" style="margin-top:0.2rem;">
               <div class="detail-label">Description</div>
               <div class="detail-description">{html.escape(fields["description"])}</div>
           </div>
           """), unsafe_allow_html=True)




def render_book_grid(books_df, ranked=True, cols_per_row=5, section_key="section", start_index=0):
   books_list = list(books_df.iterrows())


   for row_start in range(0, len(books_list), cols_per_row):
       row_books = books_list[row_start:row_start + cols_per_row]
       row_data = []


       for col_index, (_, book) in enumerate(row_books):
           rank = row_start + col_index + 1 if ranked else None
           fields = get_book_fields(book)
           book_id = book.get("i") if "i" in book.index else f"{row_start}_{col_index}"
           cover_index = start_index + row_start + col_index
           row_data.append((book, fields, rank, book_id, col_index, cover_index))


       button_cols = st.columns(cols_per_row, gap="large")


       for idx, (_, fields, rank, book_id, col_index, cover_index) in enumerate(row_data):
           with button_cols[idx]:
               if st.button(
                   "More info",
                   key=f"btn_{section_key}_{book_id}_{row_start}_{col_index}",
                   use_container_width=True
               ):
                   show_book_details(fields, cover_index=cover_index)


       cover_cols = st.columns(cols_per_row, gap="large")


       for idx, (_, fields, rank, book_id, col_index, cover_index) in enumerate(row_data):
           with cover_cols[idx]:
               st.markdown(
                   make_cover_html(fields, rank=rank, cover_index=cover_index),
                   unsafe_allow_html=True
               )


       st.markdown('<div class="shelf-board"></div>', unsafe_allow_html=True)


       meta_cols = st.columns(cols_per_row, gap="large")


       for idx, (_, fields, rank, book_id, col_index, cover_index) in enumerate(row_data):
           with meta_cols[idx]:
               st.markdown(render_book_meta_html(fields), unsafe_allow_html=True)




# ─── RECOMMENDATION FUNCTIONS ────────────────────────────────────────────────


def get_content_recs_for_new_user(liked_item_ids, items_df, n=10):
   tfidf_norm, item_id_list = build_content_similarity_matrix(items_df)


   id_to_idx = {item_id: idx for idx, item_id in enumerate(item_id_list)}


   liked_indices = [
       id_to_idx[item_id]
       for item_id in liked_item_ids
       if item_id in id_to_idx
   ]


   if not liked_indices:
       return pd.DataFrame()


   user_vector = tfidf_norm[liked_indices].mean(axis=0)
   user_vector = np.asarray(user_vector)


   scores = cosine_similarity(user_vector, tfidf_norm)[0]


   for idx in liked_indices:
       scores[idx] = -1.0


   top_indices = np.argsort(scores)[::-1][:n]
   top_item_ids = [item_id_list[i] for i in top_indices]


   rec_books = items_df[items_df["i"].isin(top_item_ids)].copy()
   rec_books["_score"] = rec_books["i"].map({
       item_id: scores[id_to_idx[item_id]]
       for item_id in top_item_ids
   })


   rec_books = rec_books.sort_values("_score", ascending=False).head(n)


   return rec_books




def search_books(query, items_df, max_results=8):
   if not query or len(query.strip()) < 2:
       return pd.DataFrame()


   q = query.strip().lower()


   title_col = "Title" if "Title" in items_df.columns else ("api_title" if "api_title" in items_df.columns else None)
   author_col = "Author" if "Author" in items_df.columns else ("api_authors" if "api_authors" in items_df.columns else None)


   masks = []


   if title_col:
       masks.append(items_df[title_col].fillna("").str.lower().str.contains(q, regex=False))


   if author_col:
       masks.append(items_df[author_col].fillna("").str.lower().str.contains(q, regex=False))


   if not masks:
       return pd.DataFrame()


   combined_mask = masks[0]


   for mask in masks[1:]:
       combined_mask = combined_mask | mask


   return items_df[combined_mask].head(max_results)




def get_most_borrowed_books(n=10):
   top_items = interactions["i"].value_counts().head(n).index.tolist()


   top_books = items[items["i"].isin(top_items)].copy()
   top_books["rank"] = top_books["i"].apply(lambda x: top_items.index(x) + 1)
   top_books = top_books.sort_values("rank")


   return top_books




# ─── BOOK SPINE GENERATOR ────────────────────────────────────────────────────


SPINE_COLORS = [
   "#818546", "#F5B1B8", "#E68A58", "#9BC0CC", "#99B7A4", "#C3A05B",
   "#F0CDBA", "#A6C4CF", "#E6A08A", "#B6C67E", "#EBC0C5", "#8DB6C2",
   "#A4C0AD", "#D3B06E", "#F2D8C8", "#C8D9DE", "#E4B58B", "#C9D6A0",
   "#E7B6BE", "#99B7A4",
]




def make_spine(color, width, height):
   return (
       f'<div class="spine" '
       f'style="width:{width}px;height:{height}px;background:{color};"></div>'
   )




def make_shelf_row(count, side="left"):
   spines_html = ""
   spine_widths = []


   for _ in range(count):
       color = random.choice(SPINE_COLORS)
       width = random.randint(13, 22)
       height = random.randint(90, 160)


       spine_widths.append(width)
       spines_html += make_spine(color, width, height)


   gaps_width = (count - 1) * 3
   shelf_width = sum(spine_widths) + gaps_width + 18


   side_class = "right-side" if side == "right" else ""


   return (
       f'<div class="hero-shelf-unit" style="--shelf-width:{shelf_width}px;">'
       f'<div class="shelf-row-books {side_class}">'
       f'{spines_html}'
       f'</div>'
       f'<div class="shelf-plank"></div>'
       f'</div>'
   )




random.seed(42)


left_shelves = "".join(make_shelf_row(8, "left") for _ in range(3))
right_shelves = "".join(make_shelf_row(8, "right") for _ in range(3))




def fmt_number(n):
   if n >= 1000:
       return f"{n / 1000:.1f}k".replace(".0k", "k")
   return str(n)




# ─── SESSION STATE ───────────────────────────────────────────────────────────


if "user_mode" not in st.session_state:
   st.session_state.user_mode = None


if "selected_books" not in st.session_state:
   st.session_state.selected_books = []


if "new_user_recs_ready" not in st.session_state:
   st.session_state.new_user_recs_ready = False


if "new_user_name" not in st.session_state:
   st.session_state.new_user_name = ""




# ─── HERO ────────────────────────────────────────────────────────────────────


hero_html = (
   '<div class="hero-outer">'
       '<div class="hero-shelf-row">'
           f'<div class="hero-shelf-left">{left_shelves}</div>'
           '<div class="hero-center">'
               '<div class="hero-eyebrow">'
                   'University Library <span>✦</span> Book Recommender'
               '</div>'
               '<h1 class="hero-title">'
                   'Your next<br><em>great read</em><br>awaits.'
               '</h1>'
               '<p class="hero-subtitle">'
                   'For bookworms, casual readers, and curious minds '
                   'discover stories that feel like they were waiting for you.'
               '</p>'
               '<div class="hero-stats">'
                   '<div class="stat-item">'
                       f'<span class="stat-number">{fmt_number(num_books)}</span>'
                       '<span class="stat-label">Books in the library</span>'
                   '</div>'
                   '<div class="stat-item">'
                       f'<span class="stat-number">{fmt_number(num_users)}</span>'
                       '<span class="stat-label">Active readers</span>'
                   '</div>'
                   '<div class="stat-item">'
                       '<span class="stat-number">10</span>'
                       '<span class="stat-label">Picks per reader</span>'
                   '</div>'
               '</div>'
           '</div>'
           f'<div class="hero-shelf-right">{right_shelves}</div>'
       '</div>'
       '<div class="hero-ribbon">'
           '<p>'
               'Powered by <strong>hybrid recommendations</strong>'
               '&nbsp;·&nbsp; Similar readers &nbsp;·&nbsp; Reading history &nbsp;·&nbsp; Book content matching'
           '</p>'
       '</div>'
   '</div>'
)


st.markdown(hero_html, unsafe_allow_html=True)




# ─── LANDING PAGE ────────────────────────────────────────────────────────────


if st.session_state.user_mode is None:
   st.markdown("""
   <div class="path-wrapper-fixed">
       <div class="path-kicker-fixed">Choose your path</div>
       <h2 class="path-title-fixed">How would you like to get recommendations?</h2>
       <p class="path-subtitle-fixed">
           Use your existing library profile if you already have a user ID,
           or build a new reading profile by selecting books you already enjoyed.
       </p>
   </div>
   """, unsafe_allow_html=True)


   st.markdown('<div class="path-options-fixed">', unsafe_allow_html=True)


   choice_col1, choice_col2 = st.columns(2, gap="large")


   with choice_col1:
       st.markdown("""
       <div class="choice-card">
           <div class="choice-icon">📚</div>
           <div class="choice-card-title">I already have a profile</div>
           <div class="choice-card-text">
               Enter your user ID and get recommendations based on your borrowing history
               and readers with similar tastes.
           </div>
       </div>
       """, unsafe_allow_html=True)


       st.markdown('<div class="get-recs-btn">', unsafe_allow_html=True)
       if st.button("Continue as existing reader", key="landing_existing", use_container_width=True):
           st.session_state.user_mode = "existing"
           st.rerun()
       st.markdown('</div>', unsafe_allow_html=True)


   with choice_col2:
       st.markdown("""
       <div class="choice-card">
           <div class="choice-icon">✨</div>
           <div class="choice-card-title">I am a new reader</div>
           <div class="choice-card-text">
               Pick a few books you like, and we will create recommendations from their
               themes, authors, and content.
           </div>
       </div>
       """, unsafe_allow_html=True)


       st.markdown('<div class="get-recs-btn">', unsafe_allow_html=True)
       if st.button("Start as new reader", key="landing_new", use_container_width=True):
           st.session_state.user_mode = "new"
           st.session_state.new_user_recs_ready = False
           st.rerun()
       st.markdown('</div>', unsafe_allow_html=True)


   st.markdown('</div>', unsafe_allow_html=True)




# ─── EXISTING USER FLOW ──────────────────────────────────────────────────────


elif st.session_state.user_mode == "existing":


   st.markdown("""
   <div class="top-action-bar">
       <div class="mode-label">Existing reader</div>
       <h2 class="mode-title">Find recommendations from your library profile</h2>
       <div class="mode-description">
           Enter your user ID to retrieve books selected from your borrowing history,
           similar readers, and hybrid recommendation scores.
       </div>
   </div>
   """, unsafe_allow_html=True)


   back_col, _ = st.columns([1, 7])
   with back_col:
       if st.button("← Back", key="back_from_existing", use_container_width=True):
           st.session_state.user_mode = None
           st.session_state.new_user_recs_ready = False
           st.rerun()


   st.markdown("""
   <div class="search-shell">
       <p class="search-title">Your reader information</p>
   </div>
   """, unsafe_allow_html=True)


   col_name, col_id, _ = st.columns([2, 2, 5])


   with col_name:
       name_input = st.text_input("Your name", placeholder="e.g. Sophie")


   with col_id:
       user_input = st.text_input("User ID", placeholder="e.g. 1042")


   if not user_input:
       st.markdown("""
       <div class="info-banner">
           Enter your user ID above to discover books selected for you based on your
           borrowing history and the tastes of similar readers.
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
               recommended_books["rank"] = recommended_books["i"].apply(lambda x: recommended_item_ids.index(x) + 1)
               recommended_books = recommended_books.sort_values("rank").head(10)


               st.markdown(f"""
               <div class="rec-banner">
                   <div class="rec-banner-icon">📖</div>
                   <div class="rec-banner-text">
                       <div class="rec-banner-kicker">Your personalised shelf</div>
                       <div class="rec-banner-headline">Hello, {html.escape(display_name)} ! we found your next reads.</div>
                       <div class="rec-banner-body">
                           These titles were selected by combining your reading history,
                           readers with similar tastes, and book-level content patterns.
                       </div>
                       <div class="rec-pills">
                           <span class="rec-pill">Similar readers</span>
                           <span class="rec-pill">Your history</span>
                           <span class="rec-pill">Content matching</span>
                           <span class="rec-pill">Hybrid model</span>
                       </div>
                   </div>
               </div>
               """, unsafe_allow_html=True)


               render_section_header(
                   "Recommended for you",
                   "Personalised · Hybrid recommendations"
               )
               render_book_grid(
                   recommended_books,
                   ranked=True,
                   cols_per_row=5,
                   section_key="recommended",
                   start_index=0
               )


               user_interactions = interactions[interactions["u"] == selected_user]


               if not user_interactions.empty:
                   read_item_ids = user_interactions["i"].drop_duplicates().tolist()
                   read_books = items[items["i"].isin(read_item_ids)].copy()


                   if not read_books.empty:
                       render_section_header(
                           "Your reading history",
                           f"{len(read_books)} books · Previously borrowed"
                       )
                       render_book_grid(
                           read_books,
                           ranked=True,
                           cols_per_row=5,
                           section_key="history",
                           start_index=20
                       )


               top_books = get_most_borrowed_books(n=10)


               render_section_header(
                   "Most borrowed",
                   "Popular across the library"
               )
               render_book_grid(
                   top_books,
                   ranked=True,
                   cols_per_row=5,
                   section_key="popular_existing",
                   start_index=40
               )


       except ValueError:
           st.markdown("""
           <div class="info-banner">Please enter a valid numeric user ID.</div>
           """, unsafe_allow_html=True)




# ─── NEW USER FLOW ───────────────────────────────────────────────────────────


elif st.session_state.user_mode == "new":


   if not st.session_state.new_user_recs_ready:


       st.markdown("""
       <div class="top-action-bar">
           <div class="mode-label">New reader</div>
           <h2 class="mode-title">Build your reading profile</h2>
           <div class="mode-description">
               Search for books you already enjoyed. Once you add a few titles,
               we will recommend books with similar themes, authors, and content.
           </div>
       </div>
       """, unsafe_allow_html=True)


       back_col, _ = st.columns([1, 7])
       with back_col:
           if st.button("← Back", key="back_from_new", use_container_width=True):
               st.session_state.user_mode = None
               st.session_state.selected_books = []
               st.session_state.new_user_recs_ready = False
               st.rerun()


       name_col, _ = st.columns([2, 7])


       with name_col:
           new_user_name = st.text_input(
               "Your name",
               placeholder="e.g. Lucas",
               key="new_user_name_input"
           )


       search_col, _ = st.columns([5, 4])


       with search_col:
           book_query = st.text_input(
               "Search for books you liked",
               placeholder="Search by title or author...",
               key="book_search_query"
           )


       if book_query and len(book_query.strip()) >= 2:
           results = search_books(book_query, items, max_results=8)


           if results.empty:
               st.markdown("""
               <div class="info-banner">
                   No books found for this search. Try another title or author.
               </div>
               """, unsafe_allow_html=True)


           else:
               already_selected_ids = {book["i"] for book in st.session_state.selected_books}


               for _, row in results.iterrows():
                   fields = get_book_fields(row)
                   book_id = int(row["i"])


                   if book_id in already_selected_ids:
                       continue


                   result_col, btn_col = st.columns([6, 1])


                   with result_col:
                       st.markdown(html_block(f"""
                       <div class="search-result-item">
                           <div class="search-result-title">{html.escape(fields["title"])}</div>
                           <div class="search-result-author">{html.escape(fields["author"] or "Unknown author")}</div>
                       </div>
                       """), unsafe_allow_html=True)


                   with btn_col:
                       st.markdown('<div class="add-book-btn">', unsafe_allow_html=True)


                       if st.button("＋ Add", key=f"add_book_{book_id}", use_container_width=True):
                           st.session_state.selected_books.append({
                               "i": book_id,
                               "title": fields["title"],
                               "author": fields["author"] or "Unknown author"
                           })
                           st.session_state.new_user_recs_ready = False
                           st.rerun()


                       st.markdown('</div>', unsafe_allow_html=True)


       if st.session_state.selected_books:
           st.markdown("""
           <div style="margin-top:1.5rem;">
               <p style="font-size:0.68rem;letter-spacing:0.16em;text-transform:uppercase;color:var(--text-soft);font-weight:700;margin-bottom:0.6rem;">
                   Books you have added
               </p>
           </div>
           """, unsafe_allow_html=True)


           pill_cols = st.columns(min(len(st.session_state.selected_books), 5), gap="small")
           to_remove = None


           for idx, book in enumerate(st.session_state.selected_books):
               with pill_cols[idx % 5]:
                   st.markdown(f"""
                   <div class="selected-card">
                       <div class="selected-card-title">{html.escape(book["title"])}</div>
                       <div class="selected-card-author">{html.escape(book["author"])}</div>
                   </div>
                   """, unsafe_allow_html=True)


                   if st.button("✕ Remove", key=f"remove_book_{book['i']}_{idx}", use_container_width=True):
                       to_remove = idx
                       st.session_state.new_user_recs_ready = False


           if to_remove is not None:
               st.session_state.selected_books.pop(to_remove)
               st.rerun()


           st.markdown('<div style="margin-top:1.2rem;max-width:340px;">', unsafe_allow_html=True)
           st.markdown('<div class="get-recs-btn">', unsafe_allow_html=True)


           if st.button(
               f"Find my recommendations ({len(st.session_state.selected_books)} selected)",
               key="get_new_user_recs",
               use_container_width=True
           ):
               st.session_state.new_user_recs_ready = True
               st.session_state.new_user_name = new_user_name.strip() if new_user_name.strip() else "reader"
               st.rerun()


           st.markdown('</div></div>', unsafe_allow_html=True)


       else:
           st.markdown("""
           <div class="info-banner">
               Start by searching for a book or author you already like. Add at least one book
               to build your recommendation profile.
           </div>
           """, unsafe_allow_html=True)


   else:
       liked_ids = [book["i"] for book in st.session_state.selected_books]
       display_name = st.session_state.new_user_name or "reader"


       with st.spinner("Finding your recommendations..."):
           rec_books = get_content_recs_for_new_user(liked_ids, items, n=10)


       if rec_books.empty:
           st.markdown("""
           <div class="info-banner">
               We could not generate recommendations from your selected books. Try starting again
               and adding a few more titles.
           </div>
           """, unsafe_allow_html=True)


       else:
           st.markdown(f"""
           <div class="rec-banner">
               <div class="rec-banner-icon">✨</div>
               <div class="rec-banner-text">
                   <div class="rec-banner-kicker">Your personalised shelf</div>
                   <div class="rec-banner-headline">Hello, {html.escape(display_name)} ! here are your first recommendations.</div>
                   <div class="rec-banner-body">
                       These titles were selected from the books you added. We matched them using
                       shared themes, authors, subjects, and text-based content similarity.
                   </div>
                   <div class="rec-pills">
                       <span class="rec-pill">Content matching</span>
                       <span class="rec-pill">Theme similarity</span>
                       <span class="rec-pill">Based on your picks</span>
                   </div>
               </div>
           </div>
           """, unsafe_allow_html=True)


           render_section_header(
               "Recommended for you",
               "Content-based · Built from your selected books"
           )
           render_book_grid(
               rec_books,
               ranked=True,
               cols_per_row=5,
               section_key="new_user_recs",
               start_index=0
           )


           top_books = get_most_borrowed_books(n=10)


           render_section_header(
               "Most borrowed",
               "Popular across the library"
           )
           render_book_grid(
               top_books,
               ranked=True,
               cols_per_row=5,
               section_key="popular_new",
               start_index=40
           )




# ─── FOOTER ──────────────────────────────────────────────────────────────────


st.markdown('<div class="bottom-divider"></div>', unsafe_allow_html=True)


st.markdown("""
<div class="footer-custom">
   <p>University Library · Geneva · Mia Chambat &amp; Rania Ben Hamidane</p>
   <div class="footer-mark"></div>
</div>
""", unsafe_allow_html=True)
