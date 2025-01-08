import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import random

age = ctrl.Antecedent(np.arange(10, 61, 1), 'age')
mood = ctrl.Antecedent(np.arange(0, 11, 1), 'mood')
listening_time = ctrl.Antecedent(np.arange(0, 25, 1), 'listening_time')
tempo = ctrl.Antecedent(np.arange(0, 201, 1), 'tempo')
recommendation = ctrl.Consequent(np.arange(0, 101, 1), 'recommendation')

age['young'] = fuzz.trapmf(age.universe, [10, 10, 20, 30])
age['adult'] = fuzz.trapmf(age.universe, [20, 35, 40, 50])
age['senior'] = fuzz.trapmf(age.universe, [40, 50, 60, 60])
mood['sad'] = fuzz.trimf(mood.universe, [0, 0, 5])
mood['neutral'] = fuzz.trimf(mood.universe, [3, 5, 7])
mood['happy'] = fuzz.trimf(mood.universe, [5, 10, 10])
listening_time['morning'] = fuzz.trapmf(listening_time.universe, [0, 0, 9, 12])
listening_time['afternoon'] = fuzz.trimf(listening_time.universe, [11, 15, 18])
listening_time['evening'] = fuzz.trimf(listening_time.universe, [18, 19, 21])
listening_time['night'] = fuzz.trimf(listening_time.universe, [21, 24, 24])
tempo['slow'] = fuzz.trapmf(tempo.universe, [0, 0, 60, 90])
tempo['moderate'] = fuzz.trimf(tempo.universe, [80, 120, 140])
tempo['fast'] = fuzz.trapmf(tempo.universe, [130, 160, 200, 200])

recommendation['Classical'] = fuzz.trimf(recommendation.universe, [0, 0, 20])
recommendation['Ballad'] = fuzz.trimf(recommendation.universe, [15, 35, 50])
recommendation['Hip-hop'] = fuzz.trimf(recommendation.universe, [45, 60, 75])
recommendation['EDM'] = fuzz.trimf(recommendation.universe, [70, 85, 90])
recommendation['Pop'] = fuzz.trimf(recommendation.universe, [85, 100, 100])

rules = []
for age_group in age.terms.keys():
    for mood_level in mood.terms.keys():
        for time_period in listening_time.terms.keys():
            for tempo_speed in tempo.terms.keys():
                if age_group == 'young' and mood_level == 'happy':
                    if tempo_speed == 'fast':
                        rule = ctrl.Rule(age[age_group] & mood[mood_level] & listening_time[time_period] & tempo[tempo_speed], recommendation['Pop'])
                    else:
                        rule = ctrl.Rule(age[age_group] & mood[mood_level] & listening_time[time_period] & tempo[tempo_speed], recommendation['EDM'])
                elif age_group == 'senior' and mood_level == 'sad':
                    rule = ctrl.Rule(age[age_group] & mood[mood_level] & listening_time[time_period] & tempo[tempo_speed], recommendation['Classical'])
                elif tempo_speed == 'moderate':
                    rule = ctrl.Rule(age[age_group] & mood[mood_level] & listening_time[time_period] & tempo[tempo_speed], recommendation['Ballad'])
                else:
                    rule = ctrl.Rule(age[age_group] & mood[mood_level] & listening_time[time_period] & tempo[tempo_speed], recommendation['Hip-hop'])
                rules.append(rule)

recommendation_ctrl = ctrl.ControlSystem(rules)
recommendation_sim = ctrl.ControlSystemSimulation(recommendation_ctrl)

song_titles = {
    'Classical': [
        "Black Swan - BTS", "Feel My Rhythm - Red Velvet", "Miracles in December - EXO",
        "Summer Rain - Gfriend", "Nxde - (G)I-dle", "Butterfly - Loona",
        "Angel - NCT 127", "Secret Garden - Oh My Girl"
    ],
    'Ballad': [
        "This Love - Davichi", "If It Is You - Jung Seunghwan", "Fine - Taeyeon",
        "Me After You - Paul Kim", "Breathe - Lee Hi", "Unspoken Words - Davichi",
        "Through the Night - IU", "You, Clouds, Rain - Heize", "Hug Me - Jung Joon Il"
    ],
    'Hip-hop': [
        "Any Song - Zico", "Spicy - CL", "Zoom - Jessi", "Mommae - Jay Park",
        "Daechwita - Agust D", "Law - Bibi", "Uh Oh - (G)I-dle", "Don't Go Insane - DPR Ian"
    ],
    'EDM': [
        "Bang Bang Bang - Big Bang", "Crazy - Le Sserafim", "POP/STARS - K/DA",
        "Hard Carry - GOT7", "Whiplash - Aespa", "Rising Sun - TVXQ",
        "DDU-DU DDU-DU - Blackpink", "Follow - Monsta X", "Cherry Bomb - NCT 127",
        "Kick It - NCT 127"
    ],
    'Pop': [
        "Likey - Twice", "Lovesick Girls - Blackpink", "Shhh - Kiss Of Life",
        "Left & Right - Seventeen", "Say My Name - ZB1", "Cheer Up - Twice",
        "Boy With Luv - BTS", "Dynamite - BTS", "Fancy - Twice",
        "Butter - BTS"
    ]
}

def get_valid_input(prompt, min_value, max_value, input_type):
    while True:
        try:
            user_input = input_type(input(prompt))
            if min_value <= user_input <= max_value:
                return user_input
            print(f"Input must be between {min_value} and {max_value}. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid value.")

def get_category(variable, value):
    max_activation = 0
    category = None
    for term in variable.terms:
        activation = fuzz.interp_membership(variable.universe, variable[term].mf, value)
        if activation > max_activation:
            max_activation = activation
            category = term
    return category

try:
    user_age = get_valid_input("Enter your age (10-60): ", 10, 60, int)
    user_mood = get_valid_input("Enter your mood (0-10, 0=sad, 10=happy): ", 0, 10, int)
    user_listening_time = get_valid_input("Enter the hour of the day you listen to music (0-24): ", 0, 24, int)
    user_tempo = get_valid_input("Enter your preferred tempo (BPM, 0-200): ", 0, 200, int)
    print(f"Inputs: age={user_age}, mood={user_mood}, listening_time={user_listening_time}, tempo={user_tempo}")

    recommendation_sim.input['age'] = user_age
    recommendation_sim.input['mood'] = user_mood
    recommendation_sim.input['listening_time'] = user_listening_time
    recommendation_sim.input['tempo'] = user_tempo
    recommendation_sim.compute()

    age_category = get_category(age, user_age)
    mood_category = get_category(mood, user_mood)
    listening_time_category = get_category(listening_time, user_listening_time)
    tempo_category = get_category(tempo, user_tempo)
    print(f"\nCategorized Inputs:")
    print(f"  Age: {age_category}")
    print(f"  Mood: {mood_category}")
    print(f"  Listening Time: {listening_time_category}")
    print(f"  Tempo: {tempo_category}")

    if 'recommendation' not in recommendation_sim.output:
        raise ValueError("The fuzzy control system failed to compute an output.")
    recommendation_score = recommendation_sim.output['recommendation']

    if recommendation_score <= 20:
        recommended_genre = 'Classical'
    elif recommendation_score <= 50:
        recommended_genre = 'Ballad'
    elif recommendation_score <= 75:
        recommended_genre = 'Hip-hop'
    elif recommendation_score <= 90:
        recommended_genre = 'EDM'
    else:
        recommended_genre = 'Pop'

    if recommended_genre in song_titles:
        selected_songs = random.sample(song_titles[recommended_genre], 3)
        print(f"Your recommendation score is: {recommendation_score:.2f}")
        print(f"Recommended genre: {recommended_genre}")
        print("Here are 3 song suggestions:")
        for song in selected_songs:
            print(f"- {song}")
    else:
        raise ValueError(f"No songs found for genre: {recommended_genre}")

except ValueError as e:
    print(f"Input or computation error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
