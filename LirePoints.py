
#Fonction qui eçoit un objet de type "InterfaceGraphique" en paramètre
#Récupère les points d'intensité à différents niveau de gris, entrés par l'utilisateur
#Retourne une liste de points avec leur valeur et opacité

def Do(MonInterface):
        p1={"value":0, "opacity":0.}
        p2={"value":0, "opacity":0.}
        p3={"value":0, "opacity":0.}
        wp=MonInterface.spinBox_white_point.value()
        bp=MonInterface.spinBox_black_point.value()
        if MonInterface.nb_points == 0:
            pass
        elif MonInterface.nb_points == 1:
            p1["value"]=MonInterface.point1spinBox.value()
            p1["opacity"]=MonInterface.point1Slider.value()/100
        elif MonInterface.nb_points == 2:  
            p1["value"]=MonInterface.point1spinBox.value()
            p1["opacity"]=MonInterface.point1Slider.value()/100
            p2["value"]=MonInterface.point2spinBox.value()
            p2["opacity"]=MonInterface.point2Slider.value()/100
        else:
            p1["value"]=MonInterface.point1spinBox.value()
            p1["opacity"]=MonInterface.point1Slider.value()/100
            p2["value"]=MonInterface.point2spinBox.value()
            p2["opacity"]=MonInterface.point2Slider.value()/100
            p3["value"]=MonInterface.point3spinBox.value()
            p3["opacity"]=MonInterface.point3Slider.value()/100
            
        result=[wp, bp, p1, p2, p3]
        return result