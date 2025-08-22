import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, HostListener, inject, signal } from '@angular/core';
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
import { TokenVerificationService } from '../../../services/token-verification.service';

@Component({
  selector: 'app-customer',
  imports: [CommonModule, FormsModule],

  templateUrl: './customer.component.html',
  styleUrl: './customer.component.css',
})
export class CustomerComponent {
  activeSection = signal<string>('locations');
  successMessage: string = '';
  errorMessage: string = '';
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
  selectedLocationId: number | null = null;
  dropdownOpen = false;
  shortName:string = '';


  private http = inject(HttpClient);
  private router = inject(Router);
  private storageService = inject(StorageServicesService);
  constructor(
    public cartService: CartService,
    private checkoutService: CheckoutService,
    private authService: TokenVerificationService
  ) { }

  ngOnInit() {
    this.checkToken();
    this.checkRole();
    this.clearCart();
    this.getCustomer();
    this.getOrders();
  }

  preferredLocationDialog = false;
  preferredLocation: FranchiseLocation | null = null;

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
          // Get address & preferences, but load locations after preferences
          this.getAddress(this.customer.user_id);
          this.getPrefernce(this.customer.user_id, () => {
            this.getLocations();
          });
          this.shortName = this.getShortName(this.customer.name);
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

  getPrefernce(customerId: number, callback?: () => void): void {
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
            preferredLocationId: prefData.preferredLocationId,
          };
          console.log('customer : ', this.customer);

          if (callback) callback();
        },
        error: (error) => {
          console.error('API Error:', error);
          if (callback) callback(); // still call even on error
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
            franchisee_id: item.franchisee_id,
            franchisee_user_id: item.franchisee_user_id,
            name: item.name,
            address: item.address,
            phone: item.phone,
            hours: item.hours,
            services: item.services,
            state: item.state,
          }));
          this.states = Array.from(new Set(response.map((i) => i.state)));
          this.filteredLocations = [...this.locations];
          if (this.customer.preferredLocationId) {
            const preferredLoc = this.locations.find(
              loc => loc.id === this.customer.preferredLocationId
            );
            if (preferredLoc) {
              this.selectedLocationId = preferredLoc.id;
              this.preferredLocation = preferredLoc;
              this.getProducts(preferredLoc.franchisee_id);
            }
          } else if (this.locations.length > 0) {
            // Fallback to first location
            this.selectedLocationId = this.locations[0].id;
            this.getProducts(this.locations[0].franchisee_id);
          }
        },
        error: (error) => console.error('API Error:', error),
      });
  }

  getProducts(franchisee_id: number) {
    this.http
      .get<any[]>(`http://127.0.0.1:5000/inventory/${franchisee_id}`, {
        headers: this.getHeader(),
      })
      .subscribe({
        next: (response: any[]) => {
          this.products = response.map((item) => ({
            id: item.product_id, // map API field to interface field
            name: item.product_name, // map API field to interface field
            description: item.description,
            price: item.price,
            rating: item.rating,
            reviews: item.reviews,
            category: item.category,
            franchisee_id: item.franchisee_id,
          })) as Product[];

          // console.log('Products from API:', this.products);


          const allCategories = this.products.map((p) => p.category);
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
        },
        error: (error) => {
          console.error('Orders API Error:', error);
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
          this.showMessage('Preferences Updated', 'success', true)
        },
        error: (err) => {
          console.error('API Error:', err);
          this.showMessage('Preferences Update Failed', 'failed', true)
        },
      });
  }

  updatePreference(customerId: number) {
    //http://127.0.0.1:5000/preferences/13
    const pay_load_3 = {
      preferences: this.customer.preferences,
      emailNotifications: this.customer.emailNotifications,
      smsNotifications: this.customer.smsNotifications,
      preferred_loc: this.customer.preferredLocationId
    };

    this.http
      .post(`http://127.0.0.1:5000/preferences/${customerId}`, pay_load_3, {
        headers: this.getHeader(),
      })
      .subscribe({
        next: (response: any) => {
          console.log(response)
          console.log(pay_load_3)
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
    const newToken: any = this.storageService.getItem('token');
    const decoded: any = jwtDecode<JwtPayload>(newToken);
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

  getShortName(name:string) : string{
    if (!name) return '';
  const index = name.indexOf(' ');
  return index === -1 ? name : name.substring(0, index);

  }

  showMessage(msg: string, type: string, reload: boolean = false) {
    window.scrollTo({ top: 0, behavior: 'smooth' });
    if (type === 'error') {
      this.errorMessage = msg;
      this.successMessage = '';
    }
    if (type === 'success') {
      this.successMessage = msg;
      this.errorMessage = '';
    }
    setTimeout(() => {
      this.errorMessage = '';
      this.successMessage = '';
      if (reload) {
        window.location.reload();
      }

    }, 3000);
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
    this.showMessage('Product Added to the cart', 'success');
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
    const cartItems = this.cartService.getItems();
    if (cartItems.length === 0) {
      this.showMessage('Your cart is empty', 'error', true);
      return;
    }

    const franchisee_id = cartItems[0].franchisee_id;
    const total_amount = this.cartService.getTotal();

    const pay_load_checkout = {
      order_display_id: `ORD-${Date.now()}`, // or let backend generate
      franchisee_id: franchisee_id,
      total_amount: total_amount,
      delivery_address: this.customer.address,
      status_id: 1, // pending
      items: cartItems.map((item) => ({
        product_id: item.id,
        quantity: item.quantity,
        price: item.price,
      })),
    };

    const token = localStorage.getItem('token');
    if (!token) return;

    this.checkoutService.checkout(pay_load_checkout, token).subscribe({
      next: (res) => {
        this.showMessage(
          `Order placed successfully (Order ID: ${res.order_id})`,
          'success',
          true
        );
        this.clearCart();
      },
      error: (err) => {
        this.showMessage(
          `Failed to place order: ${err.error?.message || err.message}`,
          'error'
        );
      },
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
    // alert('Profile updated successfully!');
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

  //Selected a base location

  setPreferredLocation(location: FranchiseLocation) {
    this.preferredLocation = location;
    this.preferredLocationDialog = false;
    console.log('preferef loc ', this.preferredLocation.id);
    this.getProducts(this.preferredLocation.id);
    this.customer.preferredLocationId = location.id;
    this.updatePreference(this.customer.user_id);
    this.showMessage(`Preferred location set to ${location.name}`, 'success');
  }
  clearPreferredLocation() {
    this.preferredLocation = null;
    this.showMessage('Preferred location cleared', 'info', true);
  }

  onLocationChange(event: any) {
    const selectedId = Number(event.target.value);
    const selectedLoc = this.locations.find((loc) => loc.id === selectedId);
    if (selectedLoc) {
      this.selectedLocationId = selectedLoc.id;
      this.getProducts(selectedLoc.franchisee_id);
      this.customer.preferredLocationId = selectedLoc.id;
      this.updatePreference(this.customer.user_id);
    }
  }



  // Toggle dropdown visibility
  toggleDropdown() {
    this.dropdownOpen = !this.dropdownOpen;
  }

  // Optional: Close when clicking outside
  @HostListener('document:click', ['$event'])
  onDocumentClick(event: MouseEvent) {
    const target = event.target as HTMLElement;
    if (!target.closest('.dropdown')) {
      this.dropdownOpen = false;
    }
  }
}
