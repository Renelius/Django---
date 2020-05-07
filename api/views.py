from django.shortcuts import render
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from rest_framework.response import Response
from bboard.models import Bd, Comment, Rubric
from .serializers import BdSerializer, BdDetailSerializer, CommentSerializer, RubricSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

'''These views provide API for working with ads, rubrics, comments
'''

@api_view(['GET','POST'])
@permission_classes((IsAuthenticated,))
def bbs(request):
    if request.method == 'GET':
        bbs = Bd.objects.all()[:10]
        serializer = BdSerializer(bbs, many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        serializer = BdSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

@api_view(['GET','DELETE','PUT','PATCH'])
@permission_classes((IsAuthenticated,))
def bbs_detail(request, bb_pk):
    bb=Bd.objects.get(pk=bb_pk)
    if request.method == 'GET':
        serializer = BdDetailSerializer(bb)
        return Response(serializer.data)
    elif request.method =='DELETE':
        bb.delete()
        return Response(status=HTTP_204_NO_CONTENT)
    elif request.method=='PUT' or request.method=='PATCH':
        serializer=BdSerializer(bb, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def comments(request, pk):
    bb=Bd.objects.get(pk=pk)
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    else:
        comments=Comment.objects.filter(bb=bb)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def api_rubrics(request):
    if request.method=='GET':
        rubrics=Rubric.objects.all()
        serializer = RubricSerializer(rubrics, many=True)
        return Response(serializer.data)
    if request.method =='POST':
        serializer=RubricSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes((IsAuthenticated,))
def api_rubrics_detail(request, pk):
    rubric=Rubric.objects.get(pk=pk)
    if request.method=='GET':
        serializer = RubricSerializer(rubric)
        return Response(serializer.data)
    elif request.method=='PUT' or request.method=='PATCH':
        serializer=RubricSerializer(rubric, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        rubric.delete()
        return Response(status=HTTP_204_NO_CONTENT)


def api_rubrics_check(request):
    return render(request, 'api/check_api_rubric.html')