from django.contrib.auth.mixins import UserPassesTestMixin #to check some properties for users

#i mixins sono utilizzati per restringere azioni ad alcuni utenti
class StaffMixin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_staff   #test che controlla se lo user è staff





