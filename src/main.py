import streamlit as st
import random

ANIME_DATA = [
    {
        'title': 'Attack on Titan',
        'genre': ['Action', 'Dark Fantasy', 'Post-apocalyptic'],
        'description': 'In a world where humanity resides within enormous walled cities to protect themselves from giant humanoid Titans, Eren Yeager vows to exterminate the Titans after they bring about the destruction of his hometown and the death of his mother. The story follows Eren, his adoptive sister Mikasa Ackerman, and their friend Armin Arlert, as they join the military to fight the Titans and uncover the mysteries of their world.',
        'rating': 9.0
    },
    {
        'title': 'Death Note',
        'genre': ['Thriller', 'Supernatural', 'Mystery'],
        'description': 'A brilliant high school student named Light Yagami discovers a mysterious notebook called the Death Note, which grants its user the ability to kill anyone whose name and face they know. Light decides to use the Death Note to rid the world of criminals, but his actions attract the attention of a brilliant detective known only as L. A deadly game of cat and mouse ensues as Light tries to create his ideal world while evading L.',
        'rating': 8.6
    },
    {
        'title': 'Naruto',
        'genre': ['Action', 'Adventure', 'Fantasy'],
        'description': 'Naruto Uzumaki, a young ninja who seeks recognition from his peers and dreams of becoming the Hokage, the leader of his village. The story is told in two parts – the first set in Naruto\'s pre-teen years, and the second in his teens. Naruto is an orphaned ninja from the Hidden Leaf Village, who is ostracized by the villagers because he is the host of the Nine-Tailed Fox, a powerful creature that attacked the village years ago.',
        'rating': 8.4
    },
    {
        'title': 'One Piece',
        'genre': ['Action', 'Adventure', 'Fantasy'],
        'description': 'Follows the adventures of Monkey D. Luffy, a boy whose body gained the properties of rubber after unintentionally eating a Devil Fruit. With his crew of pirates, named the Straw Hat Pirates, Luffy explores the Grand Line in search of the world\'s ultimate treasure known as "One Piece" in order to become the next Pirate King. The series is renowned for its world-building, humor, and diverse cast of characters.',
        'rating': 8.7
    },
    {
        'title': 'My Hero Academia',
        'genre': ['Action', 'Superhero', 'Comedy'],
        'description': 'In a world where about 80% of the population has a superpower called a "Quirk", Izuku Midoriya is a boy born without a Quirk, but still dreams of becoming a superhero himself. He is scouted by All Might, Japan\'s greatest hero, who chooses Midoriya as his successor and shares his Quirk with him after recognizing his potential. The story follows Midoriya\'s entrance into U.A. High School, a prestigious school for heroes in training.',
        'rating': 8.3
    },
    {
        'title': 'Toradora!',
        'genre': ['Rom-Com', 'Slice of Life', 'Comedy'],
        'description': 'Ryuji Takasu is a gentle high school student with an intimidating face, leading many to mistake him for a delinquent. Taiga Aisaka is a small, doll-like student who is anything but cute and cuddly – she has a fierce temper and is known as the "Palmtop Tiger". Due to an embarrassing mistake, they learn each other\'s secrets: Ryuji is in love with Taiga\'s best friend, Minori, and Taiga is in love with Ryuji\'s best friend, Yusaku. They agree to help each other win over their crushes.',
        'rating': 8.1
    },
    {
        'title': 'Kaguya-sama: Love is War',
        'genre': ['Rom-Com', 'Psychological', 'Slice of Life'],
        'description': 'At the prestigious Shuchiin Academy, student council president Miyuki Shirogane and vice-president Kaguya Shinomiya are considered the perfect couple by many. However, despite having feelings for each other, they are too proud to confess, leading to a series of elaborate schemes and mind games to try and make the other confess first. Their daily interactions become a battle of wits and romance.',
        'rating': 8.5
    },
    {
        'title': 'Your Lie in April',
        'genre': ['Rom-Com', 'Drama', 'Music'],
        'description': 'Kosei Arima is a former child prodigy pianist who loses the ability to hear the sound of his own piano after his mother\'s death. Two years later, he meets Kaori Miyazono, a free-spirited violinist whose unique playing style rekindles Kosei\'s passion for music and helps him confront his past. Together, they navigate the challenges of music competitions and their budding feelings for each other.',
        'rating': 8.7
    },
    {
        'title': 'Clannad',
        'genre': ['Rom-Com', 'Drama', 'Supernatural', 'Slice of Life'],
        'description': 'Tomoya Okazaki is a delinquent who finds life dull and believes he\'ll never amount to anything. He meets Nagisa Furukawa, a sweet and gentle girl who is repeating her senior year of high school due to illness. As Tomoya gets to know Nagisa and her friends, he starts to find purpose in his life and helps them overcome their personal problems. The series is known for its emotional depth and exploration of family and relationships.',
        'rating': 8.0
    },
    {
        'title': 'Dangers in my Heart',
        'genre': ['Rom-Com', 'Slice of Life', 'School'],
        'description': 'Kyoutaro Ichikawa is a gloomy and quiet middle school student who often fantasizes about murdering his popular and beautiful classmate, Anna Yamada. However, as he observes her more closely, he starts to realize that she is quite quirky and endearing in her own way. Their interactions lead to an unlikely friendship and a slow-budding romance as they navigate the awkwardness of adolescence.',
        'rating': 8.4
    },
    {
        'title': 'Demon Slayer: Kimetsu no Yaiba',
        'genre': ['Action', 'Dark Fantasy', 'Supernatural'],
        'description': 'Tanjiro Kamado is a kind-hearted boy who sells charcoal for a living. His peaceful life is shattered when demons slaughter his entire family, except for his younger sister Nezuko, who is turned into a demon herself. Tanjiro embarks on a perilous journey to become a demon slayer and find a way to turn his sister back into a human, seeking vengeance against the demon who killed his family.',
        'rating': 8.5
    },
    {
        'title': 'The Promised Neverland',
        'genre': ['Thriller', 'Mystery', 'Sci-Fi', 'Dark Fantasy'],
        'description': 'Emma, Norman, and Ray are the brightest kids at the Grace Field House orphanage. Under the care of the woman they refer to as "Mom," all the kids have enjoyed a comfortable life. However, their idyllic world is turned upside down when they discover the horrifying truth about their existence and the dark secret of the orphanage. They must use their wits and courage to escape their predetermined fate.',
        'rating': 8.4
    },
    {
        'title': 'Tokyo Ghoul',
        'genre': ['Thriller', 'Dark Fantasy', 'Horror', 'Supernatural'],
        'description': 'Ken Kaneki, a college student, barely survives a deadly encounter with Rize Kamishiro, a woman who is revealed to be a ghoul – a creature that feeds on human flesh. Kaneki is taken to the hospital in critical condition and undergoes surgery that transforms him into a half-ghoul. Now, he must learn to live among ghouls and hide his new identity from humans, while struggling with his hunger and the moral implications of his new existence.',
        'rating': 7.8
    },
    {
        'title': 'Steins;Gate',
        'genre': ['Thriller', 'Sci-Fi', 'Psychological', 'Drama'],
        'description': 'Rintaro Okabe, a self-proclaimed "mad scientist," runs a "Future Gadget Laboratory" in Akihabara with his friends Mayuri Shiina and Itaru "Daru" Hashida. While attempting to create a time machine by modifying a microwave oven, they discover that they can send text messages to the past. Their experiments with time travel soon attract the attention of a mysterious organization called SERN, leading to a series of tragic events that Okabe must try to prevent.',
        'rating': 9.1
    },
    {
        'title': 'Erased (Boku dake ga Inai Machi)',
        'genre': ['Thriller', 'Mystery', 'Supernatural', 'Psychological'],
        'description': 'Satoru Fujinuma is a young man who possesses an ability called "Revival," which sends him back in time moments before a life-threatening incident occurs, allowing him to prevent it. When his mother is murdered by an unknown assailant, Satoru\'s Revival sends him 18 years into the past, giving him the opportunity to prevent not only his mother\'s death but also a kidnapping incident that took the lives of three of his childhood friends.',
        'rating': 8.3
    },
    {
        'title': 'Code Geass: Lelouch of the Rebellion',
        'genre': ['Action', 'Sci-Fi', 'Mecha', 'Military', 'Drama'],
        'description': 'In an alternate timeline, the Holy Britannian Empire has conquered Japan, renaming it Area 11. Lelouch Lamperouge, an exiled Britannian prince, receives a mysterious power called Geass, which allows him to command anyone to do anything. Lelouch adopts the persona of Zero and leads a rebellion against Britannia to create a new world for his sister and uncover the truth about his mother\'s death.',
        'rating': 8.7
    },
    {
        'title': 'Fullmetal Alchemist: Brotherhood',
        'genre': ['Action', 'Adventure', 'Fantasy', 'Steampunk'],
        'description': 'Brothers Edward and Alphonse Elric use alchemy in an attempt to resurrect their deceased mother, but the experiment goes horribly wrong. Edward loses his left leg and Alphonse loses his entire body, his soul being bound to a suit of armor by Edward, who sacrifices his right arm. The brothers embark on a quest to find the Philosopher\'s Stone, a mythical artifact that can restore their bodies.',
        'rating': 9.1
    },
    {
        'title': 'Cowboy Bebop',
        'genre': ['Sci-Fi', 'Action', 'Adventure', 'Space Western', 'Neo-noir'],
        'description': 'In the year 2071, humanity has colonized several planets and moons of the solar system. Amidst a rising crime rate, the Inter Solar System Police (ISSP) legalize registered bounty hunters, known as "Cowboys," to hunt down criminals. The series follows the adventures of a group of bounty hunters traveling on their spaceship, the Bebop, as they chase bounties and confront their pasts.',
        'rating': 8.8
    },
    {
        'title': 'Neon Genesis Evangelion',
        'genre': ['Sci-Fi', 'Mecha', 'Psychological', 'Post-apocalyptic'],
        'description': 'In a post-apocalyptic world, a paramilitary organization called NERV fights against monstrous beings known as Angels using giant mechas called Evangelions. Shinji Ikari, a teenage boy, is recruited by his estranged father, the commander of NERV, to pilot an Evangelion and protect humanity. The series delves into the psychological and emotional struggles of the pilots and the nature of humanity.',
        'rating': 8.5
    },
    {
        'title': 'Mushishi',
        'genre': ['Slice of Life', 'Supernatural', 'Mystery', 'Historical'],
        'description': 'Mushi are ethereal beings that exist in a primordial state, often causing unexplainable phenomena. Ginko is a "Mushi Master" who travels the land to investigate and help people afflicted by Mushi-related problems. The series is episodic, with each episode focusing on a different case and exploring the delicate balance between humans and Mushi.',
        'rating': 8.7
    },
    {
        'title': 'Vinland Saga',
        'genre': ['Action', 'Adventure', 'Historical', 'Drama'],
        'description': 'Set in 11th century England, the story follows Thorfinn, a young Icelandic warrior who seeks revenge for the murder of his father. He joins the crew of Askeladd, the man responsible for his father\'s death, hoping to one day challenge him to a duel. The series explores themes of vengeance, war, and the meaning of a true warrior, set against the backdrop of Viking raids and political intrigue.',
        'rating': 8.8
    },
    {
        'title': 'Jujutsu Kaisen',
        'genre': ['Action', 'Supernatural', 'Dark Fantasy', 'School'],
        'description': 'Yuji Itadori, a kind-hearted high school student with immense physical strength, swallows a cursed finger to save his friend, becoming the host of Sukuna, a powerful Curse. He joins the Tokyo Jujutsu High School, where he learns to control his cursed energy and fight against other Curses. The series follows Yuji and his classmates as they battle powerful Curses and protect humanity from supernatural threats.',
        'rating': 8.7
    },
    {
        'title': 'Spy x Family',
        'genre': ['Comedy', 'Action', 'Slice of Life', 'Espionage'],
        'description': 'In order to maintain peace between rival nations Westalis and Ostania, a Westalian spy codenamed "Twilight" is tasked with creating a fake family to get close to a high-ranking Ostanian politician. He adopts a telepathic orphan girl named Anya as his daughter and marries Yor Briar, an assassin, neither of whom are aware of his true identity or each other\'s secrets. The series follows their comedic attempts to maintain their facade while navigating family life.',
        'rating': 8.6
    },
    {
        'title': 'Mob Psycho 100',
        'genre': ['Action', 'Comedy', 'Supernatural', 'Slice of Life'],
        'description': 'Shigeo Kageyama, nicknamed "Mob," is an eighth-grade esper with immense psychic powers. He works part-time for Arataka Reigen, a con artist who claims to be a psychic, helping him with exorcisms. Mob tries to live a normal life and suppress his powers, but when his emotions reach 100%, his powers are unleashed in an overwhelming display. The series follows Mob\'s journey of self-discovery and his encounters with other espers and supernatural beings.',
        'rating': 8.6
    },
    {
        'title': 'Haikyuu!!',
        'genre': ['Sports', 'Comedy', 'Drama', 'School'],
        'description': 'Shoyo Hinata, a short middle school student, becomes obsessed with volleyball after watching a national championship match. He joins his school\'s volleyball team, but they are defeated by the team of Tobio Kageyama, a prodigious setter known as the "King of the Court." Hinata vows to surpass Kageyama and enters Karasuno High School, only to find that Kageyama is also a student there. They must learn to work together to revive Karasuno\'s reputation as a volleyball powerhouse.',
        'rating': 8.8
    },
    {
        'title': 'Violet Evergarden',
        'genre': ['Slice of Life', 'Drama', 'Fantasy'],
        'description': 'The Great War has ended, and Violet Evergarden, a young former soldier raised for the sole purpose of decimating enemy lines, is left scarred and emotionless. She takes up a job as an Auto Memory Doll, a ghostwriter who transcribes people\'s thoughts and feelings into letters. Through her work, Violet embarks on a journey of self-discovery, learning about human emotions and the meaning of love.',
        'rating': 8.6
    },
    {
        'title': 'Re:Zero - Starting Life in Another World',
        'genre': ['Dark Fantasy', 'Isekai', 'Thriller', 'Psychological'],
        'description': 'Subaru Natsuki is suddenly summoned to another world. Just as he is attacked by thugs, he is saved by a mysterious silver-haired half-elf named Satella. To repay her, he offers to help her find a stolen insignia. However, they are both brutally murdered. Subaru then awakens to find himself back at the point where he first arrived in the new world. He discovers he has an ability he calls "Return by Death," allowing him to go back in time after dying, though he retains the memories of his past lives.',
        'rating': 8.1
    },
    {
        'title': 'Made in Abyss',
        'genre': ['Adventure', 'Dark Fantasy', 'Sci-Fi', 'Mystery'],
        'description': 'An enormous chasm known as the Abyss is the last unexplored place in the world. Strange and wonderful creatures reside in its depths, along with precious relics from a long-lost civilization. Riko, an orphaned girl living in a town on the edge of the Abyss, dreams of becoming a legendary Cave Raider like her mother. One day, she befriends a humanoid robot named Reg, and together they descend into the Abyss to uncover its secrets and find Riko\'s mother.',
        'rating': 8.8
    },
    {
        'title': 'Ranking of Kings (Ousama Ranking)',
        'genre': ['Fantasy', 'Adventure', 'Coming-of-age'],
        'description': 'Bojji is a deaf, powerless prince who dreams of becoming the world\'s greatest king. However, he is constantly ridiculed by his subjects for his lack of strength and intelligence. One day, Bojji befriends Kage, a survivor of an assassinated assassin clan, who understands Bojji\'s words despite his inability to speak. Together, they embark on an adventure to prove Bojji\'s worth and uncover the conspiracies within the kingdom.',
        'rating': 8.9
    },
    {
        'title': 'Cyberpunk: Edgerunners',
        'genre': ['Sci-Fi', 'Action', 'Cyberpunk', 'Crime'],
        'description': 'Based on the video game Cyberpunk 2077, this standalone series tells the story of David Martinez, a street kid trying to survive in Night City, a technology and body-modification-obsessed city of the future. Having everything to lose, he chooses to stay alive by becoming an edgerunner—a high-tech mercenary outlaw also known as a cyberpunk. His journey is one of violence, ambition, and the search for belonging in a city that consumes its inhabitants.',
        'rating': 8.6
    }
]

# Define a small list of common English stop words
STOP_WORDS = set([
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
    'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
    'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
    'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
    'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
    'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
    'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
    'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
    'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
    'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
    'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 're', 've'
])

def extract_keywords(description_text):
    """Extracts significant keywords from an anime's description."""
    if not isinstance(description_text, str):
        return set()
    words = description_text.lower().split()
    keywords = set(word for word in words if word.isalnum() and word not in STOP_WORDS)
    return keywords

def recommend_similar_anime(favorite_anime_title, anime_data, top_n=5):
    """Recommends anime similar to the favorite_anime_title based on genre and description keywords."""
    favorite_anime = None
    for anime in anime_data:
        if anime['title'].lower() == favorite_anime_title.lower():
            favorite_anime = anime
            break

    if not favorite_anime:
        return [] # Favorite anime not found

    fav_genres = set(genre.lower() for genre in favorite_anime['genre'])
    fav_keywords = extract_keywords(favorite_anime['description'])

    similarities = []
    for anime in anime_data:
        if anime['title'].lower() == favorite_anime_title.lower():
            continue # Don't compare with itself

        current_genres = set(genre.lower() for genre in anime['genre'])
        current_keywords = extract_keywords(anime['description'])

        similarity_score = 0
        # Score for matching genres
        similarity_score += len(fav_genres.intersection(current_genres)) * 2
        # Score for common keywords
        similarity_score += len(fav_keywords.intersection(current_keywords)) * 1

        if similarity_score > 0:
            similarities.append({'title': anime['title'], 'score': similarity_score})

    # Sort by score in descending order
    similarities.sort(key=lambda x: x['score'], reverse=True)

    return [anime['title'] for anime in similarities[:top_n]]

def recommend_by_genre(genre_name, anime_data, n=3):
    """Recommends N anime titles for a given genre, selected randomly."""
    genre_name_lower = genre_name.lower()
    genre_anime = [
        anime['title'] for anime in anime_data
        if genre_name_lower in [g.lower() for g in anime['genre']]
    ]

    if not genre_anime:
        return [] # No anime found for this genre

    if len(genre_anime) <= n:
        return genre_anime # Return all if less than or equal to N
    
    return random.sample(genre_anime, n)

st.title('Anime Recommendation System')
st.write('Welcome to the Anime Recommendation System! Discover anime based on your favorites or explore genres if you\'re new!')

# Initialize session state for genre recommendations
if 'genre_recommendations' not in st.session_state:
    st.session_state.genre_recommendations = None
if 'selected_genre' not in st.session_state:
    st.session_state.selected_genre = None

# Section 1: Recommend based on favorite anime
st.header('Recommend Based on Your Favorite Anime')
anime_name = st.text_input('Enter your favorite anime title here:', key='favorite_anime_input')

if st.button('Recommend Similar Anime', key='recommend_similar_btn'):
    st.session_state.genre_recommendations = None # Clear genre recommendations
    st.session_state.selected_genre = None
    if anime_name:
        recommendations = recommend_similar_anime(anime_name, ANIME_DATA, top_n=5)
        if recommendations:
            st.subheader(f"Top 5 recommendations similar to '{anime_name}':")
            for i, rec_anime in enumerate(recommendations):
                st.write(f"{i+1}. {rec_anime}")
        else:
            st.warning(f"Could not find recommendations for '{anime_name}'. Please check the spelling or try another anime. This tool works best with titles from its dataset.")
    else:
        st.error("Please enter an anime title.")

# Section 2: Recommendations for new watchers by genre
st.header('New to Anime? Explore by Genre!')

if st.button("I want to start watching anime", key="new_watcher_main_btn"):
    # This button itself doesn't do much other than act as a header for the genre buttons below
    # Or, it could set a state to show the genre buttons, if they were initially hidden.
    # For now, let's assume genre buttons are always visible if this section is active.
    st.session_state.show_genre_buttons = True # We can use this if we want to toggle visibility

# Define genres and their buttons
genres_to_show = ["Rom-Com", "Action", "Thriller", "Sci-Fi", "Fantasy", "Slice of Life"]
cols = st.columns(3) # Create 3 columns for buttons

current_col = 0
for genre in genres_to_show:
    button_label = f"Show {genre}"
    if cols[current_col].button(button_label, key=f"genre_btn_{genre.replace('-', '_').lower()}"):
        st.session_state.selected_genre = genre
        recommendations = recommend_by_genre(genre, ANIME_DATA, n=3)
        if recommendations:
            st.session_state.genre_recommendations = recommendations
        else:
            st.session_state.genre_recommendations = [] # No recommendations for this genre
    current_col = (current_col + 1) % 3


# Display genre recommendations if a genre has been selected
if st.session_state.selected_genre and st.session_state.genre_recommendations is not None:
    st.subheader(f"Top 3 {st.session_state.selected_genre} Anime Recommendations:")
    if st.session_state.genre_recommendations:
        for i, rec_anime in enumerate(st.session_state.genre_recommendations):
            # Try to find full anime details to show more info
            anime_details = next((item for item in ANIME_DATA if item["title"] == rec_anime), None)
            if anime_details:
                with st.expander(f"{i+1}. {rec_anime} (Rating: {anime_details.get('rating', 'N/A')})"):
                    st.write(f"**Genre:** {', '.join(anime_details.get('genre', []))}")
                    st.caption(f"**Description:** {anime_details.get('description', 'No description available.')}")
            else:
                st.write(f"{i+1}. {rec_anime}")
    else:
        st.info(f"No {st.session_state.selected_genre} anime found in our dataset for recommendations right now.")


with st.sidebar:
    st.title('Anime Recommendation System🤖')
    st.write('This is a simple Anime Recommendation System that recommends you some similar anime based on your favorite anime.')
    st.write('Please enter your favorite anime in the text box above and click on the "Recommend" button to get the recommendations.')
    st.write('Enjoy!😊')
