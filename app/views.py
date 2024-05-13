from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
import requests
import hashlib


def hashIt(senha):
    # Criptografando a senha
    senhaHash = hashlib.sha1(senha.encode())
    senhaDigest = str(senhaHash.hexdigest())
    return senhaDigest

def logMeIn(request):
    # Deve-se implementar autenticação JWT uma vez que não usamos models ou ORM.
    if request.method == "GET":
        return render(request, "index.html")
    else:
        # Capturamos os atributos de formulário
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        passwd = hashIt(senha)
        # Consultamos os dados de API
        r = "https://api-pi1-9lg0.onrender.com/logMeIn=%s/%s" % (email, passwd)

        # Consultando a API e transformando a resposta em um objeto pesquisável.
        j = requests.get(r).json()
        a = j['dados'][0]['Auth']

        if a == True:
            r = "https://api-pi1-9lg0.onrender.com/dados=%s" % (email)
            j = requests.get(r).json()

            ad = j['dados'][0]['ad']
            email = str(j['dados'][0]['email'])
            nome = str(j['dados'][0]['nome'])
            id = int(j['dados'][0]['id'])

            if ad is True:
                return render(request, "navigation_admin.html")
            else:
                response = render(request, "navigation_emp.html")
                response.set_cookie("id", id)
                response.set_cookie("nome", nome)
                response.set_cookie("email", email)
                response.set_cookie("ad", ad)
                cookies = request.COOKIES
                print(cookies)
                return response
        else:
            return render(request, "index.html")

def navigationEmp(request):
    if request.method == "GET":
        cookies = request.COOKIES
        print(cookies)
        return render(request, "navigation_emp.html")
    else:
        return HttpResponse("Não ha post neste site")
    
def navigationAdm(request):
    if request.method == "GET":
        return render(request, "navigation_admin.html")
    else:
        return HttpResponse("Não ha post neste site")
    
def clientes(request):
    
    idEmp = 1 # Isso deve ser armazenado em um cookie criptografado.

    if request.method == "GET":

        # Consultamos os dados de API
        r = "https://api-pi1-9lg0.onrender.com/tbCli=%s" % (idEmp)
        table_j = requests.get(r).json()
        
        return render(request, "clientes.html", {'table_j':table_j})
    else:
        if request.POST.get("btn") == "Enviar":
            #Capturando os dados de formulário
            nome = str(request.POST.get("nome"))
            email = str(request.POST.get("email"))
            tel = str(request.POST.get("telefone"))
            dt_nasc = str(request.POST.get("data_nascimento"))
            
            # Adequando a data com método built in'
            dt_mod = dt_nasc.split('-')
            dt_nasc = str(dt_mod[2]) + "-" + str(dt_mod[1]) + "-" + str(dt_mod[0]) 
            
            # Submetendo via API
            r = "https://api-pi1-9lg0.onrender.com/novoCli=%s/%s/%s/%s/%s" % (nome, email, dt_nasc, tel, 1)
            requests.post(r)

            #Repetir a consulta para atualizar a tabela
            r = "https://api-pi1-9lg0.onrender.com/tbCli=%s" % (idEmp)
            table_j = requests.get(r).json()

            #Importante, na hora de devolver passa junto o JSON para popular
            # as tabelas do HTML.
            return render(request, "clientes.html", {'table_j':table_j})
        
        else:
            # Uma atualização da página para os demais casos de post.
            r = "https://api-pi1-9lg0.onrender.com/tbCli=%s" % (idEmp)
            table_j = requests.get(r).json()
            return render(request, "clientes.html", {'table_j':table_j})
        
        # Implementar atualização PUT
        # Implementar deleção com o DELETE

def catalogo(request):
    idEmp = 1
    if request.method == "GET":
        r = "https://api-pi1-9lg0.onrender.com/tbServ=%s" % (idEmp)
        serv_j = requests.get(r).json()
        return render(request, "catserv.html", {'serv_j':serv_j})
    else:
        if request.POST.get("btn") == "Enviar":

            #Capturando os dados de formulário
            nome = str(request.POST.get("nome"))
            valor = request.POST.get("preco")

            # Submetendo via API
            # https://api-pi1-9lg0.onrender.com/novoServ=<desc>/<valor>/<id_emp>
            r = "https://api-pi1-9lg0.onrender.com/novoServ=%s/%s/%s" % (nome, valor, idEmp)
            requests.post(r)

            #Repetir a consulta para atualizar a tabela
            r = "https://api-pi1-9lg0.onrender.com/tbServ=%s" % (idEmp)
            serv_j = requests.get(r).json()

            return render(request, "catserv.html", {'serv_j':serv_j})
        else:
            #Repetir a consulta para atualizar a tabela
            r = "https://api-pi1-9lg0.onrender.com/tbServ=%s" % (idEmp)
            serv_j = requests.get(r).json()
            return render(request, "catserv.html", {'serv_j':serv_j})
        
        # Implementar precificação POST
        # Implementar atualização PUT
        # Implementar deleção com o DELETE

def agenda(request):
    if request.method == "GET":
        idEmp = 1
        r = "https://api-pi1-9lg0.onrender.com/tbAgenda=%s" % (idEmp)
        agenda_j = requests.get(r).json()

        return render(request, "agenda.html", {'agenda_j':agenda_j})
    else:
        if request.POST.get("1"):
            return render(request, "agenda.html")
        
def faturamento(request):
    if request.method == "GET":
        idEmp = 1
        r = "https://api-pi1-9lg0.onrender.com/historico=%s" % (idEmp)
        faturamento_j = requests.get(r).json()
        return render(request, "faturamento.html",{'faturamento_j':faturamento_j})
    else:
        if request.POST.get("1"):
            return render(request, "faturamento.html")
        
    