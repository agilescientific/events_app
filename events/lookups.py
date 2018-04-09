from ajax_select import register, LookupChannel
from .models import User, EventRegistration

@register('users')
class UsersLookup(LookupChannel):

    model = User

    def check_auth(self, request):
        if request.user.is_authenticated :
            return True

    def get_query(self, q, request):
        return self.model.objects.filter(first_name__icontains=q).order_by('first_name')[:10]

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.username