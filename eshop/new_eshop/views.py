"""
One of the main parts of a web applications.
Here we can see the response codes and decide whether everything worked as planned
or some mistakes have been made.
Besides, it also renders the templates if they exist.
"""
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import AttributeName, AttributeValue, Attribute, Image, Product, Catalog, ProductImage, ProductAttributes
from .serializers import (AttributeNameSerializer, AttributeValueSerializer, AttributeSerializer, ImageSerializer,
                          ProductSerializer, CatalogSerializer, ProductImageSerializer, ProductAttributesSerializer)


# Implementation of POST method
class ImportView(APIView):

    def post(self, request):
        data = request.data

        # Validating data format
        # It has to be a list of dictionaries because of JSON format
        if not isinstance(data, list):
            return Response({"error": "Invalid data format. Expected a list of objects."}, status=status.HTTP_400_BAD_REQUEST)

        for item in data:
            if not isinstance(item, dict) or len(item) != 1:
                return Response({"error": "Invalid data format for each item. Expected a dictionary with a single key."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Name of the model should be in the first place in the dictionary (index 0)
            model_name = list(item.keys())[0]
            if not isinstance(item[model_name], dict):
                return Response({"error": "Invalid data format for model details. Expected a dictionary."},
                                status=status.HTTP_400_BAD_REQUEST)

        # Saving data to the appropriate models
        for item in data:
            model_name = list(item.keys())[0]
            model_data = item[model_name]

            # For error handling
            try:
                model = globals()[model_name]
                product_id = model_data.get('id')
                product_instance, created = model.objects.get_or_create(id=product_id, defaults=model_data)

                # If the instance was not created because of unique constraint error,
                # the attributes of the instance are updated and the new instance is saved
                if not created:
                    # Updating the existing record with new data
                    for key, value in model_data.items():
                        setattr(product_instance, key, value)

                    product_instance.save()

            except KeyError:
                return Response({"error": "Invalid model name"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Data imported successfully"}, status=status.HTTP_201_CREATED)


# Implementation of GET method
class DetailView(APIView):

    # Getting information about instance by its name
    def get(self, request, model_name):

        if model_name == 'Product':
            queryset = Product.objects.all()
            serializer = ProductSerializer(queryset, many=True)
            return Response(serializer.data)

        elif model_name == 'Attribute':
            queryset = Attribute.objects.all()
            serializer = AttributeSerializer(queryset, many=True)
            return Response(serializer.data)

        elif model_name == 'AttributeName':
            queryset = AttributeName.objects.all()
            serializer = AttributeNameSerializer(queryset, many=True)
            return Response(serializer.data)

        elif model_name == 'AttributeValue':
            queryset = AttributeValue.objects.all()
            serializer = AttributeValueSerializer(queryset, many=True)
            return Response(serializer.data)

        elif model_name == 'Image':
            queryset = Image.objects.all()
            serializer = ImageSerializer(queryset, many=True)
            return Response(serializer.data)

        elif model_name == 'Catalog':
            queryset = Catalog.objects.all()
            serializer = CatalogSerializer(queryset, many=True)
            return Response(serializer.data)

        elif model_name == 'ProductImage':
            queryset = ProductImage.objects.all()
            serializer = ProductImageSerializer(queryset, many=True)
            return Response(serializer.data)

        elif model_name == 'ProductAttributes':
            queryset = ProductAttributes.objects.all()
            serializer = ProductAttributesSerializer(queryset, many=True)
            return Response(serializer.data)

        else:
            return Response({"error": "Invalid model name"}, status=status.HTTP_400_BAD_REQUEST)


class DetailItemView(APIView):
    # Getting information about a specific instance by its id
    def get(self, request, model_name, item_id):
        try:
            model = globals()[model_name]
            item = model.objects.get(id=item_id)
            serializer = globals()[f"{model_name}Serializer"](item)
            return Response(serializer.data)
        except KeyError:
            return Response({"error": "Invalid model name"}, status=status.HTTP_400_BAD_REQUEST)
        except model.DoesNotExist:
            return Response({"error": f"{model_name} with id {item_id} not found"}, status=status.HTTP_404_NOT_FOUND)