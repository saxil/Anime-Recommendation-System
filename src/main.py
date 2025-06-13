import streamlit as st
st.write('Welcome to the Anime Recommendation System! Please enter your favorite anime and we will recommend you some similar anime.')Add commentMore actions

anime_name = st.text_input('Enter your favorite anime here:')
if st.button('Recommend'):
    st.write('Recommendations for you:')
    st.write('1. Attack on Titan')
    st.write('2. Death Note')
    st.write('3. Naruto')
    st.write('4. One Piece')
    st.write('5. My Hero Academia')
if st.button("i want to start watching anime"):
    st.write('Rom-Com anime recommendations:')
    st.write('1. Toradora!')
    st.write('2. Kaguya-sama: Love is War')
    st.write('3. Your Lie in April')
    st.write('4. Clannad')
    st.write('5. Dangers in my heart')
    st.write('Action anime recommendations:')
    st.write('1. Demon Slayer')
    st.write('2. Naruto')
    st.write('3. One Piece')
    st.write('4. Attack on Titan')
    st.write('5. My Hero Academia')
    st.write('Thriller anime recommendations:')
    st.write('1. Death Note')
    st.write('2. The Promised Neverland')
    st.write('3. Tokyo Ghoul')
    st.write('4. Steins;Gate')
    st.write('5. Erased')
    
with st.sidebar:
    st.title('Anime Recommendation System🤖')
    st.write('This is a simple Anime Recommendation System that recommends you some similar anime based on your favorite anime.')
    st.write('Please enter your favorite anime in the text box above and click on the "Recommend" button to get the recommendations.')
    st.write('Enjoy!😊')
