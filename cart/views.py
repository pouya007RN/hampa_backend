from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from cart.serializers import *
from accounts.models import Profile


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @action(detail=True, methods=['post', 'put'])
    def add_to_cart(self, request, pk=None):
        """Add an item to a user's cart"""

        cart = Cart.objects.filter(owner=request.user).first()
        if not cart:
            cart = Cart(owner=request.user)
            cart.save()

        try:
            product = Product.objects.get(pk=request.data['product_id'])
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if product.count <= 0:
            json = {'message': "There's no product available!"}
            return Response(json, status=status.HTTP_400_BAD_REQUEST)

        existing_cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        # before creating a new cart item check if it is in the cart already
        # and if yes increase the quantity of that item
        if existing_cart_item:

            try:
                existing_cart_item.quantity = int(request.data.get('count'))
                existing_cart_item.save()
            except TypeError:
                return Response({'error': 'please enter count'})

        else:

            existing_cart_item = CartItem(cart=cart, product=product, quantity=1)
            existing_cart_item.save()
                
        # Disallow adding to cart if available inventory is not enough
        if product.count - existing_cart_item.quantity == -1:
            existing_cart_item.quantity -= 1
            existing_cart_item.save()
            json = {'message': "There's no more product available!"}
            return Response(json, status=status.HTTP_400_BAD_REQUEST)

        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=True, methods=['post', 'put'])
    def reduce_from_cart(self, request, pk=None):
        """Reduce the quantity of an item in the user's cart by one"""
        cart = Cart.objects.filter(owner=request.user).first()
        try:
            product = Product.objects.get(pk=request.data['product_id'])
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # if removing an item where the quantity is 1, remove the cart item
        # completely otherwise decrease the quantity of the cart item
        if cart_item.quantity == 1:
            cart_item.delete()
        else:
            cart_item.quantity -= 1
            cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=True, methods=['post', 'put'])
    def remove_from_cart(self, request, pk=None):
        """Remove a product from the user's cart"""
        cart = Cart.objects.filter(owner=request.user).first()
        try:
            product = Product.objects.get(pk=request.data['product_id'])
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

        cart_item.delete()

        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False)
    def retrieve_cart(self, request):
        """Return a user's cart"""

        cart = Cart.objects.filter(owner=request.user).first()
        serializer = CartSerializer(cart, many=False)

        return Response(serializer.data)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        """Override the creation of Order objects."""
        user = self.request.user
        cart = user.cart

        for cart_item in cart.cart_items.all():
            if cart_item.product.count - cart_item.quantity < 0:
                raise serializers.ValidationError(
                    'We do not have enough inventory of ' + str(cart_item.product.title) + \
                    ' to complete your purchase. Sorry, we will restock soon'
                )

        try:
            address_id = int(self.request.data.get('address_id'))
        except TypeError:
            return Response({'Message': 'address_id is required!'})

        try:
            address_obj = Address.objects.get(pk=address_id)
        except Exception as e:
            print(e)
            json = {'message': "No address with the given id exists!"}
            return Response(json, status=status.HTTP_400_BAD_REQUEST)

        order_cost = 0
        for c in cart.cart_items.all():
            order_cost += int(c.product.price) * c.quantity

        profile = Profile.objects.filter(user=user).first()
        if order_cost > profile.credit:
            return Response({'Message': 'Insufficient Credit!'})
        else:
            profile.credit -= order_cost
            profile.save()

        order = Order(owner=user, address=address_obj, total=order_cost, status=False)
        order.save()

        order_items = []
        for cart_item in cart.cart_items.all():
            order_items.append(OrderItem(order=order, product=cart_item.product, quantity=cart_item.quantity))
            # available_inventory should decrement by the appropriate amount
            cart_item.product.count -= cart_item.quantity
            cart_item.product.save()
            seller = cart_item.product.owner
            seller_profile = Profile.objects.filter(user=seller).first()
            seller_profile.credit += (int(cart_item.product.price) * cart_item.quantity)
            seller_profile.save()

        OrderItem.objects.bulk_create(order_items)
        # use clear instead of delete since it removes all objects from the
        # related object set. It does not delete the related objects it just
        # disassociates them, which is what we want in order to empty the cart
        # but keep cart items in the db for customer data analysis
        cart.cart_items.clear()
        return Response({'Message': 'Your order is submitted successfully!'})

    @action(detail=False)
    def order_history(self, request):
        """Return a list of a user's orders"""
        user = self.request.user
        orders = Order.objects.filter(owner=user)
        serializer = OrderSerializer(orders, many=True)

        return Response(serializer.data)

    @action(detail=False)
    def retrieve_sales_record(self, request):
        """Return a list of a producer's sales record"""
        seller = self.request.user
        sales_record = []
        order_items = OrderItem.objects.filter(product__owner=seller)
        for order in Order.objects.all():
            json = {'order_items': [o for o in order_items if o.order == order]}
            if len(json['order_items']) != 0:
                buyer = order.owner
                json['username'] = buyer.username
                json['first_name'] = buyer.first_name
                json['last_name'] = buyer.last_name
                json['phone_number'] = buyer.phone_number
                json['address'] = AddressSerializer(order.address).data
                json['profile_image'] = str(buyer.profile.image)
                json['created_at'] = order.created_at
                json['order_items'] = OrderItemSerializer(json['order_items'], many=True).data
                sales_record.append(json)

        return Response(sales_record)
    
    @action(detail=True, methods=['post', 'put'])
    def change_order_status(self, request, pk=None):
        id_list = request.data['order_id_list']
        changed_status = request.data['status']
        order_items = OrderItem.objects.filter(pk__in=id_list)
        for order_item in order_items:
            if changed_status == 1:
                order_item.status = True
            else:
                order_item.status = False
            order_item.save()

        order = order_items[0].order
        flag = True
        for o in order.order_items.all():
            if not o.status:
                flag = False
        if flag:
            order.status = True
        else:
            order.status = False
        order.save()

        json = {'Message': "Status changed successfully!"}
        return Response(json, status=status.HTTP_200_OK)

    @action(detail=False)
    def retrieve_popular_products(self, request):
        """Return a list of products that have been ordered the most"""
        product_dic = {}
        for p in Product.objects.all():
            product_dic[p] = 0

        for o in OrderItem.objects.all():
            product_dic[o.product] += o.quantity

        serializer = ProductSerializer(sorted(product_dic, key=product_dic.get, reverse=True), many=True)
        return Response(serializer.data)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
