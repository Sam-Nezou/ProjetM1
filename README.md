# Projet M1:
### Réalisation d'une interface homme machine pour communiquer avec une carte arduino

__1. Librairie à installer__

* _matplotlib_
        
        python -m pip install -U matplotlib
    ou
    
        sudo apt-get install python3-matplotlib
    ou
    
        python -m pip install -U matplotlib


    ---
* _PyQt5_

        pip3 install pyqt5

    ---
* _pyserial_

        python -m pip install pyserial
    ou
    
        pip install pyserial
  
  
        
__2. Fichier de configuration__

Le fichier de configuration [config.py](https://github.com/Sam-Nezou/ProjetM1/blob/main/config.py) permet de configurer le port USB connecté à la carte.

* Sous Windows (exemple)

        portUsb ='COM5' 

* Sous Linux (exemple)

        portUsb ='/dev/ttyACM0'
> Le dernier chiffre est à changer en fonction du port USB


__3. Utilisation__

* Programme ne se lance qu'une fois le port USB branché.
* Si l'appliction ne se lance pas bien vérifier le numéro du port.



__4. Bibliograpie__

Le travail de [pearsonkyle](https://github.com/pearsonkyle) nous a servi de base pour la communication entre le PC et la carte Arduino. 
Le lien de son travail [ici](https://github.com/pearsonkyle/pyduino_webapi)
