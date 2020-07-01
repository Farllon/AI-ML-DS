#!/usr/bin/env python
# coding: utf-8

# ### Encontrando Conectores-Chave
# 
# É seu primeiro dia de trabalho na DataSciencester e o vice-presidente de Rede (networking) está cheio de perguntas sobre seus usuários. Até agora, ele não teve ninguém para perguntar, então ele está muito empolgado em ter você aqui. Particularmente, ele quer que você identifique quem são os “conectores-chave” entre os cientistas de dados. Para isso, ele lhe dá uma parte de toda a rede da DataSciencester. Na vida real, você geralmente não recebe os dados de que precisa. O Capítulo 9 é voltado para a obtenção de dados. Com o que se parece essa parte dos dados? Ela consiste em uma lista de usuários, cada um representado por um dict que contém um id (um número) para cada usuário ou usuária e um name (que por uma das grandes coincidências cósmicas que rima com o id do usuário):

users = [
{ "id": 0, "name": "Hero" },
{ "id": 1, "name": "Dunn" },
{ "id": 2, "name": "Sue" },
{ "id": 3, "name": "Chi" },
{ "id": 4, "name": "Thor" },
{ "id": 5, "name": "Clive" },
{ "id": 6, "name": "Hicks" },
{ "id": 7, "name": "Devin" },
{ "id": 8, "name": "Kate" },
{ "id": 9, "name": "Klein" }
]


# Ele também fornece dados “amigáveis”, representados por uma lista de pares de IDs:


friendships = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4),
               (4, 5), (5, 6), (5, 7), (6, 8), (7, 8), (8, 9)]


# Por exemplo, a tupla (0,1) indica que o cientista de dados com a id 0 (Hero) e o cientista de dados com a id 1 (Dunn) são amigos. Já que representamos nossos usuários como dicts, é fácil de aumentá-los com dados extras.
# Por exemplo, talvez nós queiramos adicionar uma lista de amigos para cada usuário. Primeiro nós configuramos a propriedade friends de cada usuário em uma lista vazia:


for user in users:
    user["friends"] = []


# Então, nós povoamos a lista com os dados de friendships:


for i, j in friendships:
    users[i]["friends"].append(users[j]) # Adiciona j como amigo de i
    users[j]["friends"].append(users[i]) # Adiciona i como amigo de j


# Uma vez que o dict de cada usuário contenha uma lista de amigos, podemos facilmente perguntar sobre nosso gráfico, como “qual é o número médio de conexões?”
# Primeiro, encontramos um número total de conexões, resumindo os tamanhos de todas as listas de friends:


def number_of_friends(user):

    return len(user["friends"]) # tamanho da lista friend_ids

total_connections = sum(number_of_friends(user) for user in users)

print(total_connections)


# Então, apenas dividimos pelo número de usuários:


num_users = len(users)

avg_connections = total_connections / num_users

print(avg_connections)


# Também é fácil de encontrar as pessoas mais conectadas — são as que possuem o maior número de amigos.
# 
# Como não há muitos usuários, podemos ordená-los de “muito amigos” para“menos amigos”:


num_friends_by_id = [(user["id"], number_of_friends(user)) for user in users]


sorted(num_friends_by_id, key=lambda n : n[1], reverse=True)


# Uma maneira de pensar sobre o que nós fizemos é uma maneira de identificar as
# pessoas que são, de alguma forma, centrais para a rede. Na verdade, o que
# acabamos de computar é uma rede métrica de grau de centralidade

# Enquanto você está preenchendo os papéis de admissão, a vice-presidente da
# Fraternidade chega a sua mesa. Ela quer estimular mais conexões entre os seus
# membros, e pede que você desenvolva sugestões de “Cientistas de Dados Que
# Você Talvez Conheça”. Seu primeiro instinto é sugerir um usuário que possa conhecer amigos de
# amigos. São fáceis de computar: para cada amigo de um usuário, itera sobre os
# amigos daquela pessoa, e coleta todos os resultados:


def friends_of_friend_ids_bad(user):
# “foaf” é abreviação de “friend of a friend”
    return [foaf["id"] 
            for friend in user["friends"] # para cada amigo de usuário
                for foaf in friend["friends"]] # pega cada _their_friends


# Quando chamamos users[0] (Hero), ele produz:


friends_of_friend_ids_bad(users[0])


# Isso inclui o usuário 0 (duas vezes), uma vez que Hero é, de fato, amigo de
# ambos os seus amigos. Inclui os usuários 1 e 2, apesar de eles já serem amigos
# do Hero. E inclui o usuário 3 duas vezes, já que Chi é alcançável por meio de
# dois amigos diferentes:

print([friend["id"] for friend in users[0]["friends"]])# [1, 2]
print([friend["id"] for friend in users[1]["friends"]])# [0, 2, 3]
print([friend["id"] for friend in users[2]["friends"]])# [0, 1, 3]


# Saber que as pessoas são amigas-de-amigas de diversas maneiras parece uma
# informação interessante, então talvez nós devêssemos produzir uma contagem de
# amigos em comum. Definitivamente, devemos usar uma função de ajuda para
# excluir as pessoas que já são conhecidas do usuário:


from collections import Counter # não carregado por padrão

def not_the_same(user, other_user):
    """dois usuários não são os mesmos se possuem ids diferentes"""
    return user["id"] != other_user["id"]

def not_friends(user, other_user):
    """other_user não é um amigo se não está em user[“friends”];
    isso é, se é not_the_same com todas as pessoas em user[“friends”]"""
    return all(not_the_same(friend, other_user)
        for friend in user["friends"])

def friends_of_friend_ids(user):
    return Counter(foaf["id"]
        for friend in user["friends"] # para cada um dos meus amigos
        for foaf in friend["friends"] # que contam *their* amigos
        if not_the_same(user, foaf) # que não sejam eu
        and not_friends(user, foaf)) # e que não são meus amigos

print(friends_of_friend_ids(users[3])) # Counter({0: 2, 5: 1})


# Isso diz sobre Chi (id 3) que ela possui dois amigos em comum com Hero (id 0)
# mas somente um amigo em comum com Clive (id 5).
# Como um cientista de dados, você sabe que você pode gostar de encontrar
# usuários com interesses similares (esse é um bom exemplo do aspecto
# “competência significativa” de data science). Depois de perguntar por aí, você
# consegue pôr as mãos nesse dado, como uma lista de pares (user_id, interest):

interests = [
    (0, "Hadoop"), (0, "Big Data"), (0, "HBase"), (0, "Java"),
    (0, "Spark"), (0, "Storm"), (0, "Cassandra"),
    (1, "NoSQL"), (1, "MongoDB"), (1, "Cassandra"), (1, "HBase"),
    (1, "Postgres"), (2, "Python"), (2, "scikit-learn"), (2, "scipy"),
    (2, "numpy"), (2, "statsmodels"), (2, "pandas"), (3, "R"), (3, "Python"),
    (3, "statistics"), (3, "regression"), (3, "probability"),
    (4, "machine learning"), (4, "regression"), (4, "decision trees"),
    (4, "libsvm"), (5, "Python"), (5, "R"), (5, "Java"), (5, "C++"),
    (5, "Haskell"), (5, "programming languages"), (6, "statistics"),
    (6, "probability"), (6, "mathematics"), (6, "theory"),
    (7, "machine learning"), (7, "scikit-learn"), (7, "Mahout"),
    (7, "neural networks"), (8, "neural networks"), (8, "deep learning"),
    (8, "Big Data"), (8, "artificial intelligence"), (9, "Hadoop"),
    (9, "Java"), (9, "MapReduce"), (9, "Big Data")
]


# Por exemplo, Thor (id 4) não possui amigos em comum com Devin (id 7), mas
# compartilham do interesse em aprendizado de máquina.
# 
# É fácil construir uma função que encontre usuários com o mesmo interesse:


def data_scientists_who_like(target_interest):
    return [user_id
        for user_id, user_interest in interests
            if user_interest == target_interest]


# Funciona, mas a lista inteira de interesses deve ser examinada para cada busca.
# Se tivermos muitos usuários e interesses (ou se quisermos fazer muitas buscas),
# seria melhor construir um índice de interesses para usuários:


from collections import defaultdict
# as chaves são interesses, os valores são listas de user_ids com interests
user_ids_by_interest = defaultdict(list)

for user_id, interest in interests:
    user_ids_by_interest[interest].append(user_id)


# E outro de usuários para interesses:
# 


# as chaves são user_ids, os valores são as listas de interests para aquele user_id
interests_by_user_id = defaultdict(list)

for user_id, interest in interests:
    interests_by_user_id[user_id].append(interest)


# Agora fica fácil descobrir quem possui os maiores interesses em comum com um
# certo usuário:
#    - Itera sobre os interesses do usuário.
#    - Para cada interesse, itera sobre os outros usuários com aquele interesse.
#    - Mantém a contagem de quantas vezes vemos cada outro usuário

def most_common_interests_with(user):
    return Counter(interested_user_id
        for interest in interests_by_user_id[user["id"]]
            for interested_user_id in user_ids_by_interest[interest]
                if interested_user_id != user["id"])

most_common_interests_with(users[0])


# Poderíamos usar esse exemplo para construir um recurso mais rico de
# “Cientistas de Dados Que Você Deveria Conhecer” baseado em uma combinação
# de amigos e interesses em comum.


