# chatbot.py

from fuzzywuzzy import process


class Chatbot:
    def __init__(self):
        self.responses = {
            "olá": "Olá! Como posso ajudar você hoje?",
            "como você está?": "Estou apenas um programa, mas estou funcionando corretamente!",
            "quais são os horários de atendimento?": "Nosso horário de atendimento é de segunda a sexta, das 9h às 18h.",
            "qual é o endereço?": "Estamos localizados na Rua Exemplo, 123, Bairro Exemplo, Cidade Exemplo.",
            "quais vacinas estão disponíveis?": "Oferecemos vacinas contra Covid, hepatite B, sarampo, Quadrivalente, entre outras.",
            "como agendar uma vacinação?": "Você pode agendar uma vacinação através do nosso site ou ligando para nossa unidade.",
            "quais documentos são necessários para a vacinação?": "Por favor, traga seu documento de identidade e cartão de vacinação.",
            "qual é a idade mínima para vacinação?": "A idade mínima depende da vacina específica. Consulte nosso site para mais detalhes.",
            "as vacinas são gratuitas?": "Algumas vacinas são gratuitas, enquanto outras podem ter um custo. Verifique nossa tabela de preços.",
            "como posso cancelar um agendamento?": "Para cancelar um agendamento, entre em contato com nossa unidade pelo telefone.",
            "vacinas têm efeitos colaterais?": "Algumas vacinas podem ter efeitos colaterais leves, como dor no local da aplicação ou febre.",
            "posso tomar vacina se estiver doente?": "É recomendado consultar um médico antes de tomar qualquer vacina se você estiver doente.",
            "posso tomar várias vacinas ao mesmo tempo?": "Algumas vacinas podem ser administradas simultaneamente. Consulte um profissional de saúde.",
            "quanto tempo dura a imunidade das vacinas?": "A duração da imunidade varia de acordo com a vacina. Consulte as informações específicas da vacina.",
            "vacinas são seguras?": "Sim, todas as vacinas disponíveis passaram por rigorosos testes de segurança e eficácia.",
            "qual vacina preciso tomar para viajar?": "Dependendo do destino, você pode precisar de vacinas específicas. Consulte um médico ou clínica de viagens.",
            "como armazenar as vacinas em casa?": "Vacinas geralmente não devem ser armazenadas em casa. Elas precisam de condições específicas de armazenamento.",
            "o que fazer se perder o cartão de vacinação?": "Entre em contato com a unidade onde foi vacinado para obter um novo cartão de vacinação.",
            "as vacinas podem causar a doença?": "Não, as vacinas não causam a doença. Elas ajudam o corpo a desenvolver imunidade.",
            "como funciona a vacina de mRNA?": "As vacinas de mRNA ensinam nossas células a produzir uma proteína que desencadeia uma resposta imunológica.",
            "quais vacinas são recomendadas para crianças?": "Crianças devem seguir o calendário de vacinação recomendado pelo Ministério da Saúde.",
            "como o sistema funciona?": "O sistema foi desenvolvido para cadastro de vacinas, pacientes e hospitais. A ideia é poder unificar todas as informações, realizar o agendamento de vacinação e conseguir extrair relatórios.",
            "quem foi o desenvolvedor?": "Meu desenvolvedor foi o aluno Rafael Nadalin, GitHub: https://github.com/Tudolin, linkedin: https://www.linkedin.com/in/rafael-nadalin-68166722a, Portifólio: https://tudolin.github.io/",
            "Link do projeto?": "Aqui está o link do projeto no Github: https://github.com/Tudolin/projeto_integrado_unidombosco",
            "quais as funções que o sistema poderá executar?": "O sistema foi modelado podendo executar cadastros de usuários, unidades de vacinação e vacinas. Podendo também realizar o agendamento e exibir os dados em tempo real.",
            "quais funções que apresentam inteligência artificial?": "para o uso de inteligência artificial, desenvolvi esse chatbot, que consegue receber os inputs do usuário e responder as duvidas mais simples, onde antes precisaria de um funcionário respondendo algumas simples duvidas, agora podem ser respondidas de maneira automática, processar e pesquisar a resposta mais apropriada na base de dados desenvolvida",
        }
    
    def get_response(self, user_input):
        user_input = user_input.lower()
        closest_match, confidence = process.extractOne(user_input, self.responses.keys())
        if confidence > 60:
            return self.responses[closest_match]
        return "Desculpe, não entendi sua pergunta. Por favor, tente novamente."

chatbot = Chatbot()
