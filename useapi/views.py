from decouple import config
import markdown
from django.shortcuts import render,redirect
from django.http import HttpResponse
import openai
from .forms import QuestionForm
from .models import Question

openai.api_key = config("SECRET_KEY")

# HEALTH_KEYWORDS = ["health", "medicine", "doctor", "symptom", "hospital", "treatment"]

def is_health_related(word):
    messages = [
                {"role": "system", "content": "You are a helpful assistant."},
            ]
    if word:
        messages.append({"role":"user","content":"Is '" +word+"' health related ? Reply in yes or no"},)
        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
    answer = chat_completion.choices[0].message.content[0]
    
    
    return answer=='Y'

def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data['question_text']
            print(question_text)
            if is_health_related(question_text):
                messages = [
                    {"role": "system", "content": "You are a helpful assistant."},
                ]
                if question_text:
                    messages.append({"role":"user","content":question_text},)

                    chat_completion = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo", messages=messages
                    )
                answer = chat_completion.choices[0].message.content
                print(answer)
                # Create a new Question object and save it to the database
                question = form.save(commit=False)
                question.answer_text = answer
                question.save()
                
                
                # Pass the answer to the template context
                form = QuestionForm()
            else:
                error_message = "Please enter a health-related question."
                return render(request,"useapi/index.html",{"form":form,"error_message":error_message})
            #markdown.markdown(answer)
            context = {'question': question, 'answer': markdown.markdown(answer),'form':form}
            return render(request, 'useapi/index.html', context)

    else:
        form = QuestionForm()    
    return render(request,'useapi/index.html',{'form':form})