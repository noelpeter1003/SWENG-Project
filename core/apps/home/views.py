from django import template
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
import os
import json
import requests



@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def homePage(request):
    if "github" in request.POST:

        user_name = "noelpeter1003"
        token = os.getenv('GITHUB_TOKEN', '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')
        owner = "PradyumnBhardwaj"
        repo = "CSU33013-202122-SOFTWARE-ENGINEERING-PROJECT-"
        url1 = f"https://api.github.com/repos/{owner}/{repo}"

        def get_response(get_url):
                url = url1 + get_url
                response = requests.get(url)
                list = response.json()
                return list

        def get_commits():
            list = get_response("/commits")
            with open('apps/static/assets/json/commits.json', 'w', encoding='utf-8') as f:
                json.dump(list, f, ensure_ascii=False, indent=4)

        def get_total_commits(src):
            commits_per_user = {}
            with open(src,'r') as file:
                data = json.load(file)
                commit_list = [x['commit'] for x in data]
                author_list = [x['author'] for x in commit_list]
                user_list = [x['name'] for x in author_list]
                for name in user_list:
                    if name in commits_per_user:
                        commits_per_user[name] += 1
                    else:
                        commits_per_user.update({name: 1})
            names = commits_per_user.keys()
            number_of_commits = commits_per_user.values()
            user_list = []
            commits_list = []
            for x in names:
                user_list.append(x)
            for x in number_of_commits:
                commits_list.append(x)
            result = {"users":user_list, "data":commits_list}
            if(os.path.exists(src)):
                os.remove(src)
            with open(src, 'w') as file:
                json.dump(result, file, indent = 4)   

        def scripts():
            list = get_response("/languages")
            with open('apps/static/assets/json/scripts.json', 'w', encoding='utf-8') as f:
                json.dump(list, f, ensure_ascii=False, indent=4)
            
        def get_scripts(src):
            with open(src,'r') as file:
                data = json.load(file)
            script = data.keys()
            total_code = list(data.values())
            scripts = []
            for x in script:
                scripts.append(x)
            percentages = []
            for i in range(len(total_code)):
                code_percentage = (total_code[i]/sum(total_code))*100
                percentages.append(code_percentage)
            result = {"scripts":scripts, "percentage":percentages}
            if(os.path.exists(src)):
                os.remove(src)
            with open(src, 'w') as file:
                json.dump(result, file, indent = 4)

        def main():
            scripts()
            print("hello")
            get_scripts('apps/static/assets/json/scripts.json')
            get_commits()
            get_total_commits('apps/static/assets/json/commits.json')
        main()
        return HttpResponseRedirect(reverse("home"))
    return render(request,"home/home.html")


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
