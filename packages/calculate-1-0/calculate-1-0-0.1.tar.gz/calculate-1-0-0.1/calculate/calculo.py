
import openai



def enviar_mensagem(mensagem):  #mensagem é o que queremos
    chave_api = input("Qual é: ").strip()
    openai.api_key = chave_api
    resposta=openai.ChatCompletion.create(
        model = "gpt-4-1106-preview",
        messages=[
            {"role": "user", "content":mensagem}
        ]
    
    )     
    print(resposta["choices"][0]["message"]['content'])

