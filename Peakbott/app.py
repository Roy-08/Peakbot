from flask import Flask, request, jsonify, render_template
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

app = Flask(__name__)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('C:\\xampp\\htdocs\\Peakbot\\intents.json', 'r', encoding='utf-8') as json_data:

    intents = json.load(json_data)

data = torch.load('C:\\xampp\\htdocs\\Peakbot\\data.pth')


input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "PeakBot"

analyzer = SentimentIntensityAnalyzer()

user_messages = []
message_threshold = 3  
waiting_for_genre = False  

music_details = {
    "happy": {
        "bollywood": [
            {
                "name": "Tum Hi Ho",
                "artist": "Arijit Singh",
                "url": "https://www.last.fm/music/Arijit+Singh/_/Tum+Hi+Ho"
            },
            {
                "name": "Tum Tak",
                "artist": "A.R. Rahman",
                "url": "https://www.last.fm/music/A.R.+Rahman/_/Tum+Tak"
            },
            {
                "name": "Chaleya",
                "artist": "Anirudh Ravichander",
                "url": "https://www.last.fm/music/Anirudh+Ravichander/_/Chaleya+(From+%22Jawan%22)"
            },
            {
                "name": "O'Meri Laila",
                "artist": "Atif Aslam",
                "url": "https://www.last.fm/music/Atif+Aslam/_/O%27Meri+Laila"
            },
            {
                "name": "Akhiyaan Gulaab",
                "artist": "Mitraz",
                "url": "https://www.last.fm/music/Mitraz/_/Akhiyaan+Gulaab"
            },
            {
                "name": "Gallan Goodiyaan",
                "artist": "Yashita Sharma",
                "url": "https://www.last.fm/music/Yashita+Sharma/_/Gallan+Goodiyaan"
            },
            {
                "name": "Balam Pichkari",
                "artist": "Vishal Dadlani & Shalmali Kholgade",
                "url": "https://www.last.fm/music/Vishal+Dadlani+&+Shalmali+Kholgade/_/Balam+Pichkari"
            },
            {
                "name": "Kabhi Kabhi Aditi",
                "artist": "Rashid Ali",
                "url": "https://www.last.fm/music/Rashid+Ali/_/Kabhi+Kabhi+Aditi"
            },
            {
                "name": "Senorita",
                "artist": "Farhan Akhtar",
                "url": "https://www.last.fm/music/Farhan+Akhtar/_/Senorita"
            },
            {
                "name": "Kya Mujhe Pyaar Hai",
                "artist": "KK",
                "url": "https://www.last.fm/music/KK/_/Kya+Mujhe+Pyaar+Hai"
            },
        ],
        "marathi": [
            {
                "name": "Zingat",
                "artist": "Ajay-Atul",
                "url": "https://www.last.fm/music/Ajay-Atul/_/Zingat"
            },
            {
                "name": "Mala Jau Dya Na Ghari",
                "artist": "Ajay-Atul",
                "url": "https://www.last.fm/music/Ajay-Atul/_/Mala+Jau+Dya+Na+Ghari"
            },
            {
                "name": "Khel Mandla",
                "artist": "Ajay-Atul",
                "url": "https://www.last.fm/music/Ajay-Atul/_/Khel+Mandla"
            },
            {
                "name": "Aatach Baya Ka Baara",
                "artist": "Sukhwinder Singh",
                "url": "https://www.last.fm/music/Sukhwinder+Singh/_/Aatach+Baya+Ka+Baara"
            },
            {
                "name": "Deewana Main Chala",
                "artist": "Makarand Anaspure",
                "url": "https://www.last.fm/music/Makarand+Anaspure/_/Deewana+Main+Chala"
            },
            {
                "name": "Saath De Tu Mala",
                "artist": "Rani",
                "url": "https://www.last.fm/music/Rani/_/Saath+De+Tu+Mala"
            },
            {
                "name": "Boli Sakhare",
                "artist": "Vaishali Samant",
                "url": "https://www.last.fm/music/Vaishali+Samant/_/Boli+Sakhare"
            },
            {
                "name": "Mala Jau Dya Na Ghari",
                "artist": "Sukhwinder Singh",
                "url": "https://www.last.fm/music/Sukhwinder+Singh/_/Mala+Jau+Dya+Na+Ghari"
            },
            {
                "name": "Nandi Nandi",
                "artist": "Ajay-Atul",
                "url": "https://www.last.fm/music/Ajay-Atul/_/Nandi+Nandi"
            },
            {
                "name": "Mala Jau Dya Na Ghari",
                "artist": "Sukhwinder Singh",
                "url": "https://www.last.fm/music/Sukhwinder+Singh/_/Mala+Jau+Dya+Na+Ghari"
            },
        ],
        "90's": [
            {
                "name": "Pehla Nasha",
                "artist": "Udit Narayan",
                "url": "https://www.last.fm/music/Udit+Narayan/_/Pehla+Nasha"
            },
            {
                "name": "Chura Liya Hai Tumne Jo",
                "artist": "Asha Bhosle",
                "url": "https://www.last.fm/music/Asha+Bhosle/_/Chura+Liya+Hai+Tumne+Jo"
            },
            {
                "name": "Tujhe Dekha To",
                "artist": "Kumar Sanu",
                "url": "https://www.last.fm/music/Kumar+Sanu/_/Tujhe+Dekha+To"
            },
            {
                "name": "Dil Diyan Gallan",
                "artist": "Atif Aslam",
                "url": "https://www.last.fm/music/Atif+Aslam/_/Dil+Diyan+Gallan"
            },
            {
                "name": "Ae Mere Humsafar",
                "artist": "Vinod Rathod & Sadhana Sargam",
                "url": "https://www.last.fm/music/Vinod+Rathod/_/Ae+Mere+Humsafar"
            },
            {
                "name": "Tera Hone Laga Hoon",
                "artist": "Atif Aslam",
                "url": "https://www.last.fm/music/Atif+Aslam/_/Tera+Hone+Laga+Hoon"
            },
            {
                "name": "Aankhon Ki Gustakhiyan",
                "artist": "Asha Bhosle",
                "url": "https://www.last.fm/music/Asha+Bhosle/_/Aankhon+Ki+Gustakhiyan"
            },
            {
                "name": "Mera Joota Hai Japani",
                "artist": "Mukesh",
                "url": "https://www.last.fm/music/Mukesh/_/Mera+Joota+Hai+Japani"
            },
            {
                "name": "Chura Liya Hai Tumne Jo",
                "artist": "Asha Bhosle",
                "url": "https://www.last.fm/music/Asha+Bhosle/_/Chura+Liya+Hai+Tumne+Jo"
            },
            {
                "name": "Ye sham mastani",
                "artist": "Kishore Kumar",
                "url": "https://www.last.fm/music/Kishore+Kumar/_/Ye+Sham+Mastani"
            },
        ],
        "hip-hop": [
        {
            "name": "Good Life",
            "artist": "Kanye West",
            "url": "https://www.last.fm/music/Kanye+West/_/Good+Life"
        },
        {
            "name": "Can't Stop",
            "artist": "Red Hot Chili Peppers",
            "url": "https://www.last.fm/music/Red+Hot+Chili+Peppers/_/Can't+Stop"
        },
        {
            "name": "Happy",
            "artist": "Pharrell Williams",
            "url": "https://www.last.fm/music/Pharrell+Williams/_/Happy"
        },
        {
            "name": "Juicy",
            "artist": "The Notorious B.I.G.",
            "url": "https://www.last.fm/music/The+Notorious+B.I.G./_/Juicy"
        },
        {
            "name": "Uptown Funk",
            "artist": "Mark Ronson ft. Bruno Mars",
            "url": "https://www.last.fm/music/Mark+Ronson/_/Uptown+Funk"
        },
        {
            "name": "I Gotta Feeling",
            "artist": "The Black Eyed Peas",
            "url": "https://www.last.fm/music/The+Black+Eyed+Peas/_/I+Gotta+Feeling"
        },
        {
            "name": "Walk This Way",
            "artist": "Run-D.M.C. ft. Aerosmith",
            "url": "https://www.last.fm/music/Run-D.M.C./_/Walk+This+Way"
        },
        {
            "name": "Good Vibrations",
            "artist": "Marky Mark and the Funky Bunch",
            "url": "https://www.last.fm/music/Marky+Mark+and+the+Funky+Bunch/_/Good+Vibrations"
        },
        {
            "name": "Best Day of My Life",
            "artist": "American Authors",
            "url": "https://www.last.fm/music/American+Authors/_/Best+Day+of+My+Life"
        },
        {
            "name": "Old Town Road",
            "artist": "Lil Nas X ft. Billy Ray Cyrus",
            "url": "https://www.last.fm/music/Lil+Nas+X/_/Old+Town+Road"
        }
    ]
    },
    "sad": {
        "bollywood": [
            {
                "name": "Tujhe Kitna Chahne Lage",
                "artist": "Arijit Singh",
                "url": "https://www.last.fm/music/Arijit+Singh/_/Tujhe+Kitna+Chahne+Lage"
            },
            {
                "name": "Channa Mereya",
                "artist": "Arijit Singh",
                "url": "https://www.last.fm/music/Arijit+Singh/_/Channa+Mereya"
            },
            {
                "name": "Kabira",
                "artist": "Aditi Rao Hydari",
                "url": "https://www.last.fm/music/Aditi+Rao+Hydari/_/Kabira"
            },
            {
                "name": "Ae Mere Humsafar",
                "artist": "Suman Kalyanpur",
                "url": "https://www.last.fm/music/Suman+Kalyanpur/_/Ae+Mere+Humsafar"
            },
            {
                "name": "Dil Ke Paas",
                "artist": "Kumar Sanu",
                "url": "https://www.last.fm/music/Kumar+Sanu/_/Dil+Ke+Paas"
            },
            {
                "name": "Kabhi Alvida Naa Kehna",
                "artist": "A.R. Rahman",
                "url": "https://www.last.fm/music/A.R.+Rahman/_/Kabhi+Alvida+Naa+Kehna"
            },
            {
                "name": "Pyaar Ke Pal",
                "artist": "Arijit Singh",
                "url": "https://www.last.fm/music/Arijit+Singh/_/Pyaar+Ke+Pal"
            },
            {
                "name": "Hasi",
                "artist": "Afsana Khan",
                "url": "https://www.last.fm/music/Afsana+Khan/_/Hasi"
            },
            {
                "name": "Koi Fariyaad",
                "artist": "Jagjit Singh",
                "url": "https://www.last.fm/music/Jagjit+Singh/_/Koi+Fariyaad"
            },
            {
                "name": "Dil Diyan Gallan",
                "artist": "Atif Aslam",
                "url": "https://www.last.fm/music/Atif+Aslam/_/Dil+Diyan+Gallan"
            },
        ],
        "marathi": [
            {
                "name": "Kahe Chaar Bole",
                "artist": "Sukhwinder Singh",
                "url": "https://www.last.fm/music/Sukhwinder+Singh/_/Kahe+Chaar+Bole"
            },
            {
                "name": "Mala Jau Dya Na Ghari",
                "artist": "Sukhwinder Singh",
                "url": "https://www.last.fm/music/Sukhwinder+Singh/_/Mala+Jau+Dya+Na+Ghari"
            },
            {
                "name": "Yed Lagli",
                "artist": "Ajay-Atul",
                "url": "https://www.last.fm/music/Ajay-Atul/_/Yed+Lagli"
            },
            {
                "name": "Boli Sakhare",
                "artist": "Vaishali Samant",
                "url": "https://www.last.fm/music/Vaishali+Samant/_/Boli+Sakhare"
            },
            {
                "name": "Tu Sukhay Dhoondh",
                "artist": "Avadhoot Gupte",
                "url": "https://www.last.fm/music/Avadhoot+Gupte/_/Tu+Sukhay+Dhoondh"
            },
            {
                "name": "Chandramukhi",
                "artist": "Ajay-Atul",
                "url": "https://www.last.fm/music/Ajay-Atul/_/Chandramukhi"
            },
            {
                "name": "Deewana Main Chala",
                "artist": "Makarand Anaspure",
                "url": "https://www.last.fm/music/Makarand+Anaspure/_/Deewana+Main+Chala"
            },
            {
                "name": "Yarala Yarala",
                "artist": "Sukhwinder Singh",
                "url": "https://www.last.fm/music/Sukhwinder+Singh/_/Yarala+Yarala"
            },
            {
                "name": "Sadhu Wanwa",
                "artist": "Ajay-Atul",
                "url": "https://www.last.fm/music/Ajay-Atul/_/Sadhu+Wanwa"
            },
            {
                "name": "Aatach Baya Ka Baara",
                "artist": "Sukhwinder Singh",
                "url": "https://www.last.fm/music/Sukhwinder+Singh/_/Aatach+Baya+Ka+Baara"
            },
        ],
        "90's": [
            {
                "name": "Tumhare Hawaale Watan Saathiyo",
                "artist": "Kishore Kumar",
                "url": "https://www.last.fm/music/Kishore+Kumar/_/Tumhare+Hawaale+Watan+Saathiyo"
            },
            {
                "name": "Chura Liya Hai Tumne Jo",
                "artist": "Asha Bhosle",
                "url": "https://www.last.fm/music/Asha+Bhosle/_/Chura+Liya+Hai+Tumne+Jo"
            },
            {
                "name": "Tujhe Dekha To",
                "artist": "Kumar Sanu",
                "url": "https://www.last.fm/music/Kumar+Sanu/_/Tujhe+Dekha+To"
            },
            {
                "name": "Dil Ke Paas",
                "artist": "Kumar Sanu",
                "url": "https://www.last.fm/music/Kumar+Sanu/_/Dil+Ke+Paas"
            },
            {
                "name": "Mera Joota Hai Japani",
                "artist": "Mukesh",
                "url": "https://www.last.fm/music/Mukesh/_/Mera+Joota+Hai+Japani"
            },
            {
                "name": "Mere Dard Ko Dard Se",
                "artist": "Kumar Sanu",
                "url": "https://www.last.fm/music/Kumar+Sanu/_/Mere+Dard+Ko+Dard+Se"
            },
            {
                "name": "Chura Liya Hai Tumne Jo",
                "artist": "Asha Bhosle",
                "url": "https://www.last.fm/music/Asha+Bhosle/_/Chura+Liya+Hai+Tumne+Jo"
            },
            {
                "name": "Ye sham mastani",
                "artist": "Kishore Kumar",
                "url": "https://www.last.fm/music/Kishore+Kumar/_/Ye+Sham+Mastani"
            },
            {
                "name": "Aankhon Ki Gustakhiyan",
                "artist": "Asha Bhosle",
                "url": "https://www.last.fm/music/Asha+Bhosle/_/Aankhon+Ki+Gustakhiyan"
            },
            {
                "name": "Mera Joota Hai Japani",
                "artist": "Mukesh",
                "url": "https://www.last.fm/music/Mukesh/_/Mera+Joota+Hai+Japani"
            },
        ],
         "hip-hop": [
        {
            "name": "Mockingbird",
            "artist": "Eminem",
            "url": "https://www.last.fm/music/Eminem/_/Mockingbird"
        },
        {
            "name": "Stan",
            "artist": "Eminem ft. Dido",
            "url": "https://www.last.fm/music/Eminem/_/Stan"
        },
        {
            "name": "Changes",
            "artist": "2Pac",
            "url": "https://www.last.fm/music/2Pac/_/Changes"
        },
        {
            "name": "Song Cry",
            "artist": "Jay-Z",
            "url": "https://www.last.fm/music/Jay-Z/_/Song+Cry"
        },
        {
            "name": "Keep Ya Head Up",
            "artist": "2Pac",
            "url": "https://www.last.fm/music/2Pac/_/Keep+Ya+Head+Up"
        },
        {
            "name": "Lose Yourself",
            "artist": "Eminem",
            "url": "https://www.last.fm/music/Eminem/_/Lose+Yourself"
        },
        {
            "name": "Creep",
            "artist": "TLC",
            "url": "https://www.last.fm/music/TLC/_/Creep"
        },
        {
            "name": "Everybody Hurts",
            "artist": "R.E.M.",
            "url": "https://www.last.fm/music/R.E.M./_/Everybody+Hurts"
        },
        {
            "name": "I'm Not the Only One",
            "artist": "Sam Smith",
            "url": "https://www.last.fm/music/Sam+Smith/_/I'm+Not+the+Only+One"
        },
        {
            "name": "Better Now",
            "artist": "Post Malone",
            "url": "https://www.last.fm/music/Post+Malone/_/Better+Now"
        }
    ]
    },
    "angry": {
        "bollywood": [
            {
                "name": "Jee Karda",
                "artist": "Ankit Tiwari",
                "url": "https://www.last.fm/music/Ankit+Tiwari/_/Jee+Karda"
            },
            {
                "name": "Duniya",
                "artist": "Gully Boy",
                "url": "https://www.last.fm/music/Gully+Boy/_/Duniya"
            },
            {
                "name": "Bachpan Ka Pyaar",
                "artist": "Badshah",
                "url": "https://www.last.fm/music/Badshah/_/Bachpan+Ka+Pyaar"
            },
            {
                "name": "Phir Se Ud Chala",
                "artist": "Mohit Chauhan",
                "url": "https://www.last.fm/music/Mohit+Chauhan/_/Phir+Se+Ud+Chala"
            },
            {
                "name": "Kya Mujhe Pyaar Hai",
                "artist": "KK",
                "url": "https://www.last.fm/music/KK/_/Kya+Mujhe+Pyaar+Hai"
            },
            {
                "name": "Ae Mere Humsafar",
                "artist": "Suman Kalyanpur",
                "url": "https://www.last.fm/music/Suman+Kalyanpur/_/Ae+Mere+Humsafar"
            },
            {
                "name": "Chura Liya Hai Tumne Jo",
                "artist": "Asha Bhosle",
                "url": "https://www.last.fm/music/Asha+Bhosle/_/Chura+Liya+Hai+Tumne+Jo"
            },
            {
                "name": "Dil Diyan Gallan",
                "artist": "Atif Aslam",
                "url": "https://www.last.fm/music/Atif+Aslam/_/Dil+Diyan+Gallan"
            },
            {
                "name": "Main Hoon Don",
                "artist": "Shankar Mahadevan",
                "url": "https://www.last.fm/music/Shankar+Mahadevan/_/Main+Hoon+Don"
            },
            {
                "name": "Bachpan Ka Pyaar",
                "artist": "Badshah",
                "url": "https://www.last.fm/music/Badshah/_/Bachpan+Ka+Pyaar"
            },
        ],
        "marathi": [
            {
                "name": "Vithu Mauli",
                "artist": "Ajay-Atul",
                "url": "https://www.last.fm/music/Ajay-Atul/_/Vithu+Mauli"
            },
            {
                "name": "Shivaji",
                "artist": "Ajay-Atul",
                "url": "https://www.last.fm/music/Ajay-Atul/_/Shivaji"
            },
            {
                "name": "Janta Raja",
                "artist": "Ajay-Atul",
                "url": "https://www.last.fm/music/Ajay-Atul/_/Janta+Raja"
            },
            {
                "name": "Kaal Bhairav",
                "artist": "Sukhwinder Singh",
                "url": "https://www.last.fm/music/Sukhwinder+Singh/_/Kaal+Bhairav"
            },
            {
                "name": "Swarajyachya Sathi",
                "artist": "Ajay-Atul",
                "url": "https://www.last.fm/music/Ajay-Atul/_/Swarajyachya+Sathi"
            },
            {
                "name": "Khel Mandala",
                "artist": "Ajay-Atul",
                "url": "https://www.last.fm/music/Ajay-Atul/_/Khel+Mandala"
            },
            {
                "name": "De Dhakka",
                "artist": "Ajay-Atul",
                "url": "https://www.last.fm/music/Ajay-Atul/_/De+Dhakka"
            },
            {
                "name": "Swarajya",
                "artist": "Ajay-Atul",
                "url": "https://www.last.fm/music/Ajay-Atul/_/Swarajya"
            },
            {
                "name": "Ghar Majhya Mandira",
                "artist": "Ajay-Atul",
                "url": "https://www.last.fm/music/Ajay-Atul/_/Ghar+Majhya+Mandira"
            },
            {
                "name": "Bajirao Mastani",
                "artist": "Ajay-Atul",
                "url": "https://www.last.fm/music/Ajay-Atul/_/Bajirao+Mastani"
            },
        ],
        "90's": [
            {
                "name": "Koi Kariye Na",
                "artist": "Kumar Sanu",
                "url": "https://www.last.fm/music/Kumar+Sanu/_/Koi+Kariye+Na"
            },
            {
                "name": "Aankhen Khuli Ho Ya",
                "artist": "Kumar Sanu",
                "url": "https://www.last.fm/music/Kumar+Sanu/_/Aankhen+Khuli+Ho+Ya"
            },
            {
                "name": "Rukh Jaa",
                "artist": "Kumar Sanu",
                "url": "https://www.last.fm/music/Kumar+Sanu/_/Rukh+Jaa"
            },
            {
                "name": "Dil Laga Liya Maine",
                "artist": "Udit Narayan",
                "url": "https://www.last.fm/music/Udit+Narayan/_/Dil+Laga+Liya+Maine"
            },
            {
                "name": "Mere Dard Ko Dard Se",
                "artist": "Kumar Sanu",
                "url": "https://www.last.fm/music/Kumar+Sanu/_/Mere+Dard+Ko+Dard+Se"
            },
            {
                "name": "Kabhi Kabhi Aditi",
                "artist": "A. R. Rahman",
                "url": "https://www.last.fm/music/A.+R.+Rahman/_/Kabhi+Kabhi+Aditi"
            },
            {
                "name": "Pehla Nasha",
                "artist": "Udit Narayan",
                "url": "https://www.last.fm/music/Udit+Narayan/_/Pehla+Nasha"
            },
            {
                "name": "Tujhe Dekha To",
                "artist": "Kumar Sanu",
                "url": "https://www.last.fm/music/Kumar+Sanu/_/Tujhe+Dekha+To"
            },
            {
                "name": "Dil Deewana",
                "artist": "Kumar Sanu",
                "url": "https://www.last.fm/music/Kumar+Sanu/_/Dil+Deewana"
            },
            {
                "name": "Tumse Milna",
                "artist": "Kumar Sanu",
                "url": "https://www.last.fm/music/Kumar+Sanu/_/Tumse+Milna"
            },
        ],
         "hip-hop": [
        {
            "name": "Killing in the Name",
            "artist": "Rage Against the Machine",
            "url": "https://www.last.fm/music/Rage+Against+the+Machine/_/Killing+in+the+Name"
        },
        {
            "name": "The Way I Am",
            "artist": "Eminem",
            "url": "https://www.last.fm/music/Eminem/_/The+Way+I+Am"
        },
        {
            "name": "Fight the Power",
            "artist": "Public Enemy",
            "url": "https://www.last.fm/music/Public+Enemy/_/Fight+the+Power"
        },
        {
            "name": "Break Stuff",
            "artist": "Limp Bizkit",
            "url": "https://www.last.fm/music/Limp+Bizkit/_/Break+Stuff"
        },
        {
            "name": "Take the Power Back",
            "artist": "Rage Against the Machine",
            "url": "https://www.last.fm/music/Rage+Against+the+Machine/_/Take+the+Power+Back"
        },
        {
            "name": "B.O.B",
            "artist": "OutKast",
            "url": "https://www.last.fm/music/OutKast/_/B.O.B"
        },
        {
            "name": "Chop Suey!",
            "artist": "System of a Down",
            "url": "https://www.last.fm/music/System+of+a+Down/_/Chop+Suey!"
        },
        {
            "name": "Survival of the Fittest",
            "artist": "Mobb Deep",
            "url": "https://www.last.fm/music/Mobb+Deep/_/Survival+of+the+Fittest"
        },
        {
            "name": "N.Y. State of Mind",
            "artist": "Nas",
            "url": "https://www.last.fm/music/Nas/_/N.Y.+State+of+Mind"
        },
        {
            "name": "Riot",
            "artist": "3OH!3",
            "url": "https://www.last.fm/music/3OH!3/_/Riot"
        }
    ]
    } ,
     "neutral": {
         "bollywood": [
        {
            "name": "Tum Hi Ho",
            "artist": "Arijit Singh",
            "url": "https://www.last.fm/music/Arijit+Singh/_/Tum+Hi+Ho"
        },
        {
            "name": "Kal Ho Naa Ho",
            "artist": "Sonu Nigam",
            "url": "https://www.last.fm/music/Sonu+Nigam/_/Kal+Ho+Naa+Ho"
        },
        {
            "name": "Tujh Mein Rab Dikhta Hai",
            "artist": "Roop Kumar Rathod",
            "url": "https://www.last.fm/music/Roop+Kumar+Rathod/_/Tujh+Mein+Rab+Dikhta+Hai"
        },
        {
            "name": "Agar Tum Saath Ho",
            "artist": "Alka Yagnik, Arijit Singh",
            "url": "https://www.last.fm/music/Alka+Yagnik/_/Agar+Tum+Saath+Ho"
        },
        {
            "name": "Raabta",
            "artist": "Arijit Singh",
            "url": "https://www.last.fm/music/Arijit+Singh/_/Raabta"
        },
        {
            "name": "Phir Le Aya Dil",
            "artist": "Arijit Singh",
            "url": "https://www.last.fm/music/Arijit+Singh/_/Phir+Le+Aya+Dil"
        },
        {
            "name": "Zara Zara",
            "artist": "Bombay Jayashree",
            "url": "https://www.last.fm/music/Bombay+Jayashree/_/Zara+Zara"
        },
        {
            "name": "Kabira",
            "artist": "Pritam",
            "url": "https://www.last.fm/music/Pritam/_/Kabira"
        },
        {
            "name": "Ae Dil Hai Mushkil",
            "artist": "Arijit Singh",
            "url": "https://www.last.fm/music/Arijit+Singh/_/Ae+Dil+Hai+Mushkil"
        },
        {
            "name": "Jeene Laga Hoon",
            "artist": "Atif Aslam",
            "url": "https://www.last.fm/music/Atif+Aslam/_/Jeene+Laga+Hoon"
        }
    ],
    "marathi": [
        {
            "name": "Mala Ved Lagale",
            "artist": "Ajay-Atul",
            "url": "https://www.last.fm/music/Ajay-Atul/_/Mala+Ved+Lagale"
        },
        {
            "name": "Sairat Zaala Ji",
            "artist": "Ajay-Atul",
            "url": "https://www.last.fm/music/Ajay-Atul/_/Sairat+Zaala+Ji"
        },
        {
            "name": "Jiv Rangala",
            "artist": "Ajay-Atul",
            "url": "https://www.last.fm/music/Ajay-Atul/_/Jiv+Rangala"
        },
        {
            "name": "Kadhi Tu",
            "artist": "Ajay Gogavale",
            "url": "https://www.last.fm/music/Ajay+Gogavale/_/Kadhi+Tu"
        },
        {
            "name": "Yaari Hai",
            "artist": "Ajay-Atul",
            "url": "https://www.last.fm/music/Ajay-Atul/_/Yaari+Hai"
        },
        {
            "name": "Deva Tujhya Gabharyala",
            "artist": "Swapnil Bandodkar",
            "url": "https://www.last.fm/music/Swapnil+Bandodkar/_/Deva+Tujhya+Gabharyala"
        },
        {
            "name": "Mann Udhan Varyache",
            "artist": "Shankar Mahadevan",
            "url": "https://www.last.fm/music/Shankar+Mahadevan/_/Mann+Udhan+Varyache"
        },
        {
            "name": "Gomu Sangtina",
            "artist": "Shankar Mahadevan",
            "url": "https://www.last.fm/music/Shankar+Mahadevan/_/Gomu+Sangtina"
        },
        {
            "name": "Tuzya Vina",
            "artist": "Avadhoot Gupte",
            "url": "https://www.last.fm/music/Avadhoot+Gupte/_/Tuzya+Vina"
        },
        {
            "name": "Kuni Yenar Ga",
            "artist": "Harshavardhan Wavare",
            "url": "https://www.last.fm/music/Harshavardhan+Wavare/_/Kuni+Yenar+Ga"
        }
    ],
    "90s": [
        {
            "name": "I Want It That Way",
            "artist": "Backstreet Boys",
            "url": "https://www.last.fm/music/Backstreet+Boys/_/I+Want+It+That+Way"
        },
        {
            "name": "Wonderwall",
            "artist": "Oasis",
            "url": "https://www.last.fm/music/Oasis/_/Wonderwall"
        },
        {
            "name": "Smells Like Teen Spirit",
            "artist": "Nirvana",
            "url": "https://www.last.fm/music/Nirvana/_/Smells+Like+Teen+Spirit"
        },
        {
            "name": "Torn",
            "artist": "Natalie Imbruglia",
            "url": "https://www.last.fm/music/Natalie+Imbruglia/_/Torn"
        },
        {
            "name": "My Heart Will Go On",
            "artist": "Celine Dion",
            "url": "https://www.last.fm/music/Celine+Dion/_/My+Heart+Will+Go+On"
        },
        {
            "name": "Wannabe",
            "artist": "Spice Girls",
            "url": "https://www.last.fm/music/Spice+Girls/_/Wannabe"
        },
        {
            "name": "No Scrubs",
            "artist": "TLC",
            "url": "https://www.last.fm/music/TLC/_/No+Scrubs"
        },
        {
            "name": "Losing My Religion",
            "artist": "R.E.M.",
            "url": "https://www.last.fm/music/R.E.M./_/Losing+My+Religion"
        },
        {
            "name": "I Will Always Love You",
            "artist": "Whitney Houston",
            "url": "https://www.last.fm/music/Whitney+Houston/_/I+Will+Always+Love+You"
        },
        {
            "name": "Baby One More Time",
            "artist": "Britney Spears",
            "url": "https://www.last.fm/music/Britney+Spears/_/...Baby+One+More+Time"
        }
    ],
    "hip_hop": [
        {
            "name": "God's Plan",
            "artist": "Drake",
            "url": "https://www.last.fm/music/Drake/_/God's+Plan"
        },
        {
            "name": "Sicko Mode",
            "artist": "Travis Scott",
            "url": "https://www.last.fm/music/Travis+Scott/_/Sicko+Mode"
        },
        {
            "name": "In Da Club",
            "artist": "50 Cent",
            "url": "https://www.last.fm/music/50+Cent/_/In+Da+Club"
        },
        {
            "name": "Hotline Bling",
            "artist": "Drake",
            "url": "https://www.last.fm/music/Drake/_/Hotline+Bling"
        },
        {
            "name": "Rockstar",
            "artist": "Post Malone ft. 21 Savage",
            "url": "https://www.last.fm/music/Post+Malone/_/Rockstar"
        },
        {
            "name": "Panda",
            "artist": "Desiigner",
            "url": "https://www.last.fm/music/Desiigner/_/Panda"
        },
        {
            "name": "No Role Modelz",
            "artist": "J. Cole",
            "url": "https://www.last.fm/music/J.+Cole/_/No+Role+Modelz"
        },
        {
            "name": "Money Trees",
            "artist": "Kendrick Lamar ft. Jay Rock",
            "url": "https://www.last.fm/music/Kendrick+Lamar/_/Money+Trees"
        },
        {
            "name": "Thrift Shop",
            "artist": "Macklemore & Ryan Lewis",
            "url": "https://www.last.fm/music/Macklemore+%26+Ryan+Lewis/_/Thrift+Shop"
        },
        {
            "name": "Low Life",
            "artist": "Future ft. The Weeknd",
            "url": "https://www.last.fm/music/Future/_/Low+Life"
        }
    ]

     }

}


def get_sentiment(messages):
    combined_message = " ".join(messages)
    sentiment_scores = analyzer.polarity_scores(combined_message)
    
    if sentiment_scores['compound'] >= 0.5:
        return "happy"
    elif sentiment_scores['compound'] <= -0.5:
        return "angry"
    elif -0.5 < sentiment_scores['compound'] < 0:
        return "sad"
    else:
        return "neutral"

def get_response(msg):
    global waiting_for_genre  

    if waiting_for_genre:  
        genre = msg.strip().lower()
        return get_music_response(genre)

    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    user_messages.append(msg)

    if len(user_messages) >= message_threshold:
        sentiment = get_sentiment(user_messages)
        user_messages.clear()  
        waiting_for_genre = True  
        return f"It seems you're feeling {sentiment}. Which genre of music would you like to hear?<br>Bollywood<br>Hip-hop<br>Marathi<br>90's"
        
        
    threshold = 0.50
    if prob.item() > threshold:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                response = random.choice(intent['responses'])
                return response
    
    return "I do not understand..."

def get_music_response(genre):
    if genre in music_details["happy"]:
        songs = music_details["happy"][genre]
        song_links = "".join(
            [f"<li><a href='{song['url']}' target='_blank'>{song['name']} by {song['artist']}</a></li>" for song in songs]
        )
        return f"<ul>{song_links}</ul>"  
    else:
        return "I don't have any songs for that genre. Please choose from Bollywood, Hip-hop, Marathi, or 90's."


@app.post('/predict')
def predict():
    user_message = request.json.get('message')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    response = get_response(user_message)
    return jsonify({"answer": response})

@app.route('/')
def home():
    return render_template('base.html')

if __name__ == "__main__":
    app.run(debug=True)
