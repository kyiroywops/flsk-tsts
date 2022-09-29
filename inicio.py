from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")



@app.route("/index")
def formCredito():
    return render_template("index.html")

@app.route("/agregarUsuario", methods=["POST"])
def agregarUsuario():
    nombre = request.form["nombre"]
    monto = request.form["monto"]
    cuotas = request.form["cuotas"]
    segurodesgravamen = request.form["segurodesgravamen"]
    segurocontraincendio = request.form["segurocontraincendio"]

    if nombre == "" or monto == "" or segurodesgravamen == "" or segurocontraincendio == "":
        return render_template("index.html", mensaje="Debe completar todos los campos")
    elif not nombre.isalpha():
        return render_template("index.html", mensaje="El nombre debe contener solo letras")
    elif not monto.isdigit():
        return render_template("index.html", mensaje="El monto debe contener solo numeros")
    elif monto > 0:
        return render_template("index.html", mensaje="El monto debe ser mayor a 0")
    elif cuotas == "":
        return render_template("index.html", mensaje="Debe seleccionar una cuota") 
    
    ## calculo credito
    def calcularCredito(monto):
        uf = 34217.38
        montoPesos = monto * uf
        return montoPesos

    def porcentaje(años, porcentaje):
        if años > 0 and años >= 10:
            return porcentaje * 25
        elif años > 10 and años >= 20:
            return porcentaje * 35
        else:
            return porcentaje * 45

    def intereses(montoPesos, porcentaje):
        interes = montoPesos * porcentaje/100
        return interes

    def seguroDesgravamen(montoPesos, segurodesgravamen):
        if segurodesgravamen == "no":
            seguroDesgravamen = 0
        else:
            seguroDesgravamen = montoPesos * 0.05
        return seguroDesgravamen

    def seguroContraIncendio(montoPesos, segurocontraincendio):
        if segurocontraincendio == "no":
            seguroIncendio = 0
        else:
            seguroIncendio = montoPesos * 0.05
        return seguroIncendio

    def montoApagar(montoPesos, interes, seguroDesgravamen, seguroIncendio):
        montoApagar = montoPesos + interes + seguroDesgravamen + seguroIncendio
        return montoApagar
            

    def cuotas(montoApagar, cuotas):
        cuota = montoApagar / cuotas * 12
        return cuota

    def cuotasMensual(cuota):
        cuotaMensual = cuota / 12
        return cuotaMensual

    def informacion(nombre, uf, montoPesos, interes, seguroDesgravamen, seguroIncendio, montoApagar, cuota, cuotaMensual, cuotas, segurodesgravamen, segurocontraincendio):
        informacion = {
            "nombre": nombre,
            "uf": uf,
            "cuotas": cuotas,
            "montoPesos": montoPesos,
            "segurodesgravamen": segurodesgravamen,
            "segurocontraincendio": segurocontraincendio,

            "interes": interes,
            "seguroDesgravamen": seguroDesgravamen,
            "seguroIncendio": seguroIncendio,
            "montoApagar": montoApagar,
            "cuota": cuota,
            "cuotaMensual": cuotaMensual
        }
        return informacion
        
    return render_template("index.html", mensaje="Credito calculado", informacion=informacion)






@app.route("/informacion")
def informacion():
    return render_template("informacion.html")


if __name__ == '__main__':
      app.run(host='0.0.0.0', port=80)

app.run(debug = True)