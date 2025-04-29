import html, random
import requests
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages



def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
        else:
            user = User.objects.create_user(username=username, password=password1)
            messages.success(request, "Account created successfully!")
            return redirect("login")

    return render(request, "register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("select_category")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def select_category(request):
    category_api = "https://opentdb.com/api_category.php"
    response = requests.get(category_api)


    categories = response.json().get('trivia_categories', [])

    if request.method == "POST":
        category = request.POST.get('category')
        difficulty = request.POST.get('difficulty')
        num_questions   = request.POST.get('num_questions')

        return redirect('quiz_page', category, difficulty, num_questions)

    return render(request, 'select_category.html', {'categories': categories})


@login_required(login_url="login")
def quiz_page(request, category_id, difficulty,num_questions ):
    """Fetch and display quiz questions on the web page"""
    api_url = "https://opentdb.com/api.php"
    params = {
        "amount": num_questions,
        "category": category_id,
        "difficulty": difficulty,
        "type": "multiple"
    }

    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        questions = response.json().get("results", [])

        for question in questions:
            # Decode HTML entities
            question["question"] = html.unescape(question["question"])
            question["correct_answer"] = html.unescape(question["correct_answer"])
            question["incorrect_answers"] = [html.unescape(ans) for ans in question["incorrect_answers"]]

            # Combine correct and incorrect answers, then shuffle
            options = question["incorrect_answers"] + [question["correct_answer"]]
            random.shuffle(options)

            # Store shuffled options in the question dictionary
            question["shuffled_options"] = options

        return render(request, "quiz.html", {"questions": questions,"num_questions": num_questions,
    "category_id": category_id,
    "difficulty": difficulty})
    
    return JsonResponse({"error": "Failed to fetch questions"}, status=500)


def check_answer(request):
    """Checks if submitted answers are correct"""

    if request.method == "POST":
        results = []

        num_questions = int(request.POST.get("num_questions"))
        # print("number qusetion" + num_questions)
        category_id = request.POST.get("category_id")
        difficulty = request.POST.get("difficulty")

        for i in range(1, num_questions + 1):
            question = request.POST.get(f"question_{i}")
            selected_answer = request.POST.get(f"selected_answer_{i}")
            correct_answer = request.POST.get(f"correct_answer_{i}")

            if question and selected_answer and correct_answer:
                is_correct = selected_answer == correct_answer
                results.append({
                    "question": question,
                    "selected_answer": selected_answer,
                    "correct_answer": correct_answer,
                    "is_correct": is_correct
                })

        score = sum(1 for r in results if r["is_correct"])
        print(score)

        return render(request, "result.html", {"results": results, "score":score,"total": num_questions})

    return JsonResponse({"error": "Invalid request"}, status=400)
