import { CommonModule } from '@angular/common';
import { Component, HostListener, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { Customer, InventoryItem, JwtPayload, Order_Response, OrderDetails, OrderDisplay, OrderResponse, Sales } from '../../../services/interfaces';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { StorageServicesService } from '../../../services/storage-services.service';
import { jwtDecode } from 'jwt-decode';

@Component({
  selector: 'app-franchisee',
  imports: [CommonModule, FormsModule],
  templateUrl: './franchisee.component.html',
  styleUrl: './franchisee.component.css'
})
export class FranchiseeComponent {

  activeSection: string = 'inventory';
  user: string = 'test';
  role: string = '';
  token: string | null = '';
  franchisee: Customer = {} as Customer;
  inventory: InventoryItem[] = [];
  orders: OrderDisplay[] = [];
  sales: Sales = {} as Sales;
  unPaidCommissions: number = 0;
  successMessage: string = '';
  errorMessage: string = '';
  processedCommissions = 0;
  shortName: string = '';
  dropdownOpen = false;
  franchiseAnalytics: any;


  //manage inventory
  filteredInventory: InventoryItem[] = [];

  // Filters
  searchTerm: string = '';
  selectedCategory: string = '';
  selectedStock: string = '';

  categories: string[] = [];

  //stock request 
  showStockDialog = false;
  selectedProduct = '';
  currentStock = 0;
  requestQuantity = 1;
  selectedUrgency = 'Medium';
  requestNotes = '';
  productID = 0;

  //update Status
  selectedStatus = 1;
  showStatusDialog = false;
  order_id = 1;

  //commissions Dialouge
  showCommissionsDialog = false;

  //view customer orders
  viewOrderDialouge = false;
  selectedOrderDetails: OrderDetails | any = null;
  viewOrderLoading: boolean = false;
  orderDetails: OrderDetails[] = [];


  ngOnInit() {
    this.checkToken()
    this.checkRole();
    this.getUser()
    this.getOrders()
  }

  private http = inject(HttpClient);
  private router = inject(Router);
  private storageService = inject(StorageServicesService);

  checkToken() {
    this.token = this.storageService.getItem('token');
    if (!this.token) {
      this.router.navigate(['/login']);
      return;
    }
  }

  checkRole() {
    const newToken: any = this.storageService.getItem('token');
    const decoded: any = jwtDecode(newToken);
    this.role = decoded.role_id;
    if (this.role === '2') {
      this.router.navigate(['/customer']);
    } else if (this.role === '3') {
      this.router.navigate(['/franchisor']);
    }
  }

  getHeader() {
    const headers = new HttpHeaders({
      Authorization: `Bearer ${this.token}`,
      'Content-Type': 'application/json',
    });
    return headers;
  }

  getUser() {
    this.http
      .get<Customer>('http://127.0.0.1:5000/users/profile', {
        headers: this.getHeader(),
      })
      .subscribe({
        next: (response: Customer) => {
          this.franchisee = {
            user_id: response.user_id,
            name: response.name,
            email: response.email,
            phone_no: response.phone_no,
            role_id: response.role_id,
          };
          console.log(this.franchisee);
          this.getInventory(this.franchisee.user_id);
          this.getOrdersByUser(this.franchisee.user_id);
          this.getSales(this.franchisee.user_id);
          this.getCommisions(this.franchisee.user_id);
          this.shortName = this.getShortName(this.franchisee.name);
          this.loadFranchiseAnalytics(this.franchisee.user_id)
        },
        error: (error) => {
          console.error(' USER API Error:', error);
        },
      });
  }

  loadFranchiseAnalytics(userid: number) {
    this.http
      .get<any[]>(`http://127.0.0.1:5000/reports/franchise/${userid}`, {
        headers: this.getHeader(),
      })
      .subscribe({
        next: (data) => {
          this.franchiseAnalytics = data;
          console.log(this.franchiseAnalytics);
        },
        error: (error) => {
          console.error('Error loading analytics:', error);
          alert('unable to fetch products');
        },
      });
  }

  getInventory(userid: number) {
    this.http
      .get<any[]>(`http://127.0.0.1:5000/inventory/franchisee/${userid}`, {
        headers: this.getHeader(),
      })
      .subscribe({
        next: (response: any[]) => {
          this.inventory = response.map(item => ({
            id: item.product_id,
            name: item.product_name,
            stock: item.quantity,
            category:item.category,
            price:item.price,
          })) as InventoryItem[];

          console.log(this.inventory);
          this.categories = [...new Set(this.inventory.map(i => i.category))];

        this.filteredInventory = [...this.inventory];
        },
        error: (error) => {
          console.error('INVENTORY API Error:', error);
          alert('unable to fetch products');
        },
      });
  }

  getOrdersByUser(userId: number) {
    this.http.get<Order_Response[]>(`http://127.0.0.1:5000/orders/${userId}`, {
      headers: this.getHeader(),
    }).subscribe({
      next: (response: Order_Response[]) => {
        this.orders = response.map(o => ({
          order_id: o.id,
          title: `Order #${o.order_id}`,
          status: o.status
        }));
        console.log("orders : ", this.orders)
      },
      error: err => console.error('Error fetching orders', err),
    });
  }

  getOrders() {
    this.http
      .get<OrderDetails[]>('http://127.0.0.1:5000/orders/orders', {
        headers: this.getHeader(),
      })
      .subscribe({
        next: (data) => {
          this.orderDetails = data;
          console.log(this.orderDetails);
        },
        error: (error) => {
          console.error('Orders API Error:', error);
        },
      });
  }

  getSales(userId: number) {
    this.http
      .get<Sales>(`http://127.0.0.1:5000/sales/${userId}`, {
        headers: this.getHeader(),
      })
      .subscribe({
        next: (response: Sales) => {
          this.sales = {
            totalSales: response.totalSales,
            totalRevenue: response.totalRevenue,
            commissionPaid: response.commissionPaid,
            withdrawnEarnings: response.withdrawnEarnings,
          };

          console.log(this.sales);
        },
        error: (error) => {
          console.error('SALES API Error:', error);
        },
      });
  }

  getCommisions(userId: number) {
    this.http
      .get<any>(`http://127.0.0.1:5000/sales/${userId}/unpaid`, {
        headers: this.getHeader(),
      })
      .subscribe({
        next: (response: any) => {
          this.unPaidCommissions = response.total_unpaid_amount;
          console.log(this.unPaidCommissions);
        },
        error: (error) => {
          console.error('pending commissions API Error:', error);
        },
      });
  }

  getOrderById(orderId: number) {
    this.viewOrderDialouge = true;
    this.http
      .get<OrderDetails>(`http://127.0.0.1:5000/orders/order/${orderId}`, {
        headers: this.getHeader(),
      })
      .subscribe({
        next: (order: OrderDetails) => {
          console.log('Order Details:', order);
          this.selectedOrderDetails = order;
        },
        error: (error) => {
          console.error('Failed to fetch order details:', error);
          alert('Unable to fetch deatials')
        },
      });
  }

  sendStockRequest(payload: any, header: any) {
    this.http
      .post('http://127.0.0.1:5000/inventory/stock-request', payload, { headers: header })
      .subscribe({
        next: (response) => {
          console.log('Statud Update request submitted successfully:', response)
          this.showSuccess("Stock request submitted successfully");
          setTimeout(() => {
            window.location.reload();
          }, 3000);
        },
        error: (err) => {
          console.error('Error submitting stock request:', err);
          this.showError('Failed to submit Stock request. Please try again.');
        }
      });
  }

  sendupdatedStatus(order_id: number, payload: any, header: any) {
    this.http
      .put(`http://127.0.0.1:5000/orders/${order_id}/status`, payload, { headers: header })
      .subscribe({
        next: (response) => {
          console.log('Stock request submitted successfully:', response)
          this.showSuccess("Status Update request submitted successfully");
          setTimeout(() => {
            window.location.reload();
          }, 3000);
        },
        error: (err) => {
          console.error('Error submitting stock request:', err);
          alert('Unable to fetch deatials')
          this.showError('Failed to submit Status Update request. Please try again.');
        }
      });
  }

  application = {
    applicant: '',
    region: '',
    investment: 0,
    experience: '',
    status: 1,
  };

  showSection(section: string) {
    this.activeSection = section;
  }
  getShortName(name: string): string {
    if (!name) return '';
    const index = name.indexOf(' ');
    return index === -1 ? name : name.substring(0, index);

  }
  //drop Down for log out
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

  showSuccess(msg: string) {
    this.successMessage = msg;
    this.errorMessage = '';

    setTimeout(() => {
      this.successMessage = '';
    }, 3000);
  }

  showError(msg: string) {
    this.errorMessage = msg;
    this.successMessage = '';

    setTimeout(() => {
      this.errorMessage = '';
    }, 3000);
  }

  payCommission() {
    alert('Commission paid successfully!');
  }

  submitApplication() {
    alert('Application submitted successfully!');
    this.application.region = '';
  }

  applyFilters() {
    this.filteredInventory = this.inventory.filter(item => {
      const matchesSearch =
        !this.searchTerm ||
        item.name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
        item.category.toLowerCase().includes(this.searchTerm.toLowerCase());

      const matchesCategory =
        !this.selectedCategory || item.category === this.selectedCategory;

      const matchesStock =
        !this.selectedStock ||
        (this.selectedStock === 'low' && item.stock < 10) ||
        (this.selectedStock === 'in' && item.stock > 0) ||
        (this.selectedStock === 'out' && item.stock === 0);

      return matchesSearch && matchesCategory && matchesStock;
    });
  }

  logout() {
    localStorage.clear(); // or remove specific keys
    this.router.navigate(['/login']);
  }

  //Stock Request Dialouge Box

  openStockRequestDialog(product_id: number, productName: string, stock: number): void {
    this.selectedProduct = productName;
    this.currentStock = stock;
    this.productID = product_id
    this.showStockDialog = true;
  }

  closeDialog(): void {
    this.showStockDialog = false;
    this.showStatusDialog = false;
    this.showCommissionsDialog = false;
    this.resetForm();
    this.viewOrderDialouge = false;
  }

  submitRequest(): void {
    if (this.requestQuantity >= 1) {
      const pay_load = {
        franchisee_id: this.franchisee.user_id,
        product_id: this.productID,
        quantity: this.requestQuantity,
        urgency: this.selectedUrgency,
        status_id: 1
      };
      this.sendStockRequest(pay_load, this.getHeader())
      console.log('Stock request submitted:', pay_load);
      alert(`Stock request submitted successfully!\nProduct: ${this.selectedProduct}\nQuantity: ${this.requestQuantity}\nUrgency: ${this.selectedUrgency}`);

      this.closeDialog();
    }
  }

  // Status Dialouge Box
  updateStatus() {
    const pay_load = {
      status_id: this.selectedStatus
    };
    this.sendupdatedStatus(this.order_id, pay_load, this.getHeader())
    console.log("New Status2 :", this.selectedStatus);
    this.closeDialog();
  }

  openupdateStatusDialog(order_id: number) {
    this.showStatusDialog = true;
    this.order_id = order_id;
    console.log("order Id", order_id);
    console.log("New Status :", this.selectedStatus);
  }

  openViewOrderDetails(order_id: number) {
    this.viewOrderLoading = true;

    // Find the order in the already loaded array
    const foundOrder = this.orderDetails.find(o => o.order_id === order_id);
    if (foundOrder) {
      this.selectedOrderDetails = foundOrder;
      this.viewOrderDialouge = true;
    } else {
      console.warn(`Order with ID ${order_id} not found in orderDetails list.`);
    }
  }

  //Commissions Dialog Handler
  updatecommissions() {
    this.processedCommissions = this.unPaidCommissions;
    this.unPaidCommissions = 0;
    this.closeDialog();
  }

  openPayCommissionDialouge() {
    this.showCommissionsDialog = true;
  }

  //Reset Form
  resetForm(): void {
    this.requestQuantity = 1;
    this.selectedUrgency = 'Medium';
    this.requestNotes = '';
    this.selectedStatus = 1;
  }
}