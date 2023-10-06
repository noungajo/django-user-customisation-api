
## Documentation du modèle Django

### Classe `AbstractUser`

Cette classe est définie en tant que modèle abstrait Django qui étend `AbstractBaseUser` et `PermissionsMixin` pour personnaliser le modèle utilisateur.

#### Attributs:

- `full_name` (CharField): Le nom complet de l'utilisateur.
- `address` (CharField): L'adresse de l'utilisateur.
- `date_of_birth` (DateField): La date de naissance de l'utilisateur.
- `numero_social` (CharField): Le numéro social de l'utilisateur.
- `remuneration` (CharField): Le type de rémunération de l'utilisateur (mensuel ou taux horaire).
- `base_salary` (IntegerField): Le salaire de base de l'utilisateur.
- `telephone` (CharField): Le numéro de téléphone de l'utilisateur.
- `email` (EmailField): L'adresse e-mail de l'utilisateur.
- `is_staff` (BooleanField): Indique si l'utilisateur peut se connecter à l'interface d'administration.
- `is_active` (BooleanField): Indique si l'utilisateur est actif.
- `date_joined` (DateTimeField): La date de création du compte de l'utilisateur.
- `user_image` (ImageField): L'image de profil de l'utilisateur.
- `is_superuser` (BooleanField): Indique si l'utilisateur est un superutilisateur.

#### Méthodes:

- `clean()`: Cette méthode assure que les données de l'utilisateur sont nettoyées avant d'être enregistrées dans la base de données. Elle normalise également l'adresse e-mail de l'utilisateur.
- `email_user(subject, message, from_email=None, **kwargs)`: Cette méthode permet d'envoyer un e-mail à l'utilisateur. Elle prend en paramètres le sujet, le message et éventuellement l'adresse e-mail de l'expéditeur.

### Classe `User`

Cette classe étend la classe `AbstractUser` et représente le modèle utilisateur utilisé dans votre application.

#### Attributs:

La classe `User` hérite de tous les attributs de la classe `AbstractUser`.

#### Méthodes:

La classe `User` n'a pas de méthodes supplémentaires par rapport à la classe `AbstractUser`.


## Documentation des sérialiseurs

### `UserSerializer`

Ce sérialiseur est utilisé pour la représentation JSON des instances de la classe `User`. Il utilise la classe `HyperlinkedModelSerializer` de Django REST framework pour afficher les champs et les relations sous forme d'URLs.

#### Attributs:

- `Meta`: Un attribut de classe qui définit le modèle associé et les champs à inclure dans la sérialisation.
  - `model` : Le modèle associé à ce sérialiseur (dans ce cas, c'est la classe `User`).
  - `fields` : Une liste des champs du modèle que nous souhaitons inclure dans la sérialisation JSON.

### `SaveUserSerializer`

Ce sérialiseur est utilisé pour la création et la mise à jour d'instances de la classe `User`. Il hérite du sérialiseur `UserSerializer` et ajoute certains champs supplémentaires qui ne doivent pas être accessibles lors de la création d'un nouvel utilisateur.

#### Attributs:

- `Meta`: Un attribut de classe qui définit le modèle associé et les champs à inclure dans la sérialisation.
  - `model` : Le modèle associé à ce sérialiseur (dans ce cas, c'est la classe `User`).
  - `fields` : Une liste des champs du modèle que nous souhaitons inclure dans la sérialisation JSON lors de la création ou la mise à jour.

- `create(validated_data)`: Cette méthode est utilisée pour créer une nouvelle instance de `User` à partir des données validées fournies en entrée. Elle appelle la méthode `create()` de la classe parent (`HyperlinkedModelSerializer`) pour effectuer la création.

### `PhoneVerificationSerializer`

Ce sérialiseur est utilisé pour la représentation JSON des instances de la classe `PhoneNumberVerification`.

#### Attributs:

- `Meta`: Un attribut de classe qui définit le modèle associé et les champs à exclure de la sérialisation.
  - `model` : Le modèle associé à ce sérialiseur (dans ce cas, c'est la classe `PhoneNumberVerification`).
  - `exclude` : Une liste des champs du modèle que nous souhaitons exclure de la sérialisation JSON.

### `CreatedUserSerializer`

Ce sérialiseur est utilisé pour la représentation JSON des instances de la classe `User` avec des informations supplémentaires sur la vérification du numéro de téléphone.

#### Attributs:

- `phone_verification`: Un champ qui est sérialisé à l'aide du sérialiseur `PhoneVerificationSerializer` pour afficher les détails de la vérification du numéro de téléphone.

- `Meta`: Un attribut de classe qui définit le modèle associé et les champs à inclure dans la sérialisation.
  - `model` : Le modèle associé à ce sérialiseur (dans ce cas, c'est la classe `User`).
  - `fields` : Une liste des champs du modèle que nous souhaitons inclure dans la sérialisation JSON.

### `DisplayUserSerializer`

Ce sérialiseur est utilisé pour la représentation JSON des instances de la classe `User` avec un ensemble limité d'informations.

#### Attributs:

- `Meta`: Un attribut de classe qui définit le modèle associé et les champs à inclure dans la sérialisation.
  - `model` : Le modèle associé à ce sérialiseur (dans ce cas, c'est la classe `User`).
  - `fields` : Une liste des champs du modèle que nous souhaitons inclure dans la sérialisation JSON.

- `create(validated_data)`: Cette méthode est utilisée pour créer une nouvelle instance de `User` à partir des données validées fournies en entrée. Elle appelle la méthode `create()` de la classe parent (`HyperlinkedModelSerializer`) pour effectuer la création.

### `UserLoginSerializer`

Ce sérialiseur est utilisé pour la représentation JSON des informations de connexion d'un utilisateur.

#### Attributs:

- `email`: Un champ pour le nom d'utilisateur (adresse e-mail).
- `password`: Un champ pour le mot de passe de l'utilisateur.

### `PhoneCodeSerializer`

Ce sérialiseur est utilisé pour la représentation JSON des informations de vérification du code de téléphone.

#### Attributs:

- `user`: Un champ pour spécifier la clé primaire de l'utilisateur associé à la vérification du numéro de téléphone.
- `code`: Un champ pour le code de vérification du numéro de téléphone.


## Documentation du code d'authentification personnalisé

### `EmailBackend`

Cette classe est une implémentation personnalisée de l'authentification dans Django. Elle hérite de la classe `ModelBackend` qui est la classe de base pour les backends d'authentification Django.

#### Attributs :

- `UserModel`: Cette variable stocke la classe de modèle utilisateur utilisée dans l'application. Elle est obtenue à partir de `get_user_model()` pour rendre le code plus générique et compatible avec tout modèle d'utilisateur personnalisé que vous pourriez utiliser dans le futur.

#### Méthodes :

- `authenticate(self, request=None, telephone=None, password=None, **kwargs)`: Cette méthode est appelée lorsqu'une tentative d'authentification est effectuée avec les informations d'identification fournies. Elle prend en paramètres :
  - `request`: La requête HTTP en cours (facultatif).
  - `telephone`: Le numéro de téléphone (ou adresse e-mail) fourni par l'utilisateur pour l'authentification.
  - `password`: Le mot de passe fourni par l'utilisateur pour l'authentification.
  - `**kwargs`: Des arguments supplémentaires (facultatif).

La méthode fonctionne de la manière suivante :

1. Vérification des paramètres obligatoires : Elle vérifie si les paramètres `telephone` et `password` sont fournis. Si l'un des deux est manquant, l'authentification échoue et la méthode retourne `None`.

2. Recherche de l'utilisateur : Elle tente de trouver un utilisateur ayant le numéro de téléphone (ou l'adresse e-mail) fourni en utilisant `User.objects.get(email=telephone)`. Si l'utilisateur est trouvé dans la base de données, l'objet `User` est renvoyé. Sinon, l'authentification échoue et la méthode retourne `None`.

3. Vérification du mot de passe : Si l'utilisateur est trouvé, la méthode vérifie si le mot de passe fourni correspond au mot de passe haché stocké dans la base de données à l'aide de la méthode `check_password()`. Si le mot de passe est correct et que l'utilisateur est autorisé à s'authentifier (grâce à `self.user_can_authenticate(user)`), alors l'authentification réussit et l'objet `User` est renvoyé. Sinon, l'authentification échoue et la méthode retourne `None`.

4. Traitement de l'erreur de modèle inexistant : Si l'utilisateur n'est pas trouvé dans la base de données (i.e., l'objet `UserModel.DoesNotExist` est levé), la méthode effectue un hachage du mot de passe fourni à l'aide de `UserModel().set_password(password)` pour réduire les différences de temps d'exécution entre un utilisateur existant et un utilisateur inexistant. Cela est utile pour prévenir les attaques par force brute basées sur la durée d'exécution de l'authentification.


## Configuration personnalisée de l'application Django

### `AUTH_USER_MODEL`

Cette configuration spécifie le modèle utilisateur personnalisé que vous avez défini. Vous avez défini `AUTH_USER_MODEL` comme `'users.User'`, indiquant que le modèle personnalisé utilisé pour les utilisateurs est `User` défini dans l'application `users`.

### `APPEND_SLASH` et `REMOVE_SLASH`

Ces configurations sont utilisées pour le routage d'URLs. `APPEND_SLASH` est défini sur `False`, ce qui signifie que les URLs sans barre oblique finale (`/`) seront également traitées sans barre oblique finale. `REMOVE_SLASH` est défini sur `True`, ce qui signifie que les URLs avec une barre oblique finale (`/`) seront également traitées sans barre oblique finale. Ces configurations peuvent être utiles pour gérer la redirection d'URLs avec ou sans barre oblique finale.

## Configurations d'authentification

### `AUTHENTICATION_BACKENDS`

Cette configuration spécifie les backends d'authentification utilisés dans l'application. Vous avez ajouté deux backends :

1. `'users.backend.EmailBackend'`: C'est une implémentation spécifique de l'authentification qui permet l'authentification basée sur l'adresse e-mail (ou le numéro de téléphone) fournie par l'utilisateur.
2. `'django.contrib.auth.backends.ModelBackend'`: C'est le backend d'authentification par défaut de Django qui permet l'authentification basée sur le nom d'utilisateur (username).

## Configurations de Django REST framework

### `REST_FRAMEWORK`

Cette configuration spécifie divers paramètres pour Django REST framework.

- `DEFAULT_AUTHENTICATION_CLASSES`: C'est une liste de classes d'authentification utilisées par défaut dans les vues DRF. Vous avez configuré `BasicAuthentication`, `SessionAuthentication` et `TokenAuthentication` pour être utilisés par défaut.
- `DEFAULT_PAGINATION_CLASS`: C'est la classe de pagination par défaut utilisée pour paginer les résultats de vos API.
- `PAGE_SIZE`: C'est le nombre d'objets affichés par page lors de la pagination.

## Configurations de Django REST Knox

### `REST_KNOX`

Ces configurations sont spécifiques au package `django-rest-knox`, qui fournit une gestion des tokens d'authentification plus sécurisée.

- `SECURE_HASH_ALGORITHM`: C'est l'algorithme de hachage utilisé pour générer les tokens.
- `AUTH_TOKEN_CHARACTER_LENGTH`: C'est la longueur des tokens d'authentification.
- `TOKEN_TTL`: C'est la durée de vie (Time-To-Live) d'un token.
- `USER_SERIALIZER`: C'est le sérialiseur utilisé pour afficher les informations utilisateur associées à un token.
- `TOKEN_LIMIT_PER_USER`: C'est le nombre maximal de tokens autorisés par utilisateur.
- `AUTO_REFRESH`: Active ou désactive le renouvellement automatique des tokens expirés.
- `MIN_REFRESH_INTERVAL`: C'est l'intervalle minimal entre deux renouvellements automatiques de token.
- `EXPIRY_DATETIME_FORMAT`: Le format de la date d'expiration du token.

## Configurations pour Swagger

### `SWAGGER_SETTINGS`

Ces configurations sont spécifiques au package `drf-yasg`, qui permet de générer une documentation interactive (Swagger) pour vos API REST.

- `SECURITY_DEFINITIONS`: C'est la définition de la sécurité utilisée pour Swagger. Vous avez configuré une définition "api_key" qui spécifie l'utilisation d'une clé d'API dans l'en-tête pour l'authentification.

## Configuration pour l'envoi d'e-mails

### `EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_USE_TLS`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`

Ces configurations sont utilisées pour configurer le backend d'e-mails et les paramètres associés pour envoyer des e-mails depuis l'application. Vous avez configuré l'envoi d'e-mails via le serveur SMTP d'Outlook.



## `RegistrationView`

Cette vue gère l'inscription d'un nouvel utilisateur.

- **Méthode HTTP** : POST
- **Endpoint** : /register/

#### Fonctionnement :

1. Reçoit les données d'un nouvel utilisateur sous forme de JSON dans le corps de la requête HTTP.
2. Valide les données reçues en utilisant le sérialiseur `SaveUserSerializer`.
3. Génère un code de vérification à 4 chiffres pour le numéro de téléphone de l'utilisateur.
4. Envoie le code de vérification par SMS et par e-mail à l'utilisateur.
5. Enregistre les informations de l'utilisateur dans la base de données en utilisant le sérialiseur `CreatedUserSerializer` et retourne les informations de l'utilisateur créé, y compris le code de vérification.

## `ListUsers`

Cette vue permet de lister tous les utilisateurs du système.

- **Méthode HTTP** : GET
- **Endpoint** : /users/

#### Fonctionnement :

1. Reçoit une requête HTTP GET sans aucun paramètre.
2. Récupère tous les utilisateurs de la base de données.
3. Sérialise chaque utilisateur avec le sérialiseur `DisplayUserSerializer`.
4. Renvoie une liste de tous les utilisateurs sous forme de JSON.

## `CurrentUser`

Cette vue permet de récupérer les informations de l'utilisateur actuellement authentifié.

- **Méthode HTTP** : GET
- **Endpoint** : /current_user/

#### Fonctionnement :

1. Reçoit une requête HTTP GET sans aucun paramètre.
2. Vérifie si l'utilisateur est authentifié.
3. Renvoie les informations de l'utilisateur actuellement authentifié sous forme de JSON.

## `UpdateUserViews`

Cette vue permet de mettre à jour les informations de l'utilisateur actuellement authentifié.

- **Méthode HTTP** : PUT, PATCH
- **Endpoint** : /update_user/

#### Fonctionnement :

1. Reçoit les données mises à jour de l'utilisateur sous forme de JSON dans le corps de la requête HTTP.
2. Vérifie si l'utilisateur est authentifié.
3. Met à jour les informations de l'utilisateur avec les nouvelles données en utilisant le sérialiseur `DisplayUserSerializer`.

## `DeleteUser`

Cette vue permet de désactiver (supprimer) un utilisateur.

- **Méthode HTTP** : DELETE
- **Endpoint** : /delete_user/

#### Fonctionnement :

1. Reçoit une requête HTTP DELETE sans aucun paramètre.
2. Vérifie si l'utilisateur est authentifié.
3. Désactive l'utilisateur actuellement authentifié en le marquant comme inactif dans la base de données.

## `PhoneNumberVerifyView`

Cette vue gère la vérification du code de téléphone reçu par l'utilisateur pour la vérification du numéro de téléphone.

- **Méthode HTTP** : POST
- **Endpoint** : /phone_number_verify/

#### Fonctionnement :

1. Reçoit le code de vérification envoyé par l'utilisateur sous forme de JSON dans le corps de la requête HTTP.
2. Vérifie si le code de vérification est correct et s'il n'a pas expiré.
3. Marque le numéro de téléphone de l'utilisateur comme vérifié en enregistrant l'heure de vérification dans la base de données.

## `PhoneCodeRenew`

Cette vue permet de régénérer un nouveau code de vérification pour le numéro de téléphone de l'utilisateur.

- **Méthode HTTP** : POST
- **Endpoint** : /phone_code_renew/

#### Fonctionnement :

1. Reçoit une requête HTTP POST contenant l'ID de l'utilisateur pour lequel un nouveau code de vérification doit être généré.
2. Génère un nouveau code de vérification à 4 chiffres.
3. Envoie le nouveau code de vérification par SMS à l'utilisateur.
4. Enregistre le nouveau code de vérification dans la base de données pour l'utilisateur concerné.

## `LoginView`

Cette vue gère l'authentification de l'utilisateur à l'aide du nom d'utilisateur (e-mail ou numéro de téléphone) et du mot de passe.

- **Méthode HTTP** : POST
- **Endpoint** : /login/

#### Fonctionnement :

1. Reçoit les informations d'identification de l'utilisateur (e-mail ou numéro de téléphone et mot de passe) sous forme de JSON dans le corps de la requête HTTP.
2. Vérifie les informations d'identification et authentifie l'utilisateur.
3. Génère un token d'authentification (si les informations d'identification sont valides) et le renvoie dans la réponse.

## `EmailCheckView`

Cette vue permet de vérifier si un e-mail particulier est déjà utilisé par un utilisateur enregistré.

- **Méthode HTTP** : POST
- **Endpoint** : /email_check/

#### Fonctionnement :

1. Reçoit une requête HTTP POST contenant l'e-mail à vérifier.
2. Vérifie si l'e-mail est déjà utilisé par un utilisateur enregistré.
3. Renvoie `True` si l'e-mail est déjà utilisé, sinon renvoie `False`.

## `TelephoneCheckView`

Cette vue permet de vérifier si un numéro de téléphone particulier est déjà utilisé par un utilisateur

 enregistré.

- **Méthode HTTP** : POST
- **Endpoint** : /telephone_check/

#### Fonctionnement :

1. Reçoit une requête HTTP POST contenant le numéro de téléphone à vérifier.
2. Vérifie si le numéro de téléphone est déjà utilisé par un utilisateur enregistré.
3. Renvoie `True` si le numéro de téléphone est déjà utilisé, sinon renvoie `False`.

Bien sûr ! Voici la documentation pour la fonction `send_email` :

# Fonction `send_email`

La fonction `send_email` est une fonction utilitaire pour envoyer des e-mails en utilisant les paramètres de configuration définis dans les paramètres `settings` de votre application Django. Elle utilise la classe `EmailMessage` de Django pour composer et envoyer l'e-mail.

## Paramètres

La fonction `send_email` prend trois paramètres :

1. `subject` (str) : Le sujet de l'e-mail que vous souhaitez envoyer.
2. `body` (str) : Le contenu de l'e-mail que vous souhaitez envoyer.
3. `recipient_email` (str) : L'adresse e-mail du destinataire à qui vous souhaitez envoyer l'e-mail.

## Configuration SMTP

La fonction utilise la configuration SMTP définie dans les paramètres `settings` de votre application Django pour établir la connexion avec le serveur de messagerie sortant (SMTP) et envoyer l'e-mail. Les paramètres SMTP utilisés sont :

- `EMAIL_HOST` : L'hôte du serveur SMTP.
- `EMAIL_PORT` : Le port du serveur SMTP.
- `EMAIL_HOST_USER` : L'adresse e-mail de l'expéditeur utilisée pour envoyer l'e-mail.
- `EMAIL_HOST_PASSWORD` : Le mot de passe associé à l'adresse e-mail de l'expéditeur.
- `EMAIL_USE_TLS` : Un booléen indiquant si TLS (Transport Layer Security) doit être utilisé pour sécuriser la connexion avec le serveur SMTP.

## Utilisation

La fonction `send_email` crée une connexion avec le serveur SMTP en utilisant les paramètres configurés dans les paramètres `settings` de votre application Django. Elle compose ensuite un e-mail à l'aide des paramètres `subject`, `body`, `email_from` (défini dans les paramètres `settings`) et `recipient_list` (contenant l'adresse e-mail du destinataire).

Enfin, la fonction `send()` est appelée pour envoyer l'e-mail en utilisant la connexion SMTP établie. L'e-mail est alors envoyé à l'adresse e-mail du destinataire spécifiée dans `recipient_email`.

## Exemple

Voici un exemple de l'utilisation de la fonction `send_email` pour envoyer un e-mail :

```python
subject = 'Test Email'
body = 'Ceci est un e-mail de test envoyé depuis Django.'
recipient_email = 'destinataire@example.com'

send_email(subject, body, recipient_email)
```

Cet exemple enverra un e-mail avec le sujet "Test Email" et le corps "Ceci est un e-mail de test envoyé depuis Django" à l'adresse e-mail "destinataire@example.com" en utilisant la configuration SMTP définie dans les paramètres `settings` de votre application Django.



# Classe `ForgotPasswordView`

La classe `ForgotPasswordView` est une vue basée sur la classe `APIView` de Django REST Framework qui permet aux utilisateurs de demander une réinitialisation de leur mot de passe en fournissant leur adresse e-mail.

## Méthode HTTP supportée

- `POST` : Cette vue prend en charge les requêtes HTTP de type `POST` pour demander une réinitialisation de mot de passe.

## Paramètres

Aucun paramètre n'est attendu dans le corps de la requête HTTP `POST`. Cependant, le corps de la requête doit contenir une clé `email` avec l'adresse e-mail de l'utilisateur souhaitant réinitialiser son mot de passe.

## Réponse HTTP

La vue renvoie les réponses HTTP suivantes :

- `200 OK` : Si la demande de réinitialisation de mot de passe a réussi et que l'e-mail de réinitialisation a été envoyé avec succès.
- `400 Bad Request` : Si le corps de la requête HTTP `POST` ne contient pas la clé `email` ou si elle est vide.
- `404 Not Found` : Si aucun utilisateur n'est trouvé avec l'adresse e-mail fournie dans la base de données.

## Utilisation

Pour demander une réinitialisation de mot de passe, vous devez envoyer une requête `POST` à l'URL associée à la vue `ForgotPasswordView` en incluant l'adresse e-mail de l'utilisateur dans le corps de la requête.

Lorsque la vue reçoit une requête avec une adresse e-mail valide, elle recherche l'utilisateur correspondant dans la base de données. Si l'utilisateur est trouvé, un nouveau token d'authentification est généré à l'aide de Django Knox (`AuthToken.objects.create(user=user)`). Ce token sera utilisé par l'utilisateur pour prouver son identité lors de la réinitialisation du mot de passe.

Ensuite, un e-mail est composé avec le sujet "Password Reset Request" et le corps "Hi {full_name},\n\nPlease use the following token to reset your password: {token}", où {full_name} est le nom complet de l'utilisateur et {token} est le token de réinitialisation généré. Cet e-mail est envoyé à l'adresse e-mail de l'utilisateur en utilisant la méthode `email_user` définie dans le modèle `User`.

Si la demande de réinitialisation de mot de passe a réussi, la vue renvoie une réponse HTTP `200 OK` avec un message indiquant que les instructions de réinitialisation de mot de passe ont été envoyées à l'adresse e-mail de l'utilisateur.

## Exemple

Voici un exemple de requête HTTP `POST` pour demander une réinitialisation de mot de passe :

```
POST /api/reset-password/
Content-Type: application/json

{
  "email": "utilisateur@example.com"
}
```



# Classe `ResetPasswordView`

La classe `ResetPasswordView` est une vue basée sur la classe `APIView` de Django REST Framework qui permet aux utilisateurs de réinitialiser leur mot de passe en fournissant un token valide et un nouveau mot de passe.

## Méthode HTTP supportée

- `POST` : Cette vue prend en charge les requêtes HTTP de type `POST` pour réinitialiser le mot de passe.

## Paramètres

La vue attend deux paramètres dans le corps de la requête HTTP `POST` :

1. `token` (str) : Le token de réinitialisation de mot de passe envoyé précédemment à l'utilisateur par e-mail lors de la demande de réinitialisation de mot de passe.
2. `new_password` (str) : Le nouveau mot de passe que l'utilisateur souhaite définir.

## Réponse HTTP

La vue renvoie les réponses HTTP suivantes :

- `200 OK` : Si la réinitialisation du mot de passe réussit et que le mot de passe de l'utilisateur est mis à jour avec succès.
- `400 Bad Request` : Si le corps de la requête HTTP `POST` ne contient pas les clés `token` ou `new_password`, ou si l'une de ces clés est vide.
- `404 Not Found` : Si le token de réinitialisation fourni n'est pas valide (c'est-à-dire qu'il ne correspond à aucun enregistrement dans la base de données).
- `400 Bad Request` : Si le token de réinitialisation a expiré et que l'utilisateur doit demander un nouveau token pour réinitialiser le mot de passe.

## Utilisation

Pour réinitialiser le mot de passe, vous devez envoyer une requête `POST` à l'URL associée à la vue `ResetPasswordView` en incluant le token de réinitialisation (`token`) et le nouveau mot de passe (`new_password`) dans le corps de la requête.

Lorsque la vue reçoit une requête avec un token valide et un nouveau mot de passe, elle recherche le token correspondant dans la base de données à l'aide de Django Knox (`AuthToken.objects.get(token_key=token)`). Si le token est trouvé et n'a pas expiré, le mot de passe de l'utilisateur associé au token est mis à jour avec le nouveau mot de passe fourni (`user.password = make_password(new_password)`). Ensuite, le token utilisé est invalidé en définissant sa date d'expiration (`expiry`) à une date antérieure (par exemple, la date d'hier) pour s'assurer qu'il ne puisse plus être utilisé.

Si la réinitialisation du mot de passe réussit, la vue renvoie une réponse HTTP `200 OK` avec un message indiquant que le mot de passe a été réinitialisé avec succès.

## Exemple

Voici un exemple de requête HTTP `POST` pour réinitialiser le mot de passe :

```
POST /api/reset-password/
Content-Type: application/json

{
  "token": "abcdef123456",
  "new_password": "nouveau_mot_de_passe"
}
```

Dans cet exemple, la vue recherchera un token de réinitialisation avec la clé "abcdef123456" dans la base de données. Si le token est trouvé et n'a pas expiré, le mot de passe de l'utilisateur associé au token sera mis à jour avec le nouveau mot de passe "nouveau_mot_de_passe". Le token utilisé sera également invalidé pour qu'il ne puisse plus être utilisé pour réinitialiser le mot de passe. Enfin, la vue renverra une réponse HTTP `200 OK` avec le message "Password has been successfully reset." pour indiquer que la réinitialisation du mot de passe a réussi.
