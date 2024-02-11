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
import logging

# A logger for possible monitoring of the error with catalog in the admin panel
logger = logging.getLogger(__name__)


# Implementation of data import
class ImportView(APIView):

    def post(self, request):

        data = request.data
        # A list for errors
        validation_errors = []

        # Validating data format
        # Due to JSON format, the data to be imported have to be a list
        if not isinstance(data, list):
            # Adding an error to the error list
            validation_errors.append({"error": "Invalid data format. Expected a list of objects."})
        else:
            for item in data:
                # Checking if the item in data is a dictionary
                # and that there is a single key
                if not isinstance(item, dict) or len(item) != 1:
                    validation_errors.append({"error": "Invalid data format for each item. Expected a dictionary "
                                                       "with a single key."})
                else:
                    # Name of the model should be in the first place in the dictionary
                    model_name = list(item.keys())[0]
                    if not isinstance(item[model_name], dict):
                        validation_errors.append({"error": "Invalid data format for model details. "
                                                           "Expected a dictionary."})

        # Saving data to the appropriate models
        for item in data:
            model_name = list(item.keys())[0]
            model_data = item[model_name]

            # For error handling
            try:
                model = globals()[model_name]
            except KeyError:
                validation_errors.append({"error": "Invalid model name"})
                continue

            try:
                # Special case for ProductAttributes to retrieve Product and Attribute instances
                # Otherwise there is an error because of foreign keys in model ProductAttributes
                if model_name == 'ProductAttributes':

                    product_id = model_data.pop('product')
                    attribute_id = model_data.pop('attribute')
                    # Getting ids of product and attribute
                    # Now instances of Product and Attribute are represented by the id
                    # Thus, import can be completed without an error
                    product_instance = Product.objects.get(id=product_id)
                    attribute_instance = Attribute.objects.get(id=attribute_id)

                    # Create or update ProductAttributes instance
                    product_attribute, created = ProductAttributes.objects.get_or_create(product=product_instance,
                                                                                         attribute=attribute_instance,
                                                                                         defaults=model_data)
                    if not created:
                        # Update existing instance if it's not created
                        for key, value in model_data.items():
                            setattr(product_attribute, key, value)
                        product_attribute.save()

                elif model_name == 'ProductImage':
                    # Special handling for ProductImage to retrieve Product instance
                    product_id = model_data.pop('product')
                    product_instance = Product.objects.get(id=product_id)
                    model_data['product'] = product_instance

                    # Create or update ProductImage instance
                    product_image, created = ProductImage.objects.get_or_create(id=model_data.get('id'),
                                                                                defaults=model_data)
                    if not created:
                        # Update existing instance if it's not created
                        for key, value in model_data.items():
                            setattr(product_image, key, value)
                        product_image.save()

                elif model_name == 'Catalog':
                    # Special case for Catalog to handle many-to-many relationships
                    products_ids = model_data.pop('products_ids', [])
                    attributes_ids = model_data.pop('attributes_ids', [])
                    # Retrieve or create the Catalog instance
                    catalog_instance, created = model.objects.get_or_create(id=model_data.get('id'),
                                                                            defaults=model_data)
                    # Set products_ids
                    # catalog_instance.products_ids.set(products_ids)
                    if products_ids:
                        catalog_instance.products_ids.set(products_ids)
                    # If attributes_ids were provided, set them
                    # Otherwise, keep existing attributes_ids
                    if attributes_ids:
                        catalog_instance.attributes_ids.set(attributes_ids)

                else:
                    # Create or update other models instances
                    # Thus, we can avoid unnecessary errors when importing the duplicates
                    model_instance, created = model.objects.get_or_create(id=model_data.get('id'), defaults=model_data)
                    if not created:
                        # Update existing instance if it's not created
                        for key, value in model_data.items():
                            setattr(model_instance, key, value)
                        model_instance.save()

            except Exception as e:
                logger.error(f"Error occurred during import: {e}")
                validation_errors.append({"error": str(e)})

        # Return response with validation errors, if any
        # By returning all the errors here, all the data that we want to import
        # that doesn't contain any errors, will be imported successfully
        # If any problems were encountered, only the data with error will not be imported
        if validation_errors:
            return Response({"errors": validation_errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Data imported successfully"}, status=status.HTTP_201_CREATED)


class DetailView(APIView):

    def get(self, request, model_name):

        # Here I rewrote extra selection to one dictionary
        # If another model is added, I can simply append the dictionary
        serializer_dict = {
            'Product': ProductSerializer,
            'Attribute': AttributeSerializer,
            'AttributeName': AttributeNameSerializer,
            'AttributeValue': AttributeValueSerializer,
            'Image': ImageSerializer,
            'Catalog': CatalogSerializer,
            'ProductImage': ProductImageSerializer,
            'ProductAttributes': ProductAttributesSerializer,
        }

        if model_name in serializer_dict:
            queryset = globals()[model_name].objects.all()
            serializer = serializer_dict[model_name](queryset, many=True)
            return Response(serializer.data)

        return Response({"error": "Invalid model name"}, status=status.HTTP_400_BAD_REQUEST)


class DetailItemView(APIView):

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