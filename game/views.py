import random
from graphviz import Digraph, Graph, nohtml
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import FormView, TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import UserPassesTestMixin
from kafka.utils import get_webtext
from .models import *
from .forms import *

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

def graph(request):
    g = Digraph(format='svg')
    g.attr('node', shape='box')
    g.attr('graph', fontsize='20')
    g.attr('node', fontname='sans-serif')
    g.attr('edge', fontname='sans-serif')

    with g.subgraph(name='cluster0') as c:
        for character in Character.objects.all():
            url = reverse('admin:game_character_change', args=[character.id])
            c.node('C' + str(character.pk), character.title, color=character.color, href=url)

    for screen in Screen.objects.all():
        try:
            color = screen.type.color
        except:
            color = 'white'

        view_url = reverse('screen', args=[screen.id])
        edit_url = reverse('admin:game_screen_change', args=[screen.id])
        add_url = reverse('add_route', args=[screen.id])
        title = '''<

<table bgcolor="{}" border="1" cellspacing="10" color="black">
  <tr>
    <td colspan="3" align="left" border="0"><b>{}. {}</b></td>
  </tr>
  <tr>
    <td href="{}"><font point-size="10">bekijk scherm</font></td>
    <td href="{}"><font point-size="10">bewerk scherm</font></td>
    <td href="{}"><font point-size="10">+ nieuwe route</font></td>
  </tr>
</table>

        >'''.format(color, screen.id, screen.title, view_url, edit_url, add_url)
        g.node(str(screen.id), title, shape='plaintext', width='0', height='0')

    for character in Character.objects.all():
        g.edge('C' + str(character.pk), str(character.first_screen.id), color=character.color)

    for route in Route.objects.all():
        color = 'black'
        label = route.name
        first_loop = True

        for character in route.applies_to.all():
            if first_loop:
                first_loop = False
                label = 'Alleen van toepassing op:\n' + character.title
                color = character.color
            else:
                label += ', ' + character.title
                color += ':' + character.color

        url = reverse('add_route', args=[route.target.id])
        g.edge(str(route.source.id), str(route.target.id), label=label, color=color, fontcolor=color, href=url)

    return HttpResponse(g.pipe().decode('utf-8'))

class AddRouteView(FormView, StaffRequiredMixin):
    form_class = ChooseScreenForm
    template_name = 'game/add_route.html'

    def form_valid(self, form):
        screen_nr = form.cleaned_data.get('screen_nr')
        source_id = self.kwargs['source_id']
        source = get_object_or_404(Screen, id=source_id)
        if screen_nr:
            target = get_object_or_404(Screen, id=screen_nr)
            route = Route(source=source, target=target)
            route.save()
            return redirect('graph')
        else:
            type = ScreenType.objects.get(type=40)
            target = Screen(type=type)
            target.save()
            route = Route(source=source, target=target)
            route.save()
            return redirect('admin:game_screen_change', target.id)

class TitleScreenView(TemplateView):
    template_name = 'game/title_screen.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        screen_id = self.request.session.get('screen_id')
        context.update({
            'emoji': Emoji.objects.filter(visible=True),
            'content': get_webtext(50),
            'continue': screen_id,
            'footer': get_webtext(100),
        })
        return context

class ChooseCharacterView(FormView):
    template_name = 'game/choose_character.html'
    form_class = ChooseCharacterForm

    def form_valid(self, form):
        character = form.cleaned_data['character']
        self.request.session['character_id'] = character.id
        self.request.session['screen_id'] = character.first_screen.id
        return redirect('character')

class CharacterView(TemplateView):
    template_name = 'game/character.html'

    def dispatch(self, request, *args, **kwargs):
        character_id = request.session.get('character_id')
        try:
            self.character = Character.objects.get(id=character_id)
        except (Character.DoesNotExist, Screen.DoesNotExist):
            return redirect('choose_character')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'character': self.character,
        })
        return context

class GameView(FormView):
    template_name = 'game/game.html'

    def dispatch(self, request, *args, **kwargs):
        character_id = request.session.get('character_id')
        screen_id = request.session.get('screen_id')
        try:
            self.character = Character.objects.get(id=character_id)
            self.screen = Screen.objects.get(id=screen_id)
        except (Character.DoesNotExist, Screen.DoesNotExist):
            return redirect('title_screen')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        if self.screen.type.type == 11:
            try:
                routes = self.get_routes()
                route = random.choice(routes)
                self.request.session['screen_id'] = route.target.id
                return redirect('game')
            except:
                pass
        return super().get(request)

    def get_form(self):
        routes = self.screen.routes.all()
        return ChooseRouteForm(routes=routes, **self.get_form_kwargs())

    def form_valid(self, form):
        chosen_route = form.cleaned_data['route']
        routes = self.get_routes()
        try:
            if chosen_route in routes:
                self.request.session['screen_id'] = chosen_route.target.id
            elif self.screen.type.type != 10:
                self.request.session['screen_id'] = random.choice(routes).target.id
        except:
            pass
        return redirect('game')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        screen = self.screen
        routes = self.get_routes()

        if screen.background_color:
            background_color = screen.background_color.color
        elif screen.location and screen.location.background_color:
            background_color = screen.location.background_color.color
        elif screen.type and screen.type.background_color:
            background_color = screen.type.background_color.color
        else:
            background_color = 'white'

        if screen.foreground_color:
            foreground_color = screen.foreground_color.color
        elif screen.location and screen.location.foreground_color:
            foreground_color = screen.location.foreground_color.color
        elif screen.type and screen.type.foreground_color:
            foreground_color = screen.type.foreground_color.color
        else:
            foreground_color = 'white'

        if screen.image:
            background_image = screen.image.url
        elif screen.location and screen.location.image:
            background_image = screen.location.image.url
        else:
            background_image = 'none'

        context.update({
            'screen': screen,
            'routes': routes,
            'background_color': background_color,
            'foreground_color': foreground_color,
            'background_image': background_image,
        })
        return context

    def get_routes(self):
        routes = []
        for route in self.screen.routes.all():
            applies_to = list(route.applies_to.all())
            if applies_to:
                if self.character in applies_to:
                    routes.append(route)
            else:
                routes.append(route)
        return routes

class GameScreenView(GameView):
    def get(self, request, screen_id):
        request.session['screen_id'] = screen_id
        return redirect('game')
