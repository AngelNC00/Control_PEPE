# Control_PEPE
APLICACIÓN CLIENTE SERVIDOR PARA CONTROL Y  MONITOREO DE ROBOT INSTITUCIONAL


Durante el desarrollo del proyecto se explora la creación de un completo sistema cliente-servidor, que será la forma en que se pueda intervenir para el monitoreo y control de un robot con una aplicación remota.
Para esto, el robot se conecta a un servidor para que pueda ser controlado a través de una página web ejecutada desde un computador conectado a una red de área local.
Esta es una herramienta didáctica que permite al estudiante controlar un sistema real desde cualquier punto de conexión dentro de la red de área local.
En un equipo servidor se desarrolla un hardware de control que se ejecuta por medio de la implementación de Arduino y la comunicación de este con el usuario remoto a través de un protocolo llamado; “Firmata” utilizando el lenguaje JavaScript y Node.js. En el computador servidor usaremos express para crear un servidor web y Node.js como el entorno de ejecución, ya que esto nos permitirá el acceso para usar el robot de forma remota.

De esta forma se elimina la interacción directa que siempre ha existido entre el robot y su operario, ejecutando la aplicación por medio de una red de área local.
El robot utilizado en el proyecto ha sido creado por la Universidad Autónoma Metropolitana Unidad Iztapalapa, evitando así acudir a robots elaborados por terceras personas y, por consiguiente, corriéndose el riesgo de encontrar problemas de estrategias de control dado que es casi imposible llegar a modificar el algoritmo de programación con el que ya vienen programados.
![esquema_pepe](https://github.com/Navarrete00/Control_PEPE/assets/102823367/41f2abb4-b594-4299-80ff-8784e8821f37)
