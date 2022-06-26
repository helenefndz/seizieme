from django.http import HttpResponse 
from django.template import loader
from .models import Mystere, Image, Indice
from .forms import Prop

import random

from fuzzywuzzy import fuzz

# from scripts import choisir a été réintégré ici

def index(request):
    
    template = loader.get_template('home.html')
    
    essais = request.session.get('essais', 0)
    nb_indices_demandés = request.session.get('nb_indices_demandés', 0)
    
    message = ""
    
    p = request.session.get('p', "")  #get(key, default=None)¶
    i = request.session.get('i', "")
    h = request.session.get('h', [])
    n = request.session.get('n', "")
    

    if request.method == 'POST' and 'abandon' in request.POST:
        # return HttpResponse("Perdu ! C'était %s." % p)
        res = False
        request.session['essais'] = 0
        request.session['nb_indices_demandés'] = 0
        
        
        return verdict(request, p, res)
        # return HttpResponse(res)
        
    
        
    elif request.method == 'POST' and 'indice' in request.POST:
        # nb_indices_demandés = request.session.get('nb_indices_demandés', 0)
        nb_indices_demandés += 1
        request.session['nb_indices_demandés'] = nb_indices_demandés
        
        essais += 1
        request.session['essais'] = essais
        
        if essais == 4 or nb_indices_demandés > 4: #dernière chance

            h = h[0:nb_indices_demandés]
            
            # message = "Il ne vous reste qu'une seule chance, plus possible de demander des indices."
            proximite = ""
            message = ecrire_message(essais, nb_indices_demandés, proximite)
            
            context = {'question': i,
                        'rep': Prop(),
                        'nb_indices_demandés': nb_indices_demandés,
                        'h': h,
                        'p': p,
                        'essais': essais,
                        'message': message,
                        }
            
            return HttpResponse(template.render(context, request))
        
        
        else:
            proximite = ""
            message = ecrire_message(essais, nb_indices_demandés, proximite)
            
            # message = "Encore {} essais, {} indices.".format(5-essais, 4-nb_indices_demandés)
            
            h = h[0:nb_indices_demandés]
            
            context = {'question': i,
                        'rep': Prop(),
                        'nb_indices_demandés': nb_indices_demandés,
                        'h': h,
                        'p': p,
                        'essais': essais,
                        'message': message,
                        }
            
            # return(HttpResponse(h))
            return HttpResponse(template.render(context, request))
        
    elif request.method == 'POST' and 'reponse' in request.POST:
        rep = Prop(request.POST)
            
        if rep.is_valid():
            rep=rep.cleaned_data['prop']
            
            if rep == p:
                # return HttpResponse("eh ouais")
                res=True
                request.session['essais'] = 0
                request.session['nb_indices_demandés'] = 0
                return verdict(request, p, res)
                
            else:
                essais += 1        
                
                
                if essais == 5:
                    
                    res=False
                    request.session['essais'] = 0
                    request.session['nb_indices_demandés'] = 0
                    return verdict(request, p, res)
                    
                
                elif essais == 4 or nb_indices_demandés > 4: #dernière chance
                        request.session['essais'] = essais
                        h = h[0:nb_indices_demandés]
                        
                        proximite = proche_loin(rep, p)
						
						# message = "Il ne vous reste qu'une seule chance, plus possible de demander des indices."
                        # message = "Dernière chance ! essais = {}, nb_indices_demandés = {}, chemin post, réponse, 4 essais".format(essais, nb_indices_demandés)
                        
                        message = ecrire_message(essais, nb_indices_demandés, proximite)
                        
                        context = {'question': i,
                                    'rep': Prop(),
                                    'nb_indices_demandés': nb_indices_demandés,
                                    'h': h,
                                    'p': p,
                                    'essais': essais,
                                    'message': message,
                                    }
                        
                        return HttpResponse(template.render(context, request))# p = request.session.get('p', p)
                    # i = request.session.get('i', i)
                    # h = request.session.get('h', h)
                    
                    # return HttpResponse("Non. Encore {} essais, p : {}, i : {}, h : {}, rep = {}, {}.".format(5-essais, p, i, h, rep, rep == p))
                    
                    
                else:
                    request.session['essais'] = essais
                    # message = "Non. Encore {} essais, p : {}, i : {}, h : {}, rep = {}, {}.".format(5-essais, p, i, h, rep, rep == p)
                    
                    
                    
                    # template = loader.get_template('home.html')
                    
                    h = h[0:nb_indices_demandés]
                    
                    proximite = proche_loin(rep, p)
                    
                    message = "Non. " + ecrire_message(essais, nb_indices_demandés, proximite)
                   
                    
                    context = {'question': i,
                                'rep': Prop(),
                                'nb_indices_demandés': nb_indices_demandés,
                                'h': h,
                                'p': p,
                                'i': i,
                                'essais': essais,
                                'message': message,
                                }
                    
                    return HttpResponse(template.render(context, request))
                    # return HttpResponse(message)

    elif essais == 0:
        
        
        request.session['essais'] = 0
        request.session['nb_indices_demandés'] = 0 #on sait jamais
        
        a_deviner = random.choice(Mystere.objects.all())

        p = a_deviner.individu

        i = a_deviner.image_set.get()
        i = i.image
        
        n = a_deviner.nuance_set.get()
        n = n.nuance
        
        h = a_deviner.indice_set.get()
        h = [h.ind_p, h.ind_sortant, h.ind_dpt, h.ind_initiale]
        random.shuffle(h)

        request.session['p'] = p 
        request.session['question'] = i
        request.session['h'] = h
        request.session['i'] = i
        
        request.session['n'] = n
        
        
        # message = "C'est le début : encore {} essais et {} indices à demander.".format(5-essais, 4-nb_indices_demandés)
        # message = "p : {}, i : {}, h : {}.".format(p, i, h)
        proximite = ""
        message = ecrire_message(essais, nb_indices_demandés, proximite)
        
        
        
        context = {'question': i,
                   'rep': Prop(),
                   'nb_indices_demandés': nb_indices_demandés,
                   'h': h,
                   'p': p,
                   
                   'essais': essais,
                   'message': message,
                   }
        
    
        return HttpResponse(template.render(context, request))
        # return HttpResponse(p)
    
                
    else:
        res = False
        request.session['essais'] = 0
        request.session['nb_indices_demandés'] = 0
        
        
        return verdict(request, p, res)
        # return HttpResponse(res)
          
        
def verdict(request, p, res):
    '''fin : bravo ou raté. Deux arguments, request et res pour résolution
        On alimente aussi la session : nombre de parties jouées, nombre de réussites
    '''
     
    nb_jeu = request.session.get('nb_jeu', 0)
    yes = request.session.get('yes', 0)
     
    nb_jeu += 1
     
    if res == True:
         yes += 1
     
    request.session['nb_jeu'] = nb_jeu
    request.session['yes'] = yes

    # # if request.method == 'POST' and 'abandon' in request.POST:
    # #     return HttpResponse("Perdu ! C'était %s." % p)
    recap = "Vous avez joué {} fois, avec {:.2f} % de réussite.".format(nb_jeu, yes/nb_jeu*100)
    
    i = request.session.get('i', "")
    n = request.session.get('n', "")
    
	
    template = loader.get_template('verdict.html')
    
    # p = Mystere.objects.all().last()
    # p = p.individu

    # p = request.session.get('p', p)
    
    context = {'p':p,
               'res': res,
               'recap': recap,
               'question': i,
               'n': n
               }
    
    return HttpResponse(template.render(context, request))
    # return HttpResponse("Perdu")
    
def ecrire_message(x, y, z): #essais, nb_indices_demandés
    '''Écriture du message affiché. Essais, indices demandés
	Proximité : Levenshtein calculé par fuzzywuzzy (df proche_loin)
    '''
    
    if x == 0:
        m_fin = "Début ! Il vous reste cinq essais et vous pouvez demander quatre indices."
    
    elif x == 4:
        m_fin =  "Dernière chance ! Vous ne pouvez plus demander d'indices."
    
    else:
        
        m_fin1 = "Il vous reste {} essais ".format(5-x)
        
        if y == 3:
            m_fin2 =  "et vous pouvez encore demander un indice."
        else:
            m_fin2 =  "et vous pouvez encore demander {} indices.".format(4-y)
            
        m_fin = m_fin1 + m_fin2
        
    message = z + "<br>" + m_fin
    
    return message

def proche_loin(rep, p):
    ratio = fuzz.partial_ratio(rep, p)
    if ratio >= 85:
        proximite = "Mais vous êtes vraiment très proche ! (Juste une erreur d'orthographe peut-être ?)"
    elif ratio >= 70:
        proximite = "Vous êtes proche."
    else:
        proximite = ""
    return proximite

    
