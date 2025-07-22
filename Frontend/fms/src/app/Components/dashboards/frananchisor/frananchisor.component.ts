import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { StorageServicesService } from '../../../services/storage-services.service';
import { jwtDecode } from 'jwt-decode';
import { Applications, Customer, RawStocksRequests, Stocks } from '../../../services/interfaces';

@Component({
  selector: 'app-frananchisor',
  imports: [CommonModule, FormsModule],
  templateUrl: './frananchisor.component.html',
  styleUrl: './frananchisor.component.css'
})
export class FrananchisorComponent {
  activeSection = 'applications';
  token: string | null = '';
  franchisor: Customer = {} as Customer;
  role: string = '';
  applications: Applications[] = [];
  stockRequests: RawStocksRequests[] = [];
  products:Stocks[] =[];

  ngOnInit() {
    this.checkRole();
    this.checkToken();
    this.getUser();
    this.getApplications();
    this.getStocks();
    this.getProducts()
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
    const tokenn: any = this.storageService.getItem('token');
    const decoded: any = jwtDecode(tokenn);
    this.role = decoded.role_id;
    // console.log('Token : ', tokenn);
    // console.log('role : ', this.role);

    if (this.role === '2') {
      this.router.navigate(['/customer']);
    } else if (this.role === '4') {
      this.router.navigate(['/franchisee']);
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
          this.franchisor = {
            user_id: response.user_id,
            name: response.name,
            email: response.email,
            phone_no: response.phone_no,
            role_id: response.role_id,
          };

          console.log(this.franchisor);
        },
        error: (error) => {
          console.error(' USER API Error:', error);
        },
      });
  }

  getApplications() {
    this.http
      .get<Applications[]>('http://127.0.0.1:5000/franchises', {
        headers: this.getHeader(),
      })
      .subscribe({
        next: (response: Applications[]) => {
          this.applications = response;
          console.log('Applications:', this.applications);
        },
        error: err => {
          console.error('Applications API Error', err);
        }
      }
      );
  }

  getStocks() {
    this.http.get<RawStocksRequests[]>('http://127.0.0.1:5000/inventory/stock-requests', {
      headers: this.getHeader(),
    }).subscribe({
      next: (response: RawStocksRequests[]) => {
        this.stockRequests = response;
        console.log('Stock Requests:', this.stockRequests);
      },
      error: err => {
        console.error('Stocks API Error', err);
      }
    });
  }

  getProducts() {
    this.http.get<Stocks[]>('http://127.0.0.1:5000/orders/all', {
      headers: this.getHeader(),
    }).subscribe({
      next: (response: Stocks[]) => {
        this.products = response;
        console.log('Products:', this.products);
      },
      error: err => {
        console.error('Products API Error', err);
      }
    });
  }




















  // applications = [
  //   {
  //     id: 'APP-001',
  //     applicant: 'John Doe',
  //     region: 'California',
  //     investment: 50000,
  //     experience: '5 years retail',
  //     status: 'pending'
  //   },
  //   {
  //     id: 'APP-002',
  //     applicant: 'Jane Smith',
  //     region: 'Texas',
  //     investment: 75000,
  //     experience: '8 years business',
  //     status: 'pending'
  //   },
  //   {
  //     id: 'APP-003',
  //     applicant: 'Mike Johnson',
  //     region: 'New York',
  //     investment: 60000,
  //     experience: '3 years franchise',
  //     status: 'approved'
  //   }
  // ];

  // products = [
  //   {
  //     name: 'Premium Coffee Blend',
  //     price: 12.99,
  //     stock: 150,
  //     sales: 245
  //   },
  //   {
  //     name: 'Artisan Sandwich',
  //     price: 8.99,
  //     stock: 0,
  //     sales: 189
  //   },
  //   {
  //     name: 'Gourmet Pastry',
  //     price: 4.99,
  //     stock: 89,
  //     sales: 312
  //   }
  // ];




  // stockRequests = [
  //   {
  //     id: 'SR-001',
  //     franchise: 'Downtown Location',
  //     product: 'Premium Coffee Blend',
  //     quantity: 50,
  //     urgency: 'High'
  //   },
  //   {
  //     id: 'SR-002',
  //     franchise: 'Mall Location',
  //     product: 'Artisan Sandwich',
  //     quantity: 30,
  //     urgency: 'Medium'
  //   },
  //   {
  //     id: 'SR-003',
  //     franchise: 'Airport Location',
  //     product: 'Gourmet Pastry',
  //     quantity: 75,
  //     urgency: 'Low'
  //   }
  // ];

  commissionRate = 15;

  showSection(section: string) {
    this.activeSection = section;
  }

  approveApplication(appId: string) {
    alert(`${appId} has been approved!`);
  }
  rejectApplication(appId: string) {
    alert(`${appId} has been rejected!`);
  }

  addProduct() {
    alert('Add new product form would appear here.');
  }

  updateCommissionRate() {
    alert(`Commission rate updated to ${this.commissionRate}%`);
  }

  handleViewAction(action: string) {
    alert(`${action} functionality will be implemented here`);
  }

  logout() {
    localStorage.clear(); // or remove specific keys
    this.router.navigate(['/login']);
  }
}