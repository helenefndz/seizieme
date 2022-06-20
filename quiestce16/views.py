from django.http import HttpResponse 
from django.template import loader
from .models import Mystere, Image, Indice
from .forms import Prop

import random

# from scripts import choisir a été réintégré ici

def index(request):
    
    template = loader.get_template('home.html')
    
    essais = request.session.get('essais', 0)
    nb_indices_demandés = request.session.get('nb_indices_demandés', 0)
    
    message = ""
    
    p = request.session.get('p', "")  #get(key, default=None)¶
    i = request.session.get('i', "")
    h = request.session.get('h', [])
    

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
            message = ecrire_message(essais, nb_indices_demandés)
            
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
            
            message = ecrire_message(essais, nb_indices_demandés)
            
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
                        
                        # message = "Il ne vous reste qu'une seule chance, plus possible de demander des indices."
                        # message = "Dernière chance ! essais = {}, nb_indices_demandés = {}, chemin post, réponse, 4 essais".format(essais, nb_indices_demandés)
                        
                        message = ecrire_message(essais, nb_indices_demandés)
                        
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
                    
                    message = "Non. " + ecrire_message(essais, nb_indices_demandés)
                    
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
        # choisir.run()
        
        # Mystere.objects.create(id=0)
    
        # i = Image.objects.all().first()
        # i = i.image
    
        # p = Mystere.objects.all().last()
        # p = p.individu
    
        # h = list(Indice.objects.values_list('indice_txt', flat=True))
        # random.shuffle(h)
    
        # p = request.session.get('p', p)
        # i = request.session.get('i', i)
        # h = request.session.get('h', h)
        
        request.session['essais'] = 0
        request.session['nb_indices_demandés'] = 0 #on sait jamais
        
        a_deviner = random.choice(Mystere.objects.all())

        p = a_deviner.individu

        i = a_deviner.image_set.get()
        i = i.image
        
        h = a_deviner.indice_set.get()
        h = [h.ind_p, h.ind_gpe, h.ind_dpt, h.ind_initiale]
        random.shuffle(h)

        request.session['p'] = p
        request.session['question'] = i
        request.session['h'] = h
        request.session['i'] = i
        
        # message = "C'est le début : encore {} essais et {} indices à demander.".format(5-essais, 4-nb_indices_demandés)
        # message = "p : {}, i : {}, h : {}.".format(p, i, h)
        message = ecrire_message(essais, nb_indices_demandés)
        
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
    '''fin : bravo ou raté. Deux arguments, request et res pour résolution'''
    
    # # if request.method == 'POST' and 'abandon' in request.POST:
    # #     return HttpResponse("Perdu ! C'était %s." % p)
    
    template = loader.get_template('verdict.html')
    
    # p = Mystere.objects.all().last()
    # p = p.individu

    # p = request.session.get('p', p)
    
    context = {'p':p,
               'res': res
               }
    
    return HttpResponse(template.render(context, request))
    # return HttpResponse("Perdu")
    
def ecrire_message(x, y): #essais, nb_indices_demandés
    '''Écriture du message affiché. Essais, nb d'indices demandés'''
    
    if x == 0:
        return "Début ! Il vous reste cinq essais et vous pouvez demander quatre indices."
    
    elif x == 4:
        return "Dernière chance ! Vous ne pouvez plus demander d'indices."
    
    else:
        
        msg1 = "Il vous reste {} essais ".format(5-x)
        
        if y == 3:
            msg2 = "et vous pouvez encore demander un indice."
        else:
            msg2 = "et vous pouvez encore demander {} indices.".format(4-y)
        
        return msg1 + msg2
    
