from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.clickjacking import xframe_options_exempt

from .models import Glossary


# Create your views here.

class GlossaryView(View):

    @xframe_options_exempt
    def get(self, request):
        search = request.GET.get("q", None)
        if search is not None:
            query = search
            object_list = Glossary.objects.filter(
                Q(wordEn__icontains=query) | Q(wordEs__icontains=query)
            )

        else:
            object_list = None

        return render(
            request,
            'mentecobre/glossary.html',
            context={"object_list": object_list}
        )
