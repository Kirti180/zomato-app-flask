import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { OrdersService } from '../services/orders.service';

@Component({
  selector: 'app-orders',
  templateUrl: './orders.component.html',
  styleUrls: ['./orders.component.css']
})
export class OrdersComponent implements OnInit {
  orders: any[] = [];
  newOrder: any = {
    customer_name: '',
    items: []
  };

  constructor(private ordersService: OrdersService) { }

  ngOnInit(): void {
    this.getOrders();
  }

  getOrders(): void {
    this.ordersService.getOrders().subscribe(
      (response: any) => {
        this.orders = response;
      },
      (error: any) => {
        console.error('Error fetching orders:', error);
      }
    );
  }

  createOrder(orderForm: NgForm): void {
    if (orderForm.valid) {
      this.ordersService.createOrder(this.newOrder).subscribe(
        (response: any) => {
          console.log('Order created successfully:', response);
          this.getOrders();
          this.resetOrderForm(orderForm);
        },
        (error: any) => {
          console.error('Error creating order:', error);
        }
      );
    }
  }

  resetOrderForm(orderForm: NgForm): void {
    this.newOrder = {
      customer_name: '',
      items: []
    };
    orderForm.resetForm();
  }

  addItem(): void {
    this.newOrder.items.push({ dish_id: null, quantity: 1 });
  }

  removeItem(index: number): void {
    this.newOrder.items.splice(index, 1);
  }
}
