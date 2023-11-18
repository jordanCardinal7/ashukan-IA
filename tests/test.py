   1: """
    En tant qu'analyste des données, tu dois traiter les informations recueillies lors {event_name}. Ton objectif est de {objective}.
    Approche cette tâche étape par étape, prends ton temps et ne saute pas d'étape:

    - Identifier et regrouper les propositions similaires en les analysant pour leur contenu, leur sens et leurs thèmes. Chaque groupe d'idées similaires comptera comme une seule entrée.
    - Dans le cas où une entrée traite de plusieurs sujets à la fois, traiter chacun des sujets comme une entrée distincte.
    - Dans le cas où une entrée est ambigüe, la regrouper avec les entrées ayant la probabilité de pertinence la plus proche.
    - Classer toutes les entrées dans une liste ordonnée par priorité (fréquence de mention), en indiquant combien de fois chacune d’elles apparaît
    - Ajouter pour chaque catégorie principale, une sous-liste contenant les idées originales associées.

    EXEMPLE DE FORMAT DE SORTIE: [
        << Question >>

        **Entrée regroupée (mentionnée # fois)**
            - entrée originale associée
            - entrée originale associée
    ]

    Voici les données en réponse à la question: 
    """,

1: """
    En tant qu'analyste des données, tu dois traiter les informations recueillies lors {event_name}. Ton objectif est de {objective}.
    Prends ton temps et approche le problème dans son ensemble, de façon holistique, de manière à faire ressortir de façon concise et précise les idées les plus centrales/prédominantes.

    - Regroupe les idées similaires et compte-les comme une seule entrée, en analysant les phrases pour leur contenu, leur sens et leurs thèmes, puis regroupe-les en conséquence. 
    - Dans le cas où une entrée traite de plusieurs sujets à la fois, traite chacun des sujets comme une entrée distincte. 
    - Dans le cas où une entrée est ambigüe, regroupe-la avec les entrées ayant la probabilité de pertinence la plus proche selon une analyse sémantique. 
    - Classe toutes les entrées dans une liste numérotée ordonnée par priorité (fréquence de mention) en indiquant combien de fois chacune d’elles apparaît, et en ajoutant pour chacune, dans une sous-liste, les entrées originales y étant associées. 

    EXEMPLE DE FORMAT DE SORTIE: [
        << Question >>

        **Entrée regroupée (mentionnée # fois)**
            - entrée originale associée
            - entrée originale associée
    ]

    Voici les données en réponse à la question:
    """