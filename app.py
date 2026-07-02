from flask import Flask, jsonify, request



app = Flask(__name__)



# Simulação de estoque hospitalar

materiais = [

{

"codigo": 1,

"nome": "Luvas descartáveis",

"descricao": "Caixa com 100 unidades",

"quantidade": 3,

"valor": 25.0,

"indicador": "baixo",

"data": "2026-07-01",

"horario": "10:30"

},

{

"codigo": 2,

"nome": "Máscaras cirúrgicas",

"descricao": "Pacote com 50",

"quantidade": 15,

"valor": 40.0,

"indicador": "ok",

"data": "2026-07-01",

"horario": "11:00"

}

]



@app.route("/")

def home():

return "API hospitalar funcionando!"



# Listar materiais

@app.route("/materiais", methods=["GET"])

def listar():

return jsonify(materiais)



# Adicionar material

@app.route("/materiais", methods=["POST"])

def adicionar():

novo = request.json

materiais.append(novo)

return jsonify({"mensagem": "Material adicionado!"})



# Materiais em falta (quantidade baixa)

@app.route("/em-falta", methods=["GET"])

def em_falta():

faltando = [m for m in materiais if m["quantidade"] < 5]

return jsonify(faltando)



if __name__ == "__main__":

app.run(debug=True)