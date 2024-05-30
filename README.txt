En el proyecto aquí presente, tiene como objetivo crear una base de datos relacional en MySQL
el cual albergará los casos de contagio desagregados por su información de sucesos e información poblacional,

para lo cual el primer paso es la creación de la base de datos con la herramienta MySQL
allí se ejecutará el escript CREACIÓN_DB, validando que se encuentra conectado adecuadamente al servidor, debe ejecutarse.

Posteriormente se abrirá el script de python, preferiblemente con pycharm, es necesario contar con los programas necesarios para su uso.
Debe ejecutarse este script, el cual ya identifica que librerías requiere y las instalará si es necesario,
luego se abrirá una venatana emergente que solicita el dato del nombre de usuario este depende de la configuración en MySQL,
por lo general este será "root"
acto seguido, la ventana pedirá la contraseña para acceder al servidor
por último aparece una ventana de confirmación, si está todo bien solo se debe dar aceptar.

Tardará unos minutos en leer la información del archivo CSV e insertandolo en la Base de datos llamada CASOS_CSV.

NOTA: se hizo una pequeña corrección en los encabezados del CSV, dado que estaba trucado la información de departamento con Municipios, esto ya que se asume que un desarrollo tiene como finalidad prolongarse en el timepo, y que desde el origen posteriomente la información vendrá bien, de lo contrario debería ajustarse el script.

AUTOR: NICOLAS GOMEZ LOZANO
