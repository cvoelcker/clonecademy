class CourseView(APIView):
    """
    Contains all code related to viewing and saving courses.
    :author: Claas Voelcker
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (
        custom_permissions.IsModOrAdminOrReadOnly,)

    def get(self, request, course_id=None, format=None):
        """
        Returns a course if the course_id exists. The course, it's
        modules and questions are serialized.

        :author: Claas Voelcker
        :param request: request object containing auth token and user id
        :param course_id: the id of the required course
        :param format: unused (inherited)
        :return: a response containing the course serialization
        """

        # if no course id is given, the method was called wrong
        if not course_id:
            return Response({'ans': 'Method not allowed'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        try:
            # fetch the course object, serialize it and return 
            # the serialization
            course = Course.objects.get(id=course_id)
            course_serializer = serializers.CourseSerializer(course, context={
                'request': request})
            return Response(course_serializer.data,
                            status=status.HTTP_200_OK)
        # in case of an exception, throw a "Course not found" error for the 
        # frontend, packaged in a valid response with an error status code
        except Exception:
            return Response({'ans': 'Course not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request, course_id=None, format=None):
        """
        Saves a course to the database. If the course id is provided,
        the method updates an existing course, otherwise, a new course
        is created.

        :author: Tobias Huber, Claas Voelcker
        :param request: request containig the user and auth token
        :param course_id: optional: the course id 
                    (if a course is edited instead of created)
        :param format: unused (inherited)
        :return: a status response giving feedback about errors or a sucessful
                    database access to the frontend
        """
        
        data = request.data
        
        # checks whether the request contains any data
        if data is None:
            return Response({'error': 'Request does not contain data'},
                            status=status.HTTP_400_BAD_REQUEST)

        course_id = data.get('id')
        # Checks whether the name of the new course is unique
        if (course_id is None) and Course.objects.filter(
                name=data['name']).exists():
            return Response({'error': 'Course with that name exists'},
                            status=status.HTTP_409_CONFLICT)
        
        # adds the user of the request to the data
        if course_id is None:
            data['responsible_mod'] = request.user
        # if the course is edited, check for editing permission
        else:
            responsible_mod = Course.objects.get(id=course_id).responsible_mod
            # decline access if user is neither admin nor the responsible mod
            if (request.user.profile.is_admin()
                    or request.user == responsible_mod):
                data['responsible_mod'] = responsible_mod
            else:
                raise PermissionDenied(detail="You're not allowed to edit this"
                                       + "course, since you're not the"
                                       + 'responsible mod',
                                       code=None)

        # serialize the course
        course_serializer = serializers.CourseSerializer(data=data)
        
        # check for serialization errors
        if not course_serializer.is_valid():
            return Response({'error': course_serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # send the data to the frontend
        else:
            try:
                course_serializer.create(data)
                return Response({'success': 'Course saved'},
                                status=status.HTTP_201_CREATED)
            except ParseError as error:
                return Response({'error': str(error)},
                                status=status.HTTP_400_BAD_REQUEST)

