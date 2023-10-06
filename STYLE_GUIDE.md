# EN
# Code Style Guide

This code style guide describes the conventions we follow for Python source code in this project. Its aim is to maintain consistency and readability in the code, making collaboration among contributors more accessible.

## Indentation

Use a 4-space indentation for each level of indentation. Avoid using tabs. Configure your editor to replace tabs with spaces.

```python
# Good indentation
def example_function():
    if condition:
        instruction()
```

## Line Length

Limit the length of each code line to 80 characters. If a line exceeds this limit, you can either break it or use implicit continuation.

```python
# Maximum line length of 80 characters
long_variable = "This is an example of a long code line that should be broken to adhere to the 80-character limit."
```

## Whitespace

- Add a space after each comma in lists, tuples, and function calls.
- Do not add a space immediately before a comma or semicolon.
- Use spaces around operators (e.g., `=`, `+`, `-`, `*`, `/`) to improve readability.

```python
# Good spacing practices
my_list = [1, 2, 3]
result = variable1 + variable2
```

## Docstrings

Use docstrings to document modules, classes, and functions. Follow the [PEP 257 docstring convention](https://www.python.org/dev/peps/pep-0257/) for documentation conventions.

```python
def example_function(parameter):
    """
    This is a docstring that explains the function and its parameters.

    Args:
        parameter (type): Description of the parameter.

    Returns:
        return_type: Description of the function's result.
    """
    # Function body
```

## Naming

- Use lowercase variable and function names with words separated by underscores (snake_case).
- Use CamelCase for class names (CamelCase).
- Avoid single-letter variable names like `l` (lowercase L) or `O` (uppercase O) to prevent confusion.

```python
# Examples of naming conventions
my_variable = 42
my_example_function()
MyClass()
```

## Comments

Add explanatory comments when necessary to clarify the code. Comments should explain the "why" rather than the "how."

```python
# Good comment example
if condition:  # Check if the condition is true
    instruction()

# Avoid obvious comments
x = x + 1  # Increment x by 1
```

## Imports

- Place all imports at the beginning of the file.
- Use blank lines to separate import groups, such as standard library imports and third-party module imports.

```python
import standard_module

import module_1
import module_2
```

## Example of Good Code Style

Here's an example of code that follows the style conventions outlined above:

```python
def calculate_average(number_list):
    """
    Calculate the average of numbers in the list.

    Args:
        number_list (list): List of numbers.

    Returns:
        float: The average of numbers in the list.
    """
    total = 0
    for number in number_list:
        total += number
    average = total / len(number_list)
    return average
```

This code style guide aims to maintain consistency in the project's source code. Contributors are encouraged to follow it to ensure code readability and ease of maintenance.

# FR


# Guide de Style du Code

Ce guide de style du code décrit les conventions que nous suivons pour le code source Python dans ce projet. Il vise à maintenir la cohérence et la lisibilité du code, ce qui facilite la collaboration entre les contributeurs.

## Indentation

Utilisez une indentation de 4 espaces pour chaque niveau d'indentation. N'utilisez pas de tabulations. Configurez votre éditeur pour qu'il remplace les tabulations par des espaces.

```python
# Bonne indentation
def fonction_exemple():
    if condition:
        instruction()
```

## Longueur des lignes

Limitez la longueur de chaque ligne de code à 80 caractères. Si une ligne dépasse cette limite, vous pouvez la couper ou utiliser une continuation implicite.

```python
# Longueur maximale de ligne de 80 caractères
longue_variable = "Ceci est un exemple de longue ligne de code qui doit être coupée pour respecter la limite de 80 caractères."
```

## Espaces en blanc

- Ajoutez un espace après chaque virgule dans les listes, les tuples et les appels de fonctions.
- N'ajoutez pas d'espace immédiatement avant une virgule ou un point-virgule.
- Utilisez un espace autour des opérateurs (par exemple, `=`, `+`, `-`, `*`, `/`) pour améliorer la lisibilité.

```python
# Bonnes pratiques d'espacement
ma_liste = [1, 2, 3]
résultat = variable1 + variable2
```

## Docstrings

Utilisez des docstrings pour documenter les modules, les classes et les fonctions. Suivez la [convention de docstring PEP 257](https://www.python.org/dev/peps/pep-0257/) pour les conventions de documentation.

```python
def fonction_exemple(paramètre):
    """
    Ceci est une docstring qui explique la fonction et ses paramètres.

    Args:
        paramètre (type): Description du paramètre.

    Returns:
        type_de_retour: Description du résultat de la fonction.
    """
    # Corps de la fonction
```

## Nommage

- Utilisez des noms de variables et de fonctions en minuscules avec des mots séparés par des underscores (snake_case).
- Utilisez des noms de classe en CamelCase (CamelCase).
- Évitez les noms de variables uniques comme `l` (L minuscule) ou `O` (O majuscule) pour éviter la confusion.

```python
# Exemples de conventions de nommage
ma_variable = 42
ma_fonction_exemple()
MaClasse()
```

## Commentaires

Ajoutez des commentaires explicatifs lorsque cela est nécessaire pour clarifier le code. Les commentaires doivent expliquer le «pourquoi» plutôt que le «comment».

```python
# Bon exemple de commentaire
if condition:  # Vérifie si la condition est vraie
    instruction()

# Évitez les commentaires évidents
x = x + 1  # Incrémente x de 1
```

## Importations

- Placez toutes les importations au début du fichier.
- Utilisez des lignes vierges pour séparer les groupes d'importations, comme les importations de modules standard et les importations de modules tiers.

```python
import module_standard

import module_1
import module_2
```

## Exemple de bon style de code

Voici un exemple de code qui suit les conventions de style énoncées ci-dessus :

```python
def calcul_moyenne(liste_de_nombres):
    """
    Calcule la moyenne des nombres dans la liste.

    Args:
        liste_de_nombres (list): Liste de nombres.

    Returns:
        float: La moyenne des nombres dans la liste.
    """
    somme = 0
    for nombre in liste_de_nombres:
        somme += nombre
    moyenne = somme / len(liste_de_nombres)
    return moyenne
```

Ce guide de style du code vise à maintenir une cohérence dans le code source du projet. Les contributeurs sont encouragés à le suivre pour garantir la lisibilité et la facilité de maintenance du code.

