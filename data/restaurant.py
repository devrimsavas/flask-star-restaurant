from datetime import date
from datetime import datetime 

class Food:
    def  __init__(self, food_name,food_price):
        self.food_name=food_name
        self.food_price=food_price

    def update_food_price(self,new_price):
        self.food_price=new_price
        return self.food_price
        


class Restaurant:

    def  __init__(self,rest_name):
        
            self.rest_name=rest_name
            self.menu=[]


    def add_an_food_to_menu(self,food_to_add):
        self.menu.append(food_to_add)
        return self.menu

    def remove_food_from_menu(self,food_to_remove):
        for food_item in self.menu: 
            if food_item.food_name==food_to_remove:
                self.menu.remove(food_item)
                return f"{food_to_remove} removed from menu"
        return f"{food_to_remove} not found in menu"
        
        
        return self.menu
   
    def display_menu(self):
        menu_data=[]
        total_menu_price=0

        for counter,item in enumerate(self.menu,start=1):
            menu_data.append({
                "item_number":counter,
                "food_name":item.food_name,
                "food_price":item.food_price
            })
            total_menu_price+=item.food_price

        return  {
            "restaurant_name":self.rest_name,
            "menu_items":menu_data,
            "total_price":total_menu_price
        }

class Customer:
    def  __init__(self,name):
        self.name=name
        self.order=[]

    def place_order(self,restaurant,item_no,quantity):
        sum_total=0
        if item_no<1 or item_no>len(restaurant.menu):
            print('INVALID SELECTION')
            return

        item=restaurant.menu[item_no-1]
        total_price=item.food_price*quantity
        self.order.append((item,quantity,total_price))
        print(f' Customer: {self.name}\n{item.food_name}x {quantity}={total_price}')


    def take_out_item_from_order(self,out_item):
        
        if out_item<1 or out_item>len(self.order):
            print('INVALID SELECTION')
            return
        item=self.order[out_item-1]
        price=item.food_price*1
        print(f' Customer: {self.name}\n{item.food_name} x  1 unit={price} removed from order')
        self.order.remove((item,1,price))

    def cancel_order(self):
        if not self.order:
            print(f'{self.name } has not any orders yet')
            return

        print(f'{self.name}, current order: ')
        for i, (item,quantity,price) in enumerate(self.order,start=1):
            print(f'{i}. {item.food_name} x {quantity} ={price}')

        item_no=int(input('ENTERthe item number to cancel :'))
        if item_no<1 or item_no>len(self.order):
            print('Invalid selection')
            return
        item,quantity,price=self.order[item_no-1]

        if (item,quantity,price) in self.order:
            #self.order.remove((item,1,item.food_price))
            self.order.remove((item,quantity,price))
        
            #print(f'{item.food_name} x 1={item.food_price} has been removed')
            print(f'{item.food_name} x {quantity}={price} has been removed')
            #company_sales.total_sales-=item.food_price
            company_sales.total_sales-=price

        else:
            print('ITEM NOT FOUND IN ORDER')
            
class SaleBook:
    def  __init__(self,restaurant_name):
        self.restaurant_name=restaurant_name
       
        self.record_book=[]
        self.total_sales=0

    def add_record_to_book(self,new_entry):
        customer_name=new_entry[0]
        for i in range(len(self.record_book)):
            if customer_name in self.record_book[i][0]:
                print('already opened')
                return
            
        self.record_book.append((new_entry[0],new_entry[1]))
        self.total_sales+=new_entry[1]

    def show_record_book(self):
        counter=0
        show_text=""
        total_sales=0
        for item in self.record_book:
            
            print(item[0],item[1])
            total_sales+=item[1]

        print(f'total sales : {total_sales}')
#END OF CLASSES 

def add_food_to_menu(restaurant):
    while True:
        ask=input('Do you want to add a new item to the menu (y/n)')
        if ask=='y':
            new_item=input('ENTER THE NAME OF THE NEW ITEM:   ')

            try:
                new_item_price=int(input('ENTER THE PRICE OF THE NEW ITEM: '))
            except ValueError:
                print('Invalid Price. Please enter an integer value')
                continue
            restaurant.add_an_food_to_menu(Food(new_item,new_item_price))

        elif ask=='n':
            print('Returning to main menu.  ')
            break
        else:
            print('INVALID SELECTION')
def remove_food_from_menu(restaurant):
    restaurant.display_menu()
    item_no=int(input('Which food will be removed from menu ? '))
    if item_no<=0 or item_no>len(restaurant.menu):
        print('INVALID SELECTION')
        return
    
    restaurant.menu.remove(restaurant.menu[item_no-1])

def update_food_price(restaurant):
    restaurant.display_menu()
    item_no=int(input('Which food item would you like to update?  '))
    new_price=int(input(f'Enter the new price for {restaurant.menu[item_no-1].food_name}: '))
    restaurant.menu[item_no-1].update_food_price(new_price)
    print(f'{restaurant.menu[item_no-1].food_name} price updated to {new_price}')
                               
customers=[]   
def take_orders(restaurant):
    today=date.today()
    receipt_date=today.strftime('%d/%m/%Y')
    now=datetime.now()
    current_hour_12h=now.strftime('%I')
   
    restaurant.display_menu()
    customer_name=input('THE NAME OF THE CUSTOMER? ')
    
    customer=Customer(customer_name)
    customers.append(customer)
    
    while True:
        item_no=int(input('Enter the item number to order (0 to finish)'))
        if item_no==0:
            break
        quantity=int(input('ENTER THE QUANTITY:  '))
        customer.place_order(restaurant,item_no,quantity)
    print(f' {customer.name} ordered:')
    sum_total=0
    sum_text=""
    for item,quantity,price in customer.order:
        print(f'{item.food_name} x {quantity}= {price}')
        sum_text+=f'{item.food_name} x {quantity}={price}\n'
        sum_total+=price
    company_sales.add_record_to_book((customer.name,sum_total))

    receipt_text=f"""{restaurant.rest_name}
------------------------------------------------------

Customer Name: {customer.name}    date: {receipt_date} time: {current_hour_12h}
------------------------------------------------------


{sum_text}

TOTAL AMOUNT:    {sum_total}
------------------------------------------------------
"""
    print(receipt_text)

    receipt_demand=input('do you want receipt (y/n ?')
    if receipt_demand=='y':
    
        filename=customer_name+'.txt'

        try:

            f=open(filename,'x')
            f.write(receipt_text)
            f.close
        except FileExistsError:
            print('Error writing File.')
            filename=customer_name+'1'+'.txt'
        
        
    elif receipt_demand=='n':
        print('Thanks for saving the World')

    else:
        print('invalid selection ')
        return 
def cancel_order_1(restaurant):

    for customer in customers:
        print(customer.name)

    
    customer_name=input('Enter Customer Name:')
    for customer in customers:
        
        if customer.name==customer_name:
            if not customer.order:
                print(f'{customer.name } has not any orders yet')
                return

            print(f'{customer.name}, current order: ')
            for i, (item,quantity,price) in enumerate(customer.order,start=1):
                print(f'{i}. {item.food_name} x {quantity} ={price}')

            item_no=int(input('ENTER the item number to cancel :'))
            if item_no<1 or item_no>len(customer.order):
                print('Invalid selection')
                return
            item,quantity,price=customer.order[item_no-1]
            print(f'{item.food_name} x 1={item.food_price} has been removed')
            #customer.order.remove((item,1,item.food_price))
            customer.order.pop(item_no-1)
            customer_total_sum=sum([order[2] for order in customer.order])
            print(f'Customer {customer.name} total sum: {customer_total_sum}')
            
            return

    print(f'Customer {customer_name} not found')

def show_menu():
    your_restaurant.display_menu()
    
#restaurants first menu

def your_first_menu(restaurant):

# Create the food items
    burger = Food('Burger', 10)
    pizza = Food('Pizza', 12)
    fried_chicken = Food('Fried Chicken', 9)
    spaghetti = Food('Spaghetti', 11)
    salad = Food('Salad', 8)
    lasagna=Food('Lasagna',15)
    Sushi=Food('Sushi',20)
    Tacho=Food('Tacho',19)

# Add the food items to the menu
    restaurant.add_an_food_to_menu(burger)
    restaurant.add_an_food_to_menu(pizza)
    restaurant.add_an_food_to_menu(fried_chicken)
    restaurant.add_an_food_to_menu(spaghetti)
    restaurant.add_an_food_to_menu(salad)
    restaurant.add_an_food_to_menu(lasagna)
    restaurant.add_an_food_to_menu(Sushi)
    restaurant.add_an_food_to_menu(Tacho)


#MAIN LOOP
your_restaurant=Restaurant('STAR RESTAURANT')
company_sales=SaleBook(your_restaurant)

your_first_menu(your_restaurant)
game=True
selection=""

