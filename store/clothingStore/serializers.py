from rest_framework import serializers
from .models import *



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate(self , data):    
        if(Category.objects.filter(name=data['name']).exists()):
            raise serializers.ValidationError(f"Sorry, category '{data['name']}' already exists.")
        return data




class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset=Category.objects.all() , slug_field='name' , allow_null=True , required=False)
    class Meta:
        model = Product
        fields = '__all__'

    # If the comination of name & size exists, then I update the current object's stock, otherwise the current stock is 1.
    def create_or_update_product(name , size):
        try:
            existingProduct = Product.objects.get(name=name, size=size)
            existingProduct.stock += 1
            existingProduct.save()
            return existingProduct
        
        except Product.DoesNotExist:
            new_product = Product(name=name, size=size)
            new_product.stock = 1
            new_product.save()
            return new_product
        

    def validate(self , data):
        if(Product.objects.filter(name=data['name'] , size=data['size'] , category=data['category'])).exists():
            raise serializers.ValidationError(f"Sorry, product '{data['name']}' with size '{data['size']}' and category '{data['category']}' already exists.")
        return data
    
    def validate_category(self , value):
        if(value == None):
            raise serializers.ValidationError(f"Must select a category.")
        return value


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.PrimaryKeyRelatedField(queryset = Product.objects.all() , source='product' , write_only=True)

    class Meta:
        model = CartItem
        fields = ['id' , 'product_name' , 'quantity' , 'size']

    def validate(self , data):
        product = data['product']
        quantity = data['quantity']
        size = data['size']
        name = product.name

        try:
            product = Product.objects.get(name=name , size=size)
        except:
            raise serializers.ValidationError(f"Sorry, {name} does not contain any {size} size.")
            
        if(quantity > product.stock):
            piece = 'pieces' if product.stock > 1 or product.stock == 0 else 'piece'
            raise serializers.ValidationError(f"Sorry, {name} contains only {product.stock} {piece}.")

        return data
    

  
    # DELETE BUTTON GIA NA SBHNW OLA TA ORDER ITEMS
    def create(self , validated_data):
        product = validated_data['product']
        size = validated_data['size']
        name = product.name
        product = Product.objects.get(name=name , size=size)
        quantity = validated_data['quantity']
        product.stock -= quantity
        product.save()
        
        try:
            cart_item = CartItem.objects.get(product=product , size=size)
            cart_item.quantity += quantity
            cart_item.save()
            return cart_item
        
        except CartItem.DoesNotExist:
            cart_item = CartItem(product=product , size=size)
            cart_item.quantity = quantity
            cart_item.save()
            return cart_item
     
        




        



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'