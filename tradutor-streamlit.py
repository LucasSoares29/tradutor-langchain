import os
import streamlit as st
import time
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain_ollama.llms import OllamaLLM
from dotenv import load_dotenv

load_dotenv()
openai_key = os.getenv('OPENAI_API_KEY')

#### Criando as opções
opcao_selecionada = ["Inglês", "Espanhol", "Francês", "Alemão", "Japonês"]

#### Armazenando as respostas com session_state. Caso contrário o programa reinicia:
if 'respostas' not in st.session_state: st.session_state.respostas = []

#### Armazenando a escolha do radio button com session_state. Caso contrário o programa reinicia
if "escolha" not in st.session_state: st.session_state.escolha = None


#### Criando os modelos
llm = ChatOpenAI(temperature=0.8,
                 model_name="gpt-4o-mini")
llm_llama = OllamaLLM(model="llama3.2")
llm_mistral = OllamaLLM(model="mistral")


#### Criando o prompt
system_prompt = """
                    Você é um expert em línguas. Seu objetivo é a partir de uma frase em Português para o {idioma} que o usuário escolher.
                    Retorne apenas a frase traduzida
                    Frase do usuário: {frase}
"""

prompt_template1 = PromptTemplate(input_variables=["idioma", "frase"], 
                                  template=system_prompt)

#### Interface
st.title("Tradutor automático")
frase = st.text_input("Digite uma frase para traduzir...")
idioma = st.selectbox(label="Escolha um idioma", 
                      options=opcao_selecionada)

if st.button("Traduzir") and frase:
    # Aparece um spinner para criar este conto
    with st.spinner("Gerando tradução modelo 1..."):
        chain = prompt_template1 | llm | StrOutputParser()
        resposta = chain.invoke({"idioma": idioma, "frase": frase})
        st.session_state.respostas.append(resposta)
        time.sleep(1)
    with st.spinner("Gerando tradução modelo 2..."):
        chain_2 = prompt_template1 | llm_llama | StrOutputParser()
        resposta = chain_2.invoke({"idioma": idioma, "frase": frase})
        st.session_state.respostas.append(resposta)
        time.sleep(1)
    with st.spinner("Gerando tradução modelo 3..."):
        chain_3 = prompt_template1 | llm_mistral | StrOutputParser()
        resposta = chain_3.invoke({"idioma": idioma, "frase": frase})
        st.session_state.respostas.append(resposta)
        time.sleep(1)

    st.session_state.respostas.append("Todas atendem")

output = ""

if len(st.session_state.respostas) > 0:
    escolha = st.radio(label="Qual dessas é a melhor tradução?", options=st.session_state.respostas, 
                        index=None)

    st.session_state.escolha = escolha
    
    if escolha == st.session_state.respostas[0]:
        output = "A melhor tradução foi a do modelo gpt-4o-mini"
    elif escolha == st.session_state.respostas[1]:
        output = "A melhor resposta foi a do modelo Llama3.2"
    elif escolha == st.session_state.respostas[2]:
        output = "A melhor resposta foi a do modelo Mistral"
    
    if output:
        st.write(output)

    print(escolha)

    reiniciar = st.button("🔄 Recarregar Página")

    if reiniciar:
        st.session_state.clear()
        st.rerun()









