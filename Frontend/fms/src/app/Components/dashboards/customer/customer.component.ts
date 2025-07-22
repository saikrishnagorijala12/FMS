import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { StorageServicesService } from '../../../services/storage-services.service';
import {
  Customer,
  FranchiseLocation,
  JwtPayload,
  Orders,
  Product,
  ProductResponse,
  RawLocation,
  RawOrders,
} from '../../../services/interfaces';
import { CartService } from './cart.service';
import { CheckoutService } from './checkout.service';
import { jwtDecode } from 'jwt-decode';

@Component({
  selector: 'app-customer',
  imports: [CommonModule, FormsModule],

  templateUrl: './customer.component.html',
  styleUrl: './customer.component.css',
})
export class CustomerComponent {
  activeSection = signal<string>('locations');
  token: string | null = '';
  role: string = '';
  customer: Customer = {} as Customer;
  locations: FranchiseLocation[] = [];
  locationSearchTerm: string = '';
  products: Product[] = [];
  productSearchTerm: string = '';
  orders: Orders[] = [];
  filteredOrders: Orders[] = [];
  categories: string[] = [];
  selectedCategory = '';
  selectedPriceRange = '';
  filteredProducts: any[] = [];
  states: string[] = [];
  selectedState = '';
  selectedService = '';
  filteredLocations: FranchiseLocation[] = [];
  selectedOrderStatus: string = '';
  selectedTimeRange: string = '';
  selectedLocation: FranchiseLocation | null = null;
  orderStats = signal({
    total: 0,
    active: 0,
    totalSpent: 0,
  });
  selectedProduct: Product | null = null;
  productQuantity: number = 1;

  private http = inject(HttpClient);
  private router = inject(Router);
  private storageService = inject(StorageServicesService);
  constructor(
    public cartService: CartService,
    private checkoutService: CheckoutService
  ) { }

  ngOnInit() {
    this.checkToken();
    this.checkRole();
    this.clearCart();
    this.getCustomer();
    this.getLocations();
    this.getProducts();
    this.getOrders();
  }

  //API Calls needed

  getCustomer() {
    this.http
      .get<Customer>('http://127.0.0.1:5000/users/profile', {
        headers: this.getHeader(),
      })
      .subscribe({
        next: (response: Customer) => {
          this.customer = {
            user_id: response.user_id,
            name: response.name,
            email: response.email,
            phone_no: response.phone_no,
            role_id: response.role_id,
          };
          this.getAddress(this.customer.user_id);
          this.getPrefernce(this.customer.user_id);
          //console.log(this.customer);
        },
        error: (error) => {
          console.error('API Error:', error);
        },
      });
  }

  getAddress(customerId: number): void {
    this.http
      .get<any>(`http://127.0.0.1:5000/customers/${customerId}/address`, {
        headers: this.getHeader(),
      })
      .subscribe({
        next: (response: any) => {
          const addressData = Array.isArray(response) ? response[0] : response;
          this.customer = { ...this.customer, address: addressData.address };
        },
        error: (error) => {
          console.error('API Error:', error);
        },
      });
  }

  getPrefernce(customerId: number): void {
    this.http
      .get<any>(`http://127.0.0.1:5000/preferences/${customerId}`, {
        headers: this.getHeader(),
      })
      .subscribe({
        next: (response: any) => {
          const prefData = Array.isArray(response) ? response[0] : response;
          this.customer = {
            ...this.customer,
            preferences: prefData.preferences,
            emailNotifications: prefData.emailNotifications,
            smsNotifications: prefData.smsNotifications,
          };
          console.log(this.customer);
        },
        error: (error) => {
          console.error('API Error:', error);
        },
      });
  }

  getLocations() {
    this.http
      .get<RawLocation[]>('http://127.0.0.1:5000/franchise-locations', {
        headers: this.getHeader(),
      })
      .subscribe({
        next: (response: RawLocation[]) => {
          this.locations = response.map((item: RawLocation) => ({
            id: item.location_id,
            name: item.name,
            address: item.address,
            phone: item.phone,
            hours: item.hours,
            services: item.services,
            state: item.state,
          })) as any;
          const allStates = response.map((item: RawLocation) => item.state);
          this.states = Array.from(new Set(allStates));
          this.filteredLocations = [...this.locations];
        },
        error: (error) => {
          console.error('API Error:', error);
        },
      });
  }

  getProducts() {
    this.http
      .get<ProductResponse>('http://127.0.0.1:5000/products', {
        headers: this.getHeader(),
      })
      .subscribe({
        next: (response: ProductResponse) => {
          this.products = response.products;
          // console.log('Products from API:', this.products);
          const allCategories = this.products.map((p: any) => p.category);
          this.categories = Array.from(new Set(allCategories));
          this.filteredProducts = [...this.products];
        },
        error: (error) => {
          console.error('API Error:', error);
        },
      });
  }

  getOrders() {
    this.http
      .get<RawOrders[]>('http://127.0.0.1:5000/orders', {
        headers: this.getHeader(),
      })
      .subscribe({
        next: (response) => {
          this.orders = response.map((item: RawOrders) => ({
            id: item.id,
            date: item.date,
            location: item.location,
            items: item.items,
            status: item.status,
            total: item.total,
          }));
          this.filteredOrders = [...this.orders];
          // console.log(this.orders);
          const totalOrders = this.orders.length;
          const activeOrders = this.orders.filter(
            (o) => o.status !== 'delivered' && o.status !== 'completed'
          ).length;
          const totalSpent = this.orders.reduce((sum, o) => sum + o.total, 0);
          this.orderStats.set({
            total: totalOrders,
            active: activeOrders,
            totalSpent: totalSpent,
          });
          this.applyOrderFilters();
          // console.log('Orders:', this.orders);
          // console.log('Order Stats:', this.orderStats());
        },
        error: (error) => {
          console.error('API Error:', error);
        },
      });
  }

  updateDetails() {
    const pay_load_1 = {
      name: this.customer.name,
      phone_no: this.customer.phone_no,
      role_id: this.customer.role_id,
    };

    this.http
      .post('http://127.0.0.1:5000/users/profile', pay_load_1, {
        headers: this.getHeader(),
      })
      .subscribe({
        next: (response: any) => {
          // console.log(response)
          // alert("profile updated")
        },
        error: (err) => {
          console.error('API Error:', err);
        },
      });
  }

  updateAddress(customerId: any) {
    const pay_load_2 = {
      address: this.customer.address,
    };

    this.http
      .post(
        `http://127.0.0.1:5000/customers/${customerId}/address`,
        pay_load_2,
        {
          headers: this.getHeader(),
        }
      )
      .subscribe({
        next: (response: any) => {
          // console.log(response)
          // alert("Address updated")
        },
        error: (err) => {
          console.error('API Error:', err);
        },
      });
  }

  updatePreference(customerId: any) {
    //http://127.0.0.1:5000/preferences/13
    const pay_load_3 = {
      preferences: this.customer.preferences,
      emailNotifications: this.customer.emailNotifications,
      smsNotifications: this.customer.smsNotifications,
    };

    this.http
      .post(`http://127.0.0.1:5000/preferences/${customerId}`, pay_load_3, {
        headers: this.getHeader(),
      })
      .subscribe({
        next: (response: any) => {
          // console.log(response)
          // alert("prfernces updated")
        },
        error: (err) => {
          console.error('API Error:', err);
        },
      });
  }

  


  // Methods for calulation

  getHeader() {
    const headers = new HttpHeaders({
      Authorization: `Bearer ${this.token}`,
      'Content-Type': 'application/json',
    });
    return headers;
  }

  checkRole() {
    const tokenn: any = this.storageService.getItem('token');
    const decoded: any = jwtDecode<JwtPayload>(tokenn);
    this.role = decoded.role_id;

    if (this.role === '4') {
      this.router.navigate(['/franchisee']);
    } else if (this.role === '3') {
      this.router.navigate(['/franchisor']);
    }
  }

  checkToken() {
    this.token = this.storageService.getItem('token');
    if (!this.token) {
      this.router.navigate(['/login']);
      return;
    }
  }

  searchLocations(searchTerm: string) {
    const term = searchTerm.toLowerCase();
    this.filteredLocations = this.locations.filter(
      (loc) =>
        loc.name.toLowerCase().includes(term) ||
        loc.address.toLowerCase().includes(term)
    );
  }

  searchProducts(searchTerm: string) {
    const term = searchTerm.toLowerCase();
    this.filteredProducts = this.products.filter(
      (product) =>
        product.name.toLowerCase().includes(term) ||
        product.description.toLowerCase().includes(term) ||
        product.category.toLowerCase().includes(term)
    );
  }

  //product section sarts
  openProductDialog(product: Product) {
  this.selectedProduct = product;
  this.productQuantity = 1; // reset every time
}

closeProductDialog() {
  this.selectedProduct = null;
  this.productQuantity = 1;
}

confirmAddToCart() {
  if (!this.selectedProduct) return;
  this.cartService.addItem(this.selectedProduct, this.productQuantity);
  this.closeProductDialog();
}
  // Product Section End

  //cart section
  addToCart(product: any) {
    this.cartService.addItem(product);
    // alert(`${product.name} added to cart!`);
  }
  removeFromCart(id: number) {
    this.cartService.removeItem(id);
  }

  clearCart() {
    this.cartService.clearCart();
  }

  checkout() {
    const payload = this.cartService.getCartItemsForBackend();
    const token = localStorage.getItem('token');
    if (!token) {
      // alert('You need to log in first.');
      return;
    }
    this.checkoutService.checkout(payload, token).subscribe({
      next: (res) => alert(`Order placed: ${res.order_id}`),
      error: (err) => alert(`Failed: ${err.error?.message || err.message}`),
    });
  }

  setActiveSection(section: string) {
    this.activeSection.set(section);
  }

  viewLocationDetails(location: FranchiseLocation) {
    alert(`Viewing details for ${location.name}`);
  }

  trackOrder(order: Orders) {
    if (order.status === 'delivered') {
      alert(`Reordering ${order.id}`);
    } else {
      alert(`Tracking details for ${order.id} would be displayed here`);
    }
  }

  updateProfile() {
    this.updateDetails();
    this.updateAddress(this.customer.user_id);
    this.updatePreference(this.customer.user_id);
    alert('Profile updated successfully!');
  }

  applyFilters() {
    this.filteredProducts = this.products.filter((p: any) => {
      if (this.selectedCategory && p.category !== this.selectedCategory) {
        return false;
      }
      const price = p.price;
      if (this.selectedPriceRange === '0-10' && !(price >= 0 && price <= 10))
        return false;
      if (this.selectedPriceRange === '10-25' && !(price > 10 && price <= 25))
        return false;
      if (this.selectedPriceRange === '25-50' && !(price > 25 && price <= 50))
        return false;
      if (this.selectedPriceRange === '50+' && !(price > 50)) return false;

      return true;
    });
  }

  applyLocationFilters() {
    this.filteredLocations = this.locations.filter((loc: FranchiseLocation) => {
      if (this.selectedState && loc.state !== this.selectedState) {
        return false;
      }
      if (
        this.selectedService &&
        !loc.services.includes(this.selectedService)
      ) {
        return false;
      }

      return true;
    });
  }

  applyOrderFilters() {
    const now = new Date();
    this.filteredOrders = this.orders.filter((order) => {
      if (
        this.selectedOrderStatus &&
        order.status !== this.selectedOrderStatus
      ) {
        return false;
      }
      if (this.selectedTimeRange) {
        const days = parseInt(this.selectedTimeRange, 10);
        const orderDate = new Date(order.date); // Make sure API date is parseable
        const diffInMs = now.getTime() - orderDate.getTime();
        const diffInDays = diffInMs / (1000 * 60 * 60 * 24);
        if (diffInDays > days) {
          return false;
        }
      }

      return true;
    });
  }

  openDialog(location: any) {
    this.selectedLocation = location;
  }

  closeDialog() {
    this.selectedLocation = null;
  }

  trackByLocationId(index: number, location: FranchiseLocation) {
    return location.id;
  }

  logout() {
    localStorage.clear();
    this.router.navigate(['/login']);
  }
}
