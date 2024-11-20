import warnings
import pandas as pd
from joblib import load
import statistics
import re
from django.shortcuts import render, redirect, HttpResponse
# from django.http import HttpResponse
from django.contrib import messages, auth
from django.contrib.auth.models import User
from .models import veterinarian
from .models import feedback
from appoint.views import patientappo, docappo
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
# from website.model import keras_model
# Create your views here.


def home(request):
    return render(request, 'index.html', {})


# def loginn(request):
#     # if 'username' in request.session:
#     #     username = request.session['username']
#     #     return render(request, 'userprofile.html', {'username': username})
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)

#         if user is not None:
#             request.session['username'] = username
#             login(request, user)
#             return redirect(request, "userprofile", {'username': username})
#         else:
#             messages.error(request, "Inavlid User or Password")
#             return redirect(request, "login.html")

#     return render(request, "login.html", {})

def loginn(request):
    if 'vetusername' in request.session:
        messages.error(
            request, "Cannot Login as User When You Are Veterinarian")
        return redirect("home")
    if 'username' in request.session:
        if 'id' in request.session:
            username = request.session.get('username')
            return render(request, 'userprofile.html', {'username': username})
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['username'] = username
            user_id = request.user.id
            request.session['id'] = user_id
            # Redirect to userprofile view upon successful login
            return redirect('userprofile')
        else:
            messages.error(request, "Invalid User or Password")
            return redirect('login')  # Redirect to login view if login fails

    return render(request, "login.html", {})


def vetloginn(request):
    if 'username' in request.session:
        messages.error(
            request, "Cannot Login as Veterinarian When You Are User")
        return redirect("home")
    if 'vetusername' in request.session:
        if 'vet_id' in request.session:
            vetusername = request.session.get('vetusername')
            vet_id = request.session.get('vet_id')
            return render(request, 'vetprofile.html', {'vetusername': vetusername, 'vet_id': vet_id})
    if request.method == "POST":
        vetusername = request.POST['username']
        password = request.POST['password']
        try:
            user_check = veterinarian.objects.get(username=vetusername)
            if user_check is not None:
                if user_check.password == password:
                    vet_id = user_check.id
                    request.session['vetusername'] = vetusername
                    request.session['vet_id'] = vet_id
                    # messages.error(request, "user not found")
                    # if pass_check is None:
                    # messages.error(request, "Invalid Password")
                    # if user_check and pass_check is not None:
                    # if veterinarian.password == password:
                    # login(request, user_check)
                    return render(request, 'vetprofile.html', {'vetusername': vetusername, 'vet_id': vet_id})
                    # else:
                    # messages.error(request, "Invalid password")
                    # return redirect("vetlogin")
            else:
                messages.error(request, "Inavlid User and Password")
                return render(request, "vetlogin.html")
        except veterinarian.DoesNotExist:
            messages.error(request, "Invalid user")
            return render(request, "vetlogin.html")

    return render(request, "vetlogin.html", {})


def registerr(request):
    return render(request, "index.html", {})


# def signup(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']

#         myuser = User.objects.create_user(username, email, password)
#         myuser.save()

#         return redirect('login')
#     else:
#         messages.error(request, "Invalid")

#     return render(request, "index.html", {})

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        copassword=request.POST.get('copassword')

        if 'username' in request.session or 'vetusername' in request.session:
            messages.error(request, "Cannot Register when You are Logged in")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('signup')
        if password != copassword:
            messages.error(request, "Password and Confirm Password Doesnot Match")
            return redirect('signup')

        # Create a new user
        myuser = User.objects.create_user(username, email, password)
        myuser.save()

        messages.success(
            request, "Account created successfully. Please log in.")
        return redirect('login/')
    else:
        # Redirect to a proper page or render a specific template
        return render(request, "index.html", {})


# def userprofile(request):

#     # Retrieve username from session
#     username = request.session.get('username')
#     return render(request, 'userprofile.html', {'username': username})


def userprofile(request):

    if 'username' in request.session:
        if 'id' in request.session:
            username = request.session.get('username')
            user_id = request.session.get('id')
            if request.method == "POST":
                if 'feedback' in request.POST:
                    if feedback.objects.filter(user_id=user_id).exists():
                        star = request.POST['rating']
                        feed = request.POST['message']
                        feedobj = feedback.objects.get(user_id=user_id)
                        feedobj.feedback = feed
                        feedobj.rating = star
                        feedobj.save()
                        messages.success(
                            request, "Feedback submitted successfully")
                    else:
                        star = request.POST['rating']
                        feed = request.POST['message']
                        feedobj = feedback()
                        feedobj.user_id = user_id
                        feedobj.username = username
                        feedobj.feedback = feed
                        feedobj.rating = star
                        feedobj.save()
                        messages.success(
                            request, "Feedback submitted successfully")
                else:
                    messages.error(request, "Feedback Not submitted")

        return render(request, 'userprofile.html', {'username': username})
    else:
        return redirect('login/')


def vetprofile(request):

    if 'vetusername' in request.session and 'vet_id' in request.session:
        vetusername = request.session.get('vetusername')
        vet_id = request.session.get('vet_id')
        if request.method == "POST" and 'feed' in request.POST:
            star = request.POST.get('rating')
            feed = request.POST.get('message')
            # Get the veterinarian object
            if veterinarian.objects.filter(id=vet_id).exists():
                vet = veterinarian.objects.get(id=vet_id)
                # Update feedback and rating
                vet.feedback = feed
                vet.rating = star
                vet.save()
                messages.success(request, "Feedback submitted successfully")
            else:
                messages.error(request, "Veterinarian not found")

        return render(request, "vetprofile.html", {'vetusername': vetusername, 'vet_id': vet_id})
    else:
        return redirect('login/')

# -----------------------------------------------------------------------------------------------------


# Load pre-trained models
final_rf_model = load("./SymptomModels/final_rf_model.joblib")
final_nb_model = load("./SymptomModels/final_nb_model.joblib")
final_svm_model = load("./SymptomModels/final_svm_model.joblib")
data_dict = load("./SymptomModels/encoder.joblib")

# Load pre-trained LabelEncoder
encoder = load('./SymptomModels/encoder.joblib')
test_data = pd.read_csv("./SymptomModels/Testing.csv").dropna(axis=1)
# true_labels = test_data["diseases"].tolist()

X = test_data.iloc[:, :-1]

symptoms = X.columns.values

# Creating a symptom index dictionary to encode the
# input symptoms into numerical form
symptom_index = {}
for index, value in enumerate(symptoms):
    symptom = " ".join([i.capitalize() for i in value.split("_")])
    symptom_index[symptom] = index


# # Gives the Symptoms names
# print(symptom_index.keys())


data_dict = {
    "symptom_index": symptom_index,
    "predictions_classes": encoder.classes_
}


def predictDisease(symptoms):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")

        # symptoms = symptoms.split(",")

        # creating input data for the models
        input_data = [0] * len(data_dict["symptom_index"])
        for symptom in symptoms:
            index = data_dict["symptom_index"][symptom]
            input_data[index] = 1

        # reshaping the input data and converting it
        # into suitable format for model predictions
        input_data = np.array(input_data).reshape(1, -1)

        # generating individual outputs
        rf_prediction = data_dict["predictions_classes"][final_rf_model.predict(input_data)[
            0]]
        nb_prediction = data_dict["predictions_classes"][final_nb_model.predict(input_data)[
            0]]
        svm_prediction = data_dict["predictions_classes"][final_svm_model.predict(input_data)[
            0]]

        # making final prediction by taking mode of all predictions
        final_prediction = statistics.mode(
            [rf_prediction, nb_prediction, svm_prediction])

        predictions = {
            "rf_model_prediction": rf_prediction,
            "naive_bayes_prediction": nb_prediction,
            "svm_model_prediction": svm_prediction,
            "final_prediction": final_prediction
        }
    return predictions


def predict(request):
    if 'username' in request.session or 'vetusername' in request.session:

        if request.method == 'POST':
            selected_values = request.POST.getlist('symptoms')
            selected_values1 = selected_values
            user_symptoms = selected_values
            symptoms = selected_values
            if user_symptoms[0] == '':
                messages.error(request, "Please Enter your Symptoms")
                return redirect("predict")
            else:
                """ Calling the predicting disease function """
                predicted_disease = predictDisease(user_symptoms)

                value1 = predicted_disease['rf_model_prediction']
                value2 = predicted_disease['naive_bayes_prediction']
                value3 = predicted_disease['svm_model_prediction']
                value4 = predicted_disease['final_prediction']
                zoonoticv = "NO"

            zoonotic = ["Brucellosis", "Ehrlichiosis",
                        "Kennel_Cough", "Canine_Gastritis", "Rabies", "Canine_Gastroenteritis", "Leptospirosis"]
            if value4 in zoonotic:
                zoonoticv = "YES"

            return render(request, 'predict.html', {'feature_names': selected_values1, 'predict1': value1, 'predict2': value2, 'predict3': value3, 'finalpred': value4, 'zoonotic': zoonoticv})
        else:
            return render(request, "predict.html", {})
    else:
        return redirect('home')


# ---------------------------------------------------------------------------


def get_remedy_and_description(prediction):
    # Dictionary containing remedies and descriptions for each type of prediction
    remedies = {
        'bacterial_dermatosis': {
            'remedy': 'This type of infection may impact a dogs skin or upper respiratory tract, and can be treated using oral antibiotics such as cephalexin, erythromycin or clindamycin. Antibiotic ointments and shampoos can also work.Your vet may recommend coconut oil as part of a “skin supplement regime to strengthen the skin barrier and reduce itchiness or dry skin,”',
            'description': 'Some species of Staphylococcus bacteria are also normally present on the surface of the skin and do not cause a problem unless the skin is already damaged for another reason. Once the barriers in the skin are compromised, bacterial infections, also called pyoderma, can settle in.'
        },
        'flea_allergy': {
            'remedy': 'One home remedy for flea allergy in dogs is to create a homemade flea spray using natural ingredients. Mix together 1 cup of apple cider vinegar, 1 cup of water, 2 tablespoons of organic neem oil (optional but effective against fleas), 1 tablespoon of aloe vera gel (to soothe irritated skin), and 5 drops of lavender essential oil (which may repel fleas). Shake well and spray the solution onto your dogs coat, focusing on flea-prone areas like the neck, behind the ears, and along the back, while avoiding sensitive areas like the eyes and mouth. Additionally, maintain a clean environment by regularly vacuuming and washing bedding to reduce flea populations. If symptoms persist, consult a veterinarian for proper diagnosis and treatment.',
            'description': 'One of the most common illnesses associated with a flea infestation is flea allergy dermatitis (FAD) or flea bite hypersensitivity, which arises when a dog  immune system overreacts to the saliva injected by fleas during their bite. Itching, fur loss, and inflamed skin often follow.'
        },
        'fungal_infection': {
            'remedy': 'A home remedy for fungal infection in dogs involves using diluted apple cider vinegar as a topical solution. Mix equal parts of apple cider vinegar and water and apply it directly to the affected areas using a clean cloth or cotton ball. Apple cider vinegar has natural antifungal properties that can help alleviate fungal infections and soothe irritated skin. Additionally, ensure your dogs environment is clean and dry, as fungi thrive in moist conditions. Regular grooming and keeping your dogs coat clean can also help prevent fungal infections. If the infection persists or worsens, its important to consult a veterinarian for proper diagnosis and treatment',
            'description': 'Funguses (also called fungi) are parasitic, spore-producing organisms. They obtain their nourishment by absorbing food from the hosts on which they grow. Many species of fungus exist in the environment, but only a very few cause infections. The primary source of most infections is soil. Fungal infections can be acquired by inhalation, ingestion, or through the skin (for example, through a cut or wound).'
        },
        'hotspot': {
            'remedy': 'A home remedy for hotspots in dogs involves cleaning the affected area with a gentle antiseptic solution, such as diluted povidone-iodine or chlorhexidine. After cleaning, apply a soothing compress using a mixture of cool water and plain, unsweetened yogurt to help calm the inflammation and provide relief. Additionally, you can create a herbal tea rinse by steeping chamomile or calendula in hot water, allowing it to cool, and then applying it to the hotspot with a clean cloth. These natural remedies can help alleviate discomfort and promote healing, but if the hotspot persists or worsens, its essential to seek veterinary care for proper diagnosis and treatment.',
            'description': 'Hot spots on dogs, also known as moist dermatitis, are a painful condition where the skin becomes reddened, moist, and swollen, usually as a result of allergies, an infection, parasites, or moisture trapped within the coat. Other symptoms include licking, scratching, biting, and discharge of pus and fluids.'
        },
        'hypersensitivity_allergic_dermatosis': {
            'remedy': 'Allergic contact dermatitis is a rare hypersensitivity disorder in the dog. Clinical diagnosis is not easy. Primary lesions are transient. Secondary lesions caused by chronic inflammation and self-trauma are commonly present on typical areas, especially in sparsely haired regions and on the feet.',
            'description': 'One common home remedy for hypersensitivity allergic dermatosis in dogs is to give them oatmeal baths. Oatmeal has soothing properties that can help alleviate itching and irritation caused by allergies. To prepare an oatmeal bath, grind plain, unflavored oatmeal into a fine powder and mix it with warm water to create a paste. Then, gently massage the paste onto your dogs skin and let it sit for about 10-15 minutes before rinsing thoroughly with lukewarm water. This can provide temporary relief from itching and discomfort associated with allergic dermatitis. However, its important to consult with a veterinarian to determine the underlying cause of the allergy and to ensure the best course of treatment for your dogs specific condition.'
        },
        'mange': {
            'remedy': 'One effective home remedy for mange in dogs is a mixture of hydrogen peroxide and borax. Mix one part 3% hydrogen peroxide with two parts water and add borax powder until it no longer dissolves, creating a saturated solution. Apply this solution to the affected areas of your dogs skin using a clean cloth or sponge, making sure to avoid the eyes, nose, and mouth. Leave the solution on for about 10-15 minutes before rinsing thoroughly with warm water. Repeat this process every other day for a few weeks until the mange symptoms improve. However, its crucial to consult with a veterinarian before starting any home treatment to confirm the diagnosis and ensure the safety and effectiveness of the remedy for your dogs specific condition.',
            'description': 'Mange is a parasitic skin disease caused by microscopic mites. Two different mange mites cause this skin disease in dogs. One lives just under the surface of the skin, while the other resides in the hair follicles.'
        },
        'ringworm': {
            'remedy': 'A commonly recommended home remedy for ringworm in dogs is the application of diluted apple cider vinegar. Mix equal parts of apple cider vinegar and water, then soak a clean cloth or cotton ball in the mixture and gently dab it onto the affected areas of your dogs skin. Apple cider vinegar has antifungal properties that can help combat the fungus responsible for ringworm. Additionally, keeping the affected areas clean and dry is crucial to prevent the spread of the infection. However, its essential to consult with a veterinarian to confirm the diagnosis of ringworm and to ensure that the home remedy is appropriate for your dogs condition, as severe cases may require medical treatment.',
            'description': 'Ringworm isnt actually a worm, but a fungus that is similar to athletes foot. Dogs with ringworm suffer hair loss, usually in patches, with a crusty covering but lots of other skin conditions look very similar. Ringworm can be passed from your dog to you and other people who come into contact with your dog.'
        },
        # Add remedies and descriptions for other diseases
    }
    disease_info = remedies.get(prediction)
    print(prediction, remedies)

    if disease_info:
        remedy = disease_info.get('remedy', 'Remedy not found')
        description = disease_info.get('description', 'Description not found')
        return remedy, description
    else:
        return 'Remedy not found', 'Description not found'

    # return remedies.get(prediction, {}).get('remedy', 'Remedy not found'), remedies.get(prediction, {}).get('description', 'Description not found')


def skinpredict(request):
    if 'username' in request.session or 'vetusername' in request.session:

        final_string = None  # Initialize class_name
        confidence_score = None
        desc = None
        remedy = None
        string_without_space = None
        s = None

        if request.method == "POST" and request.FILES['skin']:

            imagetest = request.FILES['skin']
            # Disable scientific notation for clarity
            np.set_printoptions(suppress=True)
            # Load the model
            model = load_model("./savedModels/keras_model.h5", compile=False)

            # Load the labels
            class_names = open("./savedModels/labels.txt", "r").readlines()

            # Create the array of the right shape to feed into the keras model
            # The 'length' or number of images you can put into the array is
            # determined by the first position in the shape tuple, in this case 1
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

            # Replace this with the path to your image
            image = Image.open(imagetest).convert("RGB")

            # resizing the image to be at least 224x224 and then cropping from the center
            size = (224, 224)
            image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

            # turn the image into a numpy array
            image_array = np.asarray(image)

            # Normalize the image
            normalized_image_array = (
                image_array.astype(np.float32) / 127.5) - 1

            # Load the image into the array
            data[0] = normalized_image_array

            # Predicts the model
            prediction = model.predict(data)
            index = np.argmax(prediction)
            class_name = class_names[index]
            confidence_score = prediction[0][index]

            # Print prediction and confidence score
            print("Class:", class_name[2:], end="")
            print("Confidence Score:", confidence_score)

            # Remove numbers from the string
            string_without_numbers = re.sub(r'\d', '', class_name)

            string_without_space = string_without_numbers.replace(' ', '')

            # Replace underscores with spaces
            string_with_spaces = string_without_space.replace('_', ' ')

            s = str(class_name.split()[1])
            print(s, "dskjbsdg")

            # Ensure the string starts with a capital letter
            final_string = string_with_spaces.capitalize()
            remedy, desc = get_remedy_and_description(s)

        return render(request, "skinpredict.html", {'prediction': final_string, 'confidence_score': confidence_score, 'desc': desc, 'remedy': remedy})
    else:
        return redirect('home')


def docappo(request):

    return render(request, "docappo.html", {})


# -------------------------------------------------------
def sample(request):

    if 'username' or 'vetusername' in request.session:

        class_name = None  # Initialize class_name

        if request.method == "POST" and request.FILES['skin']:

            imagetest = request.FILES['skin']
            # Disable scientific notation for clarity
            np.set_printoptions(suppress=True)
            # Load the model
            model = load_model("./savedModels/keras_model.h5", compile=False)

            # Load the labels
            class_names = open("./savedModels/labels.txt", "r").readlines()

            # Create the array of the right shape to feed into the keras model
            # The 'length' or number of images you can put into the array is
            # determined by the first position in the shape tuple, in this case 1
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

            # Replace this with the path to your image
            image = Image.open(imagetest).convert("RGB")

            # resizing the image to be at least 224x224 and then cropping from the center
            size = (224, 224)
            image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

            # turn the image into a numpy array
            image_array = np.asarray(image)

            # Normalize the image
            normalized_image_array = (
                image_array.astype(np.float32) / 127.5) - 1

            # Load the image into the array
            data[0] = normalized_image_array

            # Predicts the model
            prediction = model.predict(data)
            index = np.argmax(prediction)
            class_name = class_names[index]
            confidence_score = prediction[0][index]

            # Print prediction and confidence score
            print("Class:", class_name[2:], end="")
            print("Confidence Score:", confidence_score)

        return render(request, "sample.html", {'prediction': class_name})
    else:
        return redirect('home')


def user_logout(request):
    # auth.logout(request)
    if "username" or "vetusername" in request.session:
        request.session.flush()
    return redirect('home')
