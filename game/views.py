from graphviz import Digraph, Graph, nohtml
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import FormView, TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from .models import *
from .forms import *

@staff_member_required
def graph(request, edit=False):
    g = Digraph(format='svg')
    g.attr('node', shape='box')
    g.attr('graph', fontsize='20')
    if edit:
        g.attr('graph', rankdir='BT')

    with g.subgraph(name='cluster0') as c:
        for character in Character.objects.all():
            url = '/admin/game/character/{}/change/'.format(character.id)
            c.attr('node', url=url)
            c.node('C' + str(character.pk), character.title, href=url)

    for screen in Screen.objects.all():
        try:
            if screen.type.type == 10:
                color = 'yellow'
            if screen.type.type == 11:
                color = 'magenta'
            if screen.type.type == 20:
                color = 'green'
            if screen.type.type == 30:
                color = 'blue'
            if screen.type.type == 40:
                color = 'red'
            if screen.type.type == 50:
                color = 'orange'
        except:
            color = 'white'

        g.node(str(screen.id), screen.title, color=color, style='filled')

        if edit:
            url = reverse('admin:game_screen_change', args=[screen.id])
            g.node('edit{}'.format(screen.id), 'bewerken', fontsize='10', href=url, width='0', height='0')
            g.edge(str(screen.id), 'edit{}'.format(screen.id), arrowhead='none')

            url = reverse('add_screen', args=[screen.id])
            g.node('add{}'.format(screen.id), 'toevoegen', fontsize='10', href=url, width='0', height='0')
            g.edge(str(screen.id), 'add{}'.format(screen.id), arrowhead='none')

    for character in Character.objects.all():
        g.edge('C' + str(character.pk), str(character.first_screen.id))

    for route in Route.objects.all():
        g.edge(str(route.source.id), str(route.target.id), label=route.name)

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

class ChooseCharacterView(FormView):
    template_name = 'game/choose_character.html'
    form_class = ChooseCharacterForm

    def form_valid(self, form):
        self.request.session['screen_id'] = form.cleaned_data['character'].first_screen.id
        return redirect('game')

class GameView(FormView):
    template_name = 'game/game.html'

    def dispatch(self, request):
        screen_id = request.session.get('screen_id')
        try:
            self.screen = Screen.objects.get(id=screen_id)
        except Screen.DoesNotExist:
            return redirect('choose_character')
        return super().dispatch(request)

    def get_form(self):
        routes = self.screen.routes.all()
        return ChooseRouteForm(routes=routes)

    def form_valid(self, form):
        chosen_route = form.cleaned_data['route']
        self.request.session['screen_id'] = chosen_route.target.id
        return redirect('game')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        screen = self.screen
        context.update({
            'screen': screen,
        })
        return context
