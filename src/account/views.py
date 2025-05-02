from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.


@api_view(["GET"])
def hello(request) -> Response:
    name = request.GET.get("name")
    if name is None:
        return Response("hello coaie")
    else:
        return Response(f"hello {name}")


@api_view(["GET"])
def hello_dedication(request, dedication: str) -> Response:
    return Response(f"hello fratele {dedication}")
