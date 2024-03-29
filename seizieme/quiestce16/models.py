from django.db import models


class Mystere(models.Model):
    
    individu = models.CharField(max_length=100, default="")
    
    def __str__(self):
        return self.individu
#recommandé par le tuto django sur le site de la doc



class Nuance(models.Model):
    
    numero = models.ForeignKey(Mystere, on_delete=models.CASCADE, default=0)
    nuance = models.CharField(max_length=100, default="")
    
    def __str__(self):
        return self.nuance

class Image(models.Model):
    
    numero = models.ForeignKey(Mystere, on_delete=models.CASCADE, default=0)
    image = models.URLField(max_length=255, default="")
    
    def __str__(self):
        return self.image

# class Indice(models.Model):
#     numero = models.ForeignKey(Mystere, on_delete=models.CASCADE, default=0)
#     # indice_txt = models.CharField(max_length=255, default="")
#     ind_p = models.CharField(max_length=255, default="")
#     ind_gpe = models.CharField(max_length=255, default="")
#     ind_dpt = models.CharField(max_length=255, default="")
#     ind_initiale = models.CharField(max_length=255, default="")
    
#     def __str__(self):
#         return "[%s, %s, %s, %s]" % (self.ind_p, self.ind_gpe, self.ind_dpt, self.ind_initiale)


class Indice(models.Model):
    numero = models.ForeignKey(Mystere, on_delete=models.CASCADE, default=0)
    ind_p = models.CharField(max_length=255, default="")
    ind_dpt = models.CharField(max_length=255, default="")
    ind_initiale = models.CharField(max_length=255, default="")
    ind_sortant = models.CharField(max_length=255, default="")
    ind_groupe = models.CharField(max_length=255, default="")
    ind_commission = models.CharField(max_length=255, default="")
    
    def __str__(self):
            return "[%s, %s, %s, %s, %s, %s]" % (self.ind_p,
                                             self.ind_sortant,
                                             self.ind_dpt,
                                             self.ind_initiale,
                                             self.ind_groupe,
                                             self.ind_commission
                                             )
