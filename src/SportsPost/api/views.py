from django.db.models import Q
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from SportsPost.models import Question
from .pagination import StandardResultPagination
from  .serializers import SportsModelSerializer


class LikeToggleAPIView(APIView):
	permission_classes  = [permissions.IsAuthenticated]
	def get(self, request, pk, format=None):
		question_qs = Question.objects.filter(pk=pk)
		message = "Not allowed"
		if request.user.is_authenticated:
			is_liked = Question.objects.like_toggle(request.user, question_qs.first())
			return Response({'liked': is_liked})
		return Response({"message": message}, status=400)


class ReshareAPIView(APIView):
	permission_classes  = [permissions.IsAuthenticated]

	def get(self, request, pk, format=None):
		question_qs = Question.objects.filter(pk=pk)
		message = "Not allowed"
		if question_qs.exists() and question_qs.count() == 1:
			# if request.user.is_authenticated:
			new_question = Question.objects.reshare(request.user, question_qs.first())
			if new_question is not None:
				data = SportsModelSerializer(new_question).data 
				return Response(data)
			message = "Cannot share same sporst post daily"
		return Response({"message": message}, status=400)

class SportDetailAPIView(generics.ListAPIView):
	queryset = Question.objects.all()
	serializer_class	= SportsModelSerializer
	pagination_class    = StandardResultPagination
	permission_classes  = [permissions.AllowAny]

	def get_queryset(self, *args, **kwargs):
		sports_id = self.kwargs.get("pk")
		qs = Question.objects.filter(pk=sports_id)
		if qs.exists() and qs.count() == 1:
			parent_obj = qs.first()
			qs1 = parent_obj.get_children()
			qs = (qs | qs1).distinct().extra(select={"parent_id_null": 'parent_id IS NULL'})
		return qs.order_by("-parent_id_null", '-timestamp')


class SportCreateAPIView(generics.CreateAPIView):
	serializer_class	= SportsModelSerializer
	permission_classes  = [permissions.IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(user = self.request.user)

class SearchSportsAPIView(generics.ListAPIView):
	queryset            = Question.objects.all().order_by("-timestamp")
	serializer_class 	= SportsModelSerializer
	pagination_class    = StandardResultPagination

	def get_serializer_content(self, *args, **kwargs):
		context = super(SearchSportsAPIView, self).get_serializer_content(*args, **kwargs)
		context["request"] = self.request
		return context 

	def get_queryset(self,*args, **kwargs):
		qs = self.queryset
		query  = self.request.GET.get("q", None)	
		if query is not None:
			qs   = qs.filter(
							Q(content__icontains=query) |
							Q(user__username__icontains=query) 
						)
		return qs
		

class SportsListAPIView(generics.ListAPIView):
	serializer_class 	= SportsModelSerializer
	pagination_class    = StandardResultPagination

	def get_serializer_content(self, *args, **kwargs):
		context = super(SportsListAPIView, self).get_serializer_content(*args, **kwargs)
		context["request"] = self.request
		return context 

	def get_queryset(self,*args, **kwargs):
		requested_user = self.kwargs.get("username")
		if requested_user:
			qs   = Question.objects.filter(user__username=requested_user).order_by("-timestamp")

		else:
			im_following = self.request.user.profile.get_following()
			qs1	  = Question.objects.filter(user__in=im_following)
			qs2   = Question.objects.filter(user=self.request.user)
			qs    = (qs1 | qs2).distinct().order_by("-timestamp")

		query  = self.request.GET.get("q", None)	
		if query is not None:
			qs   = qs.filter(
							Q(content__icontains=query) |
							Q(user__username__icontains=query) 
						)
		return qs
		