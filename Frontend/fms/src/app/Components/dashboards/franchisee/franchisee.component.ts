import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { Customer, InventoryItem, JwtPayload, Order_Response, OrderDisplay, OrderResponse, Sales } from '../../../services/interfaces';
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
  role:string='';
  token:string | null='';
  franchisee: Customer = {} as Customer;
  inventory: InventoryItem[] = [];
  orders: OrderDisplay[] = [];
  sales : Sales = {} as Sales;
  unPaidCommissions:number = 0;


  ngOnInit() {
    this.checkToken()
    this.checkRole();
    this.getUser()

    
  }

  private http = inject(HttpClient);
  private router = inject(Router);
  private storageService = inject(StorageServicesService);

  checkToken(){
    this.token = this.storageService.getItem('token');
    if (!this.token) {
      this.router.navigate(['/login']);
      return;
    }
  }

  checkRole(){
    const tokenn : any = this.storageService.getItem('token');
    const decoded: any = jwtDecode(tokenn);
    this.role = decoded.role_id;
    // console.log('Token : ', tokenn);
    // console.log('role : ', this.role);

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
        },
        error: (error) => {
          console.error(' USER API Error:', error);
        },
      });   
  }

  getInventory(userid: number) {
  this.http
    .get<any[]>(`http://127.0.0.1:5000/inventory/${userid}`, {
      headers: this.getHeader(),
    })
    .subscribe({
      next: (response: any[]) => {
        // Map backend response to desired format
        this.inventory = response.map(item => ({
          name: item.product_name,
          stock: item.quantity,
        })) as InventoryItem[];

        console.log(this.inventory);
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
          title: `Order #${o.order_id}`, // or o.order_display_id
          status: o.status
        }));
        console.log("orders : ", this.orders)
      },
      error: err => console.error('Error fetching orders', err),
    });
  }

  getSales(userId: number){
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

  getCommisions(userId: number){
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
  
  application = {
    region: ''
  };

  showSection(section: string) {
    this.activeSection = section;
  }

  requestStock(productName: string) {
    alert(`Stock request for ${productName} submitted!`);
  }

  updateOrderStatus(order: any) {
    if (order.status === 'Delivered') {
      alert('Viewing order details...');
    } else {
      order.status = 'Shipped'; // Simulate a status update
      alert('Status updated successfully!');
    }
  }

 

  payCommission() {
    alert('Commission paid successfully!');
  }

  submitApplication() {
    alert('Application submitted successfully!');
    this.application.region = '';
  }

  logout() {
    localStorage.clear(); // or remove specific keys
    this.router.navigate(['/login']);
  }
}