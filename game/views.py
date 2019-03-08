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

@staff_member_required
def graph(request):
    g = Digraph(format='svg')
    g.attr('node', shape='box')
    g.attr('graph', fontsize='20')
    g.attr('node', fontname='sans-serif')
    g.attr('edge', fontname='sans-serif')

    for screen in Screen.objects.all():
        try:
            color = screen.type.color
        except:
            pass
        if not color:
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

    for route in Route.objects.all():
        color = 'black'
        label = str(route) if route.name else ''
        penwidth = '2'
        if route.conditions.exists():
            only_enabled_if = ', '.join([str(c.only_enabled_if) for c in route.conditions.all()])
            label = 'Condities: {}'.format(only_enabled_if)
            penwidth = '5'
            color = 'red'

        url = reverse('admin:game_route_change', args=[route.id])
        g.edge(str(route.source.id), str(route.target.id), label=label, color=color, fontcolor=color, href=url, penwidth=penwidth)

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

class GameView(FormView):
    template_name = 'game/game.html'

    def dispatch(self, request, *args, **kwargs):
        if 'chosen_routes' not in request.session:
            self.request.session['chosen_routes'] = []
        screen_id = request.session.get('screen_id')
        try:
            self.screen = Screen.objects.get(id=screen_id)
        except Screen.DoesNotExist:
            self.screen = Screen.objects.filter(type__type=5).first()
            request.session['screen_id'] = self.screen.id
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

        if not routes:
            return redirect('game')

        if chosen_route in routes:
            self.request.session['screen_id'] = chosen_route.target.id
            self.request.session['chosen_routes'] += [chosen_route.id]
        elif self.screen.type.type != 10:
            self.request.session['screen_id'] = random.choice(routes).target.id
        return redirect('game')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        screen = self.screen
        routes = self.get_routes()

        if screen.background_color:
            background_color = screen.background_color.color
        elif screen.type and screen.type.background_color:
            background_color = screen.type.background_color.color
        else:
            background_color = 'white'

        if screen.foreground_color:
            foreground_color = screen.foreground_color.color
        elif screen.type and screen.type.foreground_color:
            foreground_color = screen.type.foreground_color.color
        else:
            foreground_color = 'white'

        if screen.text_color:
            text_color = screen.text_color.color
        else:
            text_color = 'black'

        if screen.image:
            background_image = screen.image.url
        else:
            background_image = 'none'

        if screen.image_desktop:
            background_image_desktop = screen.image_desktop.url
        else:
            background_image_desktop = None

        if screen.audio:
            audio = screen.audio.url
            loop = screen.loop
        elif screen.type and screen.type.audio:
            audio = screen.type.audio.url
            loop = screen.type.audio.loop
        else:
            audio = False
            loop = False

        context.update({
            'screen': screen,
            'routes': routes,
            'background_color': background_color,
            'foreground_color': foreground_color,
            'text_color': text_color,
            'background_image': background_image,
            'background_image_desktop': background_image_desktop,
            'audio': audio,
            'loop': loop,
        })
        return context

    def get_routes(self):
        routes = []
        for route in self.screen.routes.all():
            if route.conditions.exists():
                enabled = False
                for condition in route.conditions.all():
                    if condition.only_enabled_if.id in self.request.session['chosen_routes']:
                        enabled = True
                        break
                if enabled:
                    routes.append(route)
            else:
                routes.append(route)
        print(routes)
        return routes

class GameScreenView(TemplateView):
    def get(self, request, screen_id):
        request.session['chosen_routes'] = []
        request.session['screen_id'] = screen_id
        return redirect('game')

class ResetView(TemplateView):
    def get(self, request):
        del request.session['screen_id']
        return redirect('game')
