import { Injectable } from '@angular/core';

export interface CartItem {
  id: number;
  name: string;
  price: number;
  quantity: number;
}

@Injectable({ providedIn: 'root' })
export class CartService {
  private items: CartItem[] = [];

  getItems(): CartItem[] {
    return this.items;
  }

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
    });
  }
}

  removeItem(productId: number) {
    this.items = this.items.filter(item => item.id !== productId);
  }

  clearCart() {
    this.items = [];
  }

  getTotal(): number {
    return this.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  }

  // ✅ NEW METHOD: map to backend-friendly format
  getCartItemsForBackend(): { product_id: number; quantity: number }[] {
    return this.items.map(item => ({
      product_id: item.id,
      quantity: item.quantity
    }));
  }
}