from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.db import connection
from decouple import config

# ---------------------------------------------

def envia_email(request):

    cursor = connection.cursor()

    cursor.execute("""
        select
            ek_pessoa.cod_pessoa as "Cod.Pessoa", 
            ek_pessoa.nome as "Nome cliente",
            extract(day from dt_nascimento) as dia,
            extract(month from dt_nascimento) as mes,
            extract(YEAR from dt_nascimento) as ano,

            extract(day from now()) as dia,
            extract(month from now()) as mes,
            extract(YEAR from now()) as ano,
	    ek_contato.observacao_contato
                   
        from ek_pessoa left join ek_contato on ek_pessoa.cod_pessoa = ek_contato.cod_pessoa 
        where 
            dt_nascimento::varchar <> '' 
            and extract(day from dt_nascimento) = extract(day from now()) 
            and extract(month from dt_nascimento) = extract(month from now())
            and ek_contato.contato_fiscal = 'P'
    """)

            

    aniversariantes = cursor.fetchall()

    if aniversariantes:
        for cliente in aniversariantes:
            try:
                send_mail(
                    subject = f"Feliz Aniversario" , #Assunto do email
                    message = f"""
                                { str(cliente[1]).capitalize().split(' ')[0] },hoje celebramos o dia de uma pessoa muito querida e especial: VOCÊ!!!🙏🏻🥳
            
                                💫 Te desejamos todas as alegrias e sorrisos possíveis! ✨
                                                
                                Parabéns👏🏻👏🏻👏🏻! Muita saúde, paz e sabedoria😉😁!
                                        
                                Um grande abraço, de toda nossa equipe! 🤗

                                Nova Aliança""" , 
                    from_email = config("EMAIL_HOST_USER") ,                
                    recipient_list = [ cliente[8] ] )
            except:
                print("Erro ao enviar o e-mail")

    return HttpResponse("Enviando e-mails aos aniversariantes de hoje !")



def getAniversariantes(requests):
    cursor = connection.cursor()

    cursor.execute("""
        select
            ek_pessoa.cod_pessoa as "Cod.Pessoa", 
            ek_pessoa.nome as "Nome cliente",
            extract(day from dt_nascimento) as dia,
            extract(month from dt_nascimento) as mes,
            extract(YEAR from dt_nascimento) as ano,

            extract(day from now()) as dia,
            extract(month from now()) as mes,
            extract(YEAR from now()) as ano,
	    ek_contato.observacao_contato
                   
        from ek_pessoa left join ek_contato on ek_pessoa.cod_pessoa = ek_contato.cod_pessoa 
        where 
            dt_nascimento::varchar <> '' 
            and extract(day from dt_nascimento) = extract(day from now()) 
            and extract(month from dt_nascimento) = extract(month from now())
            and ek_contato.contato_fiscal = 'P'
    """)


    aniversariantes = cursor.fetchall()

    if aniversariantes:
        html_message = '''
                    
                        <h1>Aniversariantes do Dia</h1>
                        
                        <table border=1>
                            <tr>
                                <th>Código Cliente</th>
                                <th>Nome do Cliente</th>
                                <th>Aniversario</th>
                            </tr>
                    '''

        for cliente in aniversariantes:

                html_message += f'''<tr>
                                <td>{cliente[0]}</td>
                                <td>{cliente[1]}</td>
                                <td>{int(cliente[2])}/{int(cliente[3])}/{int(cliente[4])}</td>
                            </tr>'''
        
        html_message += '</table>'
    else:
         html_message = "Não há aniversariantes no dia de hoje"

    try:
        send_mail(
            subject = f"Aniversariantes do Dia" , #Assunto do email
            message= "Segue abaixo os aniversariantes do dia: ",
            from_email = config("EMAIL_HOST_USER") , 
            recipient_list = [ config("EMAIL_RECEBER_ANIVERSARIO") ] ,
            html_message = html_message
            )
    except:
         print("Erro ao enviar e-mail.")

    


    return HttpResponse("Enviando e-mail para o adm com os aniversariantes do dia.")