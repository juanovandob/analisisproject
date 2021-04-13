# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
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
    #form_comercio = SQLFORM.grid(db.comercio, fields=[db.comercio.name, db.comercio.direccion],
    #                              headers={'name': 'Nombre Comercio', 'direccion': 'Dirección'}, csv=False)
    
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
        
        return redirect(URL('default', 'queja'))

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
    return dict(form=form_comercio, categories=departamentos,themakers=municipios, makers=makers, message=T('Welcome to web2py!'))

    #return dict(form=form_comercio)

def maker():
    makers = db(db.municipio.fk_departamento==request.vars.category_name).select(db.municipio.ALL)
    result = "<select name='maker_name'>"
    for maker in makers:
        result += "<option value='" + str(maker.id) + "'>" + maker.name + "</option>"  
    result += "</select>"
    return XML(result)

def queja():
    form_queja= SQLFORM(db.queja,
                            labels ={'fecha':'Fecha','contenido':'Queja',
                                    'peticion':'Petición','fk_comercio':'Comercio'})
    if form_queja.process().accepted:
       response.flash = 'SU QUEJA HA SIDO REGISTRADA GRACIAS'
       return redirect(URL('default', 'index'))
    elif form_queja.errors:
       response.flash = 'El formulario tiene errores'
    else:
       response.flash = 'Por favor complete el formulario'
      
    #form_comercio = SQLFORM.grid(db.comercio, fields=[db.comercio.name, db.comercio.direccion],
    #                              headers={'name': 'Nombre Comercio', 'direccion': 'Dirección'}, csv=False)
    return dict(form=form_queja)

def estadistica():
     return dict(message=T('Estadísticas!'))


    