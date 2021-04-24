# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
from gluon.globals import Request


def index():
     #response.flash = T("Hello World")
     return dict(message=T('Welcome to web2py!'))

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

def comercio():
    #response.flash = T("Hello World")
    form_comercio= SQLFORM(db.comercio,
                            labels ={'name':'Nombre','direccion':'Dirección',
                                    'fk_municipio':'Municipio'})
        
    #LO QUE SIGUE INCLUYENDO LA FUNCION def makers() sirve para elegir muncipios acorde al departamento
    #elegido y su posterior inserción en la base de datos.
    if request.vars.maker_name:

        #lists = db(db.Product.Maker_ID==request.vars.maker_name).select(db.Product.ALL)
        #themakers = db(db.Maker.id==request.vars.maker_name).select(db.Maker.ALL)
        municipios = db(db.municipio.id==request.vars.maker_name).select(db.municipio.ALL)
        comercio_name = request.vars.get("nom_comercio")
        comercio_direccion = request.vars.get("dir_comercio")
        comercio_municipio = request.vars.get("maker_name")
        response.flash = 'formulario aceptado'
        
        insert_comercio = db.comercio.validate_and_insert(name=comercio_name, direccion=comercio_direccion, fk_municipio=comercio_municipio)      
        
        return redirect(URL('queja', vars=dict(comercio_name=comercio_name)))

    else:
        #lists = db(db.Product.Maker_ID==1).select(db.Product.ALL)
        #themakers = db(db.Maker.id==1).select(db.Maker.ALL)
        municipios = db(db.municipio.id==1).select(db.municipio.ALL)

    departamentos = db().select(db.departamento.ALL)
    

    if request.vars.category_name:
        #makers = db(db.Maker.Category_ID==request.vars.category_name).select(db.Maker.ALL)
       makers = db(db.municipio.fk_departamento==request.vars.category_name).select(db.municipio.ALL)
    else:
        makers = db(db.municipio.fk_departamento==1).select(db.municipio.ALL)
    #return dict(lists=lists, categories=departamentos, makers=makers, themakers=municipios)
    return dict(form=form_comercio, categories=departamentos,themakers=municipios, makers=makers)
    

def maker():
    makers = db(db.municipio.fk_departamento==request.vars.category_name).select(db.municipio.ALL)
    result = "<select name='maker_name'>"
    for maker in makers:
        result += "<option value='" + str(maker.id) + "'>" + maker.name + "</option>"  
    result += "</select>"
    return XML(result)

def queja():
    comercio_name = request.vars['comercio_name'] 
    comer= db(db.comercio.name==comercio_name).select().first() 
    
    form_queja= SQLFORM(db.queja,
                            labels ={'fecha':'Fecha','contenido':'Queja',
                                    'peticion':'Petición','fk_comercio':'Comercio'})
    if form_queja.process().accepted:
       response.flash = 'SU QUEJA HA SIDO REGISTRADA GRACIAS'
       return redirect(URL('default', 'confirmacion'))
    elif form_queja.errors:
       response.flash = 'El formulario tiene errores'
    else:
       response.flash = 'Por favor complete el formulario'
      
    #form_comercio = SQLFORM.grid(db.comercio, fields=[db.comercio.name, db.comercio.direccion],
    #                              headers={'name': 'Nombre Comercio', 'direccion': 'Dirección'}, csv=False)
    return dict(form=form_queja)

def estadistica():
    formulario=''
    return dict(message=T('Estadísticas!'), form=formulario)

def norte():
    msg = "def norte"
    consulta = db(db.queja).select().first()
    #ESTE NO ESTÁ EN USO LO DEJO PARA CONSULTAS /Devuelve las quejas correspondientes a los
    #comercios de la region norte que tuvieron quejas el ultimo año
    # row = db(
    #         (db.queja.fk_comercio==db.comercio.id)&
    #         (db.comercio.fk_municipio==db.municipio.id)&
    #         (db.municipio.fk_departamento==db.departamento.id)&
    #         (db.departamento.fk_region==db.region.id)&
    #         (db.region.name=='NORTE')&
    #         (db.queja.fecha >='2021-01-01 00:00:00')
    #         ).select(
    #             db.queja.fecha, 
    #             db.comercio.name,
    #             orderby=~db.queja.fecha
    #         )
    #Esta es una condición de web2py para hacer el conteo. después se coloca dentro del select.
    count = db.queja.id.count()

    row_count = db(
            (db.queja.fk_comercio==db.comercio.id)&
            (db.comercio.fk_municipio==db.municipio.id)&
            (db.municipio.fk_departamento==db.departamento.id)&
            (db.departamento.fk_region==db.region.id)&
            (db.region.name=='NORTE')&
            (db.queja.fecha >='2021-01-01 00:00:00')
            ).select(
                db.comercio.name,
                count,
                groupby = db.comercio.name,
                orderby= ~db.queja.fecha,
            )
    
    #Del query que obtiene la agrupación y conteo de quejas por comercio, se crean dos 
    #una para labels y otra para data.
    #COMO EL ROW DEVUELVE UN CAMPO '_extra': '{COUNT("queja"."id")'} se hizo _extra[count]  count = a la consulta
    #que regresa el conteo que en este caso es queja.id por eso se sustituye alli.
    #https://www.pythonstudio.us/web2py/grouping-and-counting.html
    labels=[]
    data=[]    
    for line in row_count:
        labels.append(line.comercio.name)
        data.append(line._extra[count])
        
                 
    #*******EMPIEZA SQLFORM.grid personalizado ***************
    #Query para mostrar en el SQLFORM.grid No utiliza select porque así lo pide SQLFORM.grid
    elquery = (( (db.queja.fk_comercio==db.comercio.id)&
            (db.comercio.fk_municipio==db.municipio.id)&
            (db.municipio.fk_departamento==db.departamento.id)&
            (db.departamento.fk_region==db.region.id)&
            (db.region.name=='NORTE')&
            (db.queja.fecha >='2021-01-01 00:00:00')
              ))
    
    fields = (db.queja.fecha, db.queja.fk_comercio, db.queja.contenido)
   
    grid = SQLFORM.grid(query=elquery, fields=fields, csv=False, deletable=True,  searchable=True)
     #*******FINALIZA SQLFORM.grid personalizado ***************
    
    return dict(mygrid=grid, labels=labels, data=data, mensaje = msg)

def sur():
    msg = "def sur"

    #Conteo de quejas de los comercios de la region sur del año 2021
    # ******** Aquí empieza la consulta ********   
    count = db.queja.id.count()

    row_sur = db(
            (db.queja.fk_comercio==db.comercio.id)&
            (db.comercio.fk_municipio==db.municipio.id)&
            (db.municipio.fk_departamento==db.departamento.id)&
            (db.departamento.fk_region==db.region.id)&
            (db.region.name=='SUR')&
            (db.queja.fecha >='2021-01-01 00:00:00')            
            ).select(
                db.comercio.name,
                count,
                groupby = db.comercio.name,
                orderby= ~db.queja.fecha,
            )
    # **********Finaliza consulta **********************
    
    #EN def norte() arriba está comentado bastante de esta función / ingresamos el nombre del comercio en labels[] 
    # y la cantidad de veces que se ha colocado una queja   data[]
    labels=[]
    data=[]    
    for line in row_sur:
        labels.append(line.comercio.name)
        data.append(line._extra[count])
        
                 
    #*******EMPIEZA SQLFORM.grid personalizado ***************
    elquery = (( (db.queja.fk_comercio==db.comercio.id)&
            (db.comercio.fk_municipio==db.municipio.id)&
            (db.municipio.fk_departamento==db.departamento.id)&
            (db.departamento.fk_region==db.region.id)&
            (db.region.name=='SUR')&
            (db.queja.fecha >='2021-01-01 00:00:00')
              ))
    
    fields = (db.queja.fecha, db.queja.fk_comercio, db.queja.contenido)
   
    grid = SQLFORM.grid(query=elquery, fields=fields, csv=False, deletable=True,  searchable=True)
     #*******FINALIZA SQLFORM.grid personalizado ***************
    
    return dict(mygrid=grid, labels=labels, data=data, mensaje = msg)

def oriente():
    msg = "def oriente"

    #Comercios que no recibieron quejas durante 2021 oriente
    # ******** Aquí empieza la consulta ********   
    row_count = db(
            (db.queja.fk_comercio==db.comercio.id)&
            (db.comercio.fk_municipio==db.municipio.id)&
            (db.municipio.fk_departamento==db.departamento.id)&
            (db.departamento.fk_region==db.region.id)&
            (db.region.name=='ORIENTE')&
            (db.queja.fecha.year() != 2021)
            ).select(
                db.comercio.name,
                db.municipio.name,
                groupby = db.comercio.name,
                orderby= ~db.comercio.name,
            )
    # **********Finaliza consulta **********************
       
    return dict(mygrid=grid, registros= row_count, mensaje = msg)

def region():
    count = db.queja.id.count()
    # Consulta para la gráfica
    row_region = db(
            (db.queja.fk_comercio==db.comercio.id)&
            (db.comercio.fk_municipio==db.municipio.id)&
            (db.municipio.fk_departamento==db.departamento.id)&
            (db.departamento.fk_region==db.region.id)
            ).select(
                db.region.name,
                count,
                groupby = db.region.name,
                orderby= ~db.queja.fecha,
            )
    # **********Finaliza consulta **********************
    #EN def norte() arriba está comentado bastante de esta función / ingresamos el nombre del comercio en labels[] 
    # y la cantidad de veces que se ha colocado una queja   data[]
    labels=[]
    data=[]    
    for line in row_region:
        labels.append(line.region.name)
        data.append(line._extra[count])

    # ****Consulta para la tabla ***********
    # Consulta de quejas por region. Ordenados por region - Obtiene fecha de la queja, nombre del comercio y region a la que pertenece    
    row_region_table = db(
            (db.queja.fk_comercio==db.comercio.id)&
            (db.comercio.fk_municipio==db.municipio.id)&
            (db.municipio.fk_departamento==db.departamento.id)&
            (db.departamento.fk_region==db.region.id)
            ).select(
                db.queja.fecha,
                db.comercio.name,
                db.region.name,
                groupby = db.comercio.name,
                orderby= ~db.region.name,
            )

    return dict(msg='Region',labels=labels, data=data, registros= row_region_table)
    #FIN REGION

def departamento():
    count = db.queja.id.count()
    # Consulta para la gráfica
    row_departamento = db(
            (db.queja.fk_comercio==db.comercio.id)&
            (db.comercio.fk_municipio==db.municipio.id)&
            (db.municipio.fk_departamento==db.departamento.id)&
            (db.departamento.fk_region==db.region.id)
            ).select(
                db.departamento.name,
                count,
                groupby = db.departamento.name,
                orderby= ~db.queja.fecha,
            )
    # **********Finaliza consulta **********************
    #EN def norte() arriba está comentado bastante de esta función / ingresamos el nombre del comercio en labels[] 
    # y la cantidad de veces que se ha colocado una queja   data[]
    labels=[]
    data=[]    
    for line in row_departamento:
        labels.append(line.departamento.name)
        data.append(line._extra[count])

    # ****Consulta para la tabla ***********
    # Consulta de quejas por region. Ordenados por region - Obtiene fecha de la queja, nombre del comercio y region a la que pertenece    
    row_departamento_table = db(
            (db.queja.fk_comercio==db.comercio.id)&
            (db.comercio.fk_municipio==db.municipio.id)&
            (db.municipio.fk_departamento==db.departamento.id)&
            (db.departamento.fk_region==db.region.id)
            ).select(
                db.queja.fecha,
                db.comercio.name,
                db.departamento.name,
                groupby = db.comercio.name,
                orderby= db.departamento.name,
            )

    return dict(msg='Region',labels=labels, data=data, registros= row_departamento_table)
    #FIN DEPARTAMENTO

def municipio():
    #Consulta para elegir departamentos
    dep = None
    departamentos = db().select(db.departamento.ALL)

    if request.vars:
        dep = request.vars.get("departamento_name")
        

    #comercio_name = request.vars.get("nom_comercio")


    #form_elegir_dep = SQLFORM(db.departamento,
    #                        labels ={'name':'Elija el departamento',})

    #if form_elegir_dep.process().accepted:
    #   response.flash = 'SU QUEJA HA SIDO REGISTRADA GRACIAS'
    #   return redirect(URL('default', 'confirmacion'))
    #elif form_elegir_dep.errors:
    #   response.flash = 'El formulario tiene errores'
    #else:
    #   response.flash = 'Por favor complete el formulario'
    

    count = db.queja.id.count()
    # Consulta para la gráfica
    row_departamento = db(
            (db.queja.fk_comercio==db.comercio.id)&
            (db.comercio.fk_municipio==db.municipio.id)&
            (db.municipio.fk_departamento==db.departamento.id)&
            (db.departamento.fk_region==db.region.id)&
            (db.departamento.id==dep)
            ).select(
                db.municipio.name,
                count,
                groupby = db.municipio.name,
                orderby= ~db.queja.fecha,
            )
    # **********Finaliza consulta **********************
    #EN def norte() arriba está comentado bastante de esta función / ingresamos el nombre del comercio en labels[] 
    # y la cantidad de veces que se ha colocado una queja   data[]
    labels=[]
    data=[]    
    for line in row_departamento:
        labels.append(line.municipio.name)
        data.append(line._extra[count])

    # ****Consulta para la tabla ***********
    # Consulta de quejas por region. Ordenados por region - Obtiene fecha de la queja, nombre del comercio y region a la que pertenece    
    row_departamento_table = db(
            (db.queja.fk_comercio==db.comercio.id)&
            (db.comercio.fk_municipio==db.municipio.id)&
            (db.municipio.fk_departamento==db.departamento.id)&
            (db.departamento.fk_region==db.region.id)&
            (db.departamento.id==dep)
            ).select(
                db.queja.fecha,
                db.comercio.name,
                db.municipio.name,
                groupby = db.comercio.name,
                orderby= db.departamento.name,
            )

    return dict(departamento=departamentos, dep_id =dep, labels=labels, data=data, registros= row_departamento_table)
    #FIN municipio

def rango_fecha():
    #Consulta para elegir departamentos
    import datetime
    dep = None
    fecha_inicial = None
    fecha_final = None
    departamentos = db().select(db.departamento.ALL)

    form_rango= SQLFORM(db.rango,
                            labels ={'fecha_inicial':'Fecha Inicial','fecha_final':'Fecha Final'})
    
    #con form_rango.validate() se logró que solo envie los datos acá sin mandarlos a la base de datos directamente del SQLFORM
    if form_rango.validate():
        fecha_inicial = request.vars.get("fecha_inicial")
        fecha_final = request.vars.get("fecha_final")
        dep = True

        #Como fecha inicial es string en d/m/y se tuvo que convertir a un objeto date.time Y-d-d
        #Arriba en el inicio de la función hay un import sino no funciona
        fecha_inicial_obj = datetime.datetime.strptime(fecha_inicial, "%d/%m/%Y").strftime("%Y-%m-%d")
        fecha_final_obj = datetime.datetime.strptime(fecha_final, "%d/%m/%Y").strftime("%Y-%m-%d")

        # ****Consulta para la tabla ***********
        # Consulta de quejas por region. Ordenados por region - Obtiene fecha de la queja, nombre del comercio y region a la que pertenece    
        row_departamento_table = db(
                (db.queja.fk_comercio==db.comercio.id)&
                (db.comercio.fk_municipio==db.municipio.id)&
                (db.municipio.fk_departamento==db.departamento.id)&
                (db.departamento.fk_region==db.region.id)&
                (db.queja.fecha >= fecha_inicial_obj)&
                (db.queja.fecha <= fecha_final_obj)
                ).select(
                    db.queja.fecha,
                    db.comercio.name,
                    db.municipio.name,
                    groupby = db.comercio.name,
                    orderby= ~db.queja.fecha,
                )
        return dict(dep_id =dep, registros= row_departamento_table)

    return dict(form=form_rango, dep_id =dep)
    #FIN rango_fecha

def confirmacion():
    return dict(message=T('Welcome to web2py!'))
    