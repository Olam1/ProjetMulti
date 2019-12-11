
#Fonction qui récupère les points d'intensité à différents niveau de gris, entrés par l'utilisateur
#Retourne une liste de points avec leur valeur et opacité

def Do(MyWidget,AppName):
        p1={"value":0, "opacity":0.}
        p2={"value":0, "opacity":0.}
        p3={"value":0, "opacity":0.}
        wp=MyWidget.spinBox_white_point.value()
        bp=MyWidget.spinBox_black_point.value()
        if AppName.nb_points == 0:
            pass
        elif AppName.nb_points == 1:
            p1["value"]=MyWidget.point1spinBox.value()
            p1["opacity"]=MyWidget.point1Slider.value()/100
        elif AppName.nb_points == 2:  
            p1["value"]=MyWidget.point1spinBox.value()
            p1["opacity"]=MyWidget.point1Slider.value()/100
            p2["value"]=MyWidget.point2spinBox.value()
            p2["opacity"]=MyWidget.point2Slider.value()/100
        else:
            p1["value"]=MyWidget.point1spinBox.value()
            p1["opacity"]=MyWidget.point1Slider.value()/100
            p2["value"]=MyWidget.point2spinBox.value()
            p2["opacity"]=MyWidget.point2Slider.value()/100
            p3["value"]=MyWidget.point3spinBox.value()
            p3["opacity"]=MyWidget.point3Slider.value()/100
            
        result=[wp, bp, p1, p2, p3]
        return result