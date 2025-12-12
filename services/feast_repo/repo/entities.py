from feast import Entity

# TODO: définir l'entité principale "user"
user = Entity(
    name="user",               # TODO
    join_keys=["user_id"],        # TODO
    description="Identifie un utilisateur StreamFlow",        # TODO (en français)
)