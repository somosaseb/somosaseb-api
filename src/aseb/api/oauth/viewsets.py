from oauth2_provider import views


class AuthorizationView(views.AuthorizationView):
    ...


class TokenView(views.TokenView):
    ...


class RevokeTokenView(views.RevokeTokenView):
    ...


class IntrospectTokenView(views.IntrospectTokenView):
    ...


class AuthorizedTokenDeleteView(views.AuthorizedTokenDeleteView):
    ...


class AuthorizedTokensListView(views.AuthorizedTokensListView):
    ...
