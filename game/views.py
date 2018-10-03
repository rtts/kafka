import random
from graphviz import Digraph, Graph, nohtml
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import FormView, TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import *
from .forms import *

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

def graph(request, edit=False):
    g = Digraph(format='svg')
    g.attr('node', shape='box')
    g.attr('graph', fontsize='20')
    g.attr('node', fontname='sans-serif')
    g.attr('edge', fontname='sans-serif')
    if edit:
        g.attr('graph', rankdir='BT')

    with g.subgraph(name='cluster0') as c:
        for character in Character.objects.all():
            c.node('C' + str(character.pk), character.title, color=character.color)

    for screen in Screen.objects.all():
        try:
            color = screen.type.color
            style = 'filled'
        except:
            color = 'black'
            style = ''

        title = '{}. {}'.format(screen.pk, screen.title)
        g.node(str(screen.id), title, color=color, style=style)

        if edit:
            url = reverse('admin:game_screen_change', args=[screen.id])
            g.node('edit{}'.format(screen.id), 'bewerken', fontsize='10', href=url, width='0', height='0')
            g.edge(str(screen.id), 'edit{}'.format(screen.id), arrowhead='none')

            url = reverse('add_screen', args=[screen.id])
            g.node('add{}'.format(screen.id), '+ route nieuw scherm', fontsize='10', href=url, width='0', height='0')
            g.edge(str(screen.id), 'add{}'.format(screen.id), arrowhead='none')

            url = reverse('add_existing_screen', args=[screen.id])
            g.node('add2{}'.format(screen.id), '+ route naar bestaand scherm', fontsize='10', href=url, width='0', height='0')
            g.edge(str(screen.id), 'add2{}'.format(screen.id), arrowhead='none')

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

        g.edge(str(route.source.id), str(route.target.id), label=label, color=color, fontcolor=color)

    return HttpResponse(g.pipe().decode('utf-8'))

@staff_member_required
def add_screen(request, source_id, target_id=None):
    source = get_object_or_404(Screen, id=source_id)
    if target_id:
        target = get_object_or_404(Screen, id=target_id)
    else:
        target = Screen()
        target.save()
    route = Route(source=source, target=target)
    route.save()
    return redirect('admin:game_screen_change', target.id)

class ExistingScreenView(FormView, StaffRequiredMixin):
    form_class = ChooseScreenForm
    template_name = 'game/choose_screen.html'

    def form_valid(self, form):
        screen_nr = form.cleaned_data['screen_nr']
        source_id = self.kwargs['source_id']
        source = get_object_or_404(Screen, id=source_id)
        target = get_object_or_404(Screen, id=screen_nr)
        route = Route(source=source, target=target)
        route.save()
        return redirect('graph')

class ChooseCharacterView(FormView):
    template_name = 'game/choose_character.html'
    form_class = ChooseCharacterForm

    def form_valid(self, form):
        character = form.cleaned_data['character']
        self.request.session['character_id'] = character.id
        self.request.session['screen_id'] = character.first_screen.id
        return redirect('game')

class GameView(FormView):
    template_name = 'game/game.html'

    def dispatch(self, request):
        character_id = request.session.get('character_id')
        screen_id = request.session.get('screen_id')
        try:
            self.character = Character.objects.get(id=character_id)
            self.screen = Screen.objects.get(id=screen_id)
        except (Character.DoesNotExist, Screen.DoesNotExist):
            return redirect('choose_character')
        return super().dispatch(request)

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
                route = random.choice(routes)
                self.request.session['screen_id'] = route.target.id
        except:
            pass
        return redirect('game')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        screen = self.screen
        routes = self.get_routes()

        context.update({
            'screen': screen,
            'routes': routes,
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
