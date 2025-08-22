import { Injectable } from '@angular/core';
import { CartItem } from '../../../services/interfaces';


@Injectable({ providedIn: 'root' })
export class CartService {
  private items: CartItem[] = [];

  getItems(): CartItem[] {
    return this.items;
  }

  //method to add item to checkout
  addItem(product: any, quantity: number = 1): void {
  const existing = this.items.find((i) => i.id === product.id);
  if (existing) {
    existing.quantity += quantity;
  } else {
    this.items.push({
      id: product.id,
      name: product.name,
      price: product.price,
      quantity: quantity,
      franchisee_id: product.franchisee_id
    });
  }
}

//methd to remove items from cart
  removeItem(productId: number) {
    this.items = this.items.filter(item => item.id !== productId);
  }

  //method to clear cart
  clearCart() {
    this.items = [];
  }

  //method to caluculate total
  getTotal(): number {
    return this.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  }

  //method to map to backend-friendly format
  getCartItemsForBackend(): { product_id: number; quantity: number }[] {
    return this.items.map(item => ({
      product_id: item.id,
      quantity: item.quantity,
      franchisee_id: item.franchisee_id
    }));
  }
}