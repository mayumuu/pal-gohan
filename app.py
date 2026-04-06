import streamlit as st

st.set_page_config(
    page_title="パルごはん 投稿下書き",
    page_icon="🍽️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    .main > div { padding-top: 1rem; }
    h1 { font-size: 1.5rem !important; }
    h2 { font-size: 1.2rem !important; }
    .stTextArea textarea { font-size: 15px; }
    .stSelectbox div[data-baseweb] { font-size: 16px; }
    .char-ok   { color: #28a745; font-size: 13px; margin: 0; }
    .char-over { color: #dc3545; font-size: 13px; margin: 0; }
</style>
""", unsafe_allow_html=True)


def stars_label(n: float) -> str:
    """セレクトボックス表示用（例：★3.5）"""
    if n == int(n):
        return f"★{int(n)}"
    return f"★{n}"


def stars_post(n: float) -> str:
    """投稿文用（例：★3.5）"""
    if n == int(n):
        return f"★{int(n)}"
    return f"★{n}"


# 5.0 → 0.5 の順で選択肢を作る
STAR_OPTIONS = {stars_label(n / 2): n / 2 for n in range(10, 0, -1)}


def make_post(
    dishes,
    product_comment,
    wife_rating,
    wife_comment,
    husband_rating,
    husband_comment,
):
    dish_lines = "\n".join(f"・{d}" for d in dishes)

    post = f"""📦 パルシステム活用！ゆる夜ごはん🍽️
{dish_lines}

{product_comment}

夫婦★評価は続きで👇

私👩{stars_post(wife_rating)}
{wife_comment}

夫👨{stars_post(husband_rating)}
{husband_comment}

#パルシステム #時短ごはん #パルシステムのある暮らし"""
    return post


# ── UI ───────────────────────────────────────────────
st.title("🍽️ パルごはん 投稿下書き")
st.caption("入力するだけで X・Threads・Instagram の下書きが完成します")

with st.form("post_form"):

    st.subheader("📦 パルシステムのごはん")
    dishes_raw = st.text_area(
        "使った商品・メニュー（1行に1品）",
        placeholder="例：\n赤魚の黒酢あんかけ\nうの花",
        height=110,
    )
    product_comment = st.text_area(
        "商品についてひとこと",
        placeholder="例：野菜を切って炒めるだけでメイン完成✨\n副菜までパルでそろうと、仕事終わりでもちゃんとごはんがラク🥹",
        height=90,
    )

    st.divider()

    st.subheader("👩 私の評価")
    wife_rating_label = st.selectbox(
        "評価", list(STAR_OPTIONS.keys()), index=0, key="wr"
    )
    wife_comment = st.text_area(
        "ひとこと",
        placeholder="例：揚げ焼きでもしっかり揚げ物感✨\n黒酢ダレ付きで、家にある野菜と炒めるだけで簡単おいしい❣️",
        height=90,
        key="wc",
    )

    st.divider()

    st.subheader("👨 夫の評価")
    husband_rating_label = st.selectbox(
        "評価", list(STAR_OPTIONS.keys()), index=1, key="hr"
    )
    husband_comment = st.text_area(
        "ひとこと",
        placeholder="例：骨取りなのも食べやすくて嬉しい☺️",
        height=90,
        key="hc",
    )

    submitted = st.form_submit_button("✨ 下書きを作る", use_container_width=True)


# ── 生成 ─────────────────────────────────────────────
if submitted:
    dishes = [d.strip() for d in dishes_raw.strip().splitlines() if d.strip()]

    missing = []
    if not dishes:
        missing.append("商品・メニュー")
    if not product_comment.strip():
        missing.append("商品についてひとこと")
    if not wife_comment.strip():
        missing.append("私のひとこと")
    if not husband_comment.strip():
        missing.append("夫のひとこと")

    if missing:
        st.warning(f"未入力の項目があります：{' / '.join(missing)}")
    else:
        wife_rating    = STAR_OPTIONS[wife_rating_label]
        husband_rating = STAR_OPTIONS[husband_rating_label]

        post = make_post(
            dishes,
            product_comment.strip(),
            wife_rating,
            wife_comment.strip(),
            husband_rating,
            husband_comment.strip(),
        )

        st.success("下書きができました！コピーして投稿に使ってください 👇")

        st.subheader("📋 X・Threads・Instagram 共通")
        post_len = len(post)
        if post_len > 280:
            st.markdown(
                f'<p class="char-over">⚠️ {post_len}文字（Xは280文字制限あり。Threads・Instagramはそのまま使えます）</p>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(f'<p class="char-ok">✅ {post_len}文字</p>', unsafe_allow_html=True)

        st.text_area("投稿文", value=post, height=370, key="post_out", label_visibility="collapsed")

        st.info("📸 写真はコピーした文を貼り付けた後、各アプリから追加してください")
