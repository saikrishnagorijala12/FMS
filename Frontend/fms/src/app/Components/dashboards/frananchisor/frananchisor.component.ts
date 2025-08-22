import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, HostListener, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { StorageServicesService } from '../../../services/storage-services.service';
import { jwtDecode } from 'jwt-decode';
import { Applications, Customer, Products, RawStocks, RawStocksRequests } from '../../../services/interfaces';
import { BoldPipe } from "../../../custom_pipe/bold.pipe";

@Component({
  selector: 'app-frananchisor',
  imports: [CommonModule, FormsModule],
  templateUrl: './frananchisor.component.html',
  styleUrl: './frananchisor.component.css'
})
export class FrananchisorComponent {

  //Base Setting of the application
  activeSection = 'applications';
  successMessage: string = '';
  errorMessage: string = '';
  token: string | null = '';
  franchisor: Customer = {} as Customer;
  role: string = '';
  applications: Applications[] = [];
  stockRequests: RawStocksRequests[] = [];
  products: Products[] = [];
  filteredStockRequests: RawStocksRequests[] = [];
  selectedStatus: string = '';
  statusOptions: string[] = [];
  shortName: string = '';
  dropdownOpen = false;
  applicationSearchTerm = '';
  selectedState = '';
  selected_Status = '';
  filteredApps: any[] = [];
  productSearchTerm = '';
  selectedCategory = '';
  filteredProducts: Products[] = [];
  categories: string[] = [];
  stockSearchTerm: string = '';
  selectedStockStatus: string = '';
  selectedStockUrgency: string = '';
  statusStockOptions: string[] = [];
  urgencyOptions: string[] = [];
  reports: any;

  //Application Dialouge box
  selectedApplication: any = null;
  showAppDetails = false;
  showRejectDetails = false;
  showAcceptDetails = false;
  productid = 0;
  commissionRate = 15;

  //Products 
  //Add Product
  showAddpProduct = false;
  newProduct = {
    user_id: 0,
    name: '',
    price: 0,
    description: '',
    category: '',
    stock: 0
  };

  //Update Stock
  newStock = 0;
  showUpdateStock = false;
  product_id = 0;

  //Update Price
  newPrice = 0;
  showUpdateprice = false;

  // Delete Product
  showDeleteProduct = false;

  //Accept stock reuest
  requestid = 0;
  productName = '';
  productQuantity = 0;
  showAcceptStockRequest = false;
  showRejectStockRequest = false;
  showStockDetails = false;
  selectedStock: any = null;


  ngOnInit() {
    this.checkRole();
    this.checkToken();
    this.getUser();
    this.getApplications();
    this.getStocks();
    this.loadReports();
  }

  private http = inject(HttpClient);
  private router = inject(Router);
  private storageService = inject(StorageServicesService);

  // API CALLS

  //API Call to get all the user information 
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
          this.getProducts(this.franchisor.user_id)
          this.shortName = this.getShortName(this.franchisor.name);

          console.log(this.franchisor);
        },
        error: (error) => {
          console.error(' USER API Error:', error);
        },
      });
  }

  // API call to get all the APllication requests from franchisee's to franchisor
  getApplications() {
    this.http
      .get<Applications[]>('http://127.0.0.1:5000/franchises', {
        headers: this.getHeader(),
      })
      .subscribe({
        next: (response: Applications[]) => {
          this.applications = response;
          console.log('Applications:', this.applications);
          this.filteredApps = [...this.applications];
        },
        error: err => {
          console.error('Applications API Error', err);
        }
      }
      );
  }

  //API Call to get all the stock request by Franchisee to the franchisor
  getStocks() {
    this.http.get<RawStocksRequests[]>('http://127.0.0.1:5000/inventory/stock-requests', {
      headers: this.getHeader(),
    }).subscribe({
      next: (response) => {
        this.stockRequests = response;
        this.filteredStockRequests = [...response];
        this.statusOptions = [...new Set(response.map(r => r.status_name))];
        this.statusStockOptions = [...new Set(response.map(r => r.status_name))];
        this.urgencyOptions = [...new Set(response.map(r => r.urgency))];
        this.applyFilters();
        console.log('Stock Requests:', this.stockRequests);
      },
      error: err => {
        console.error('Stocks API Error', err);
      }
    });
  }

  //API call to get all the products in stock by the franchisor id

  getProducts(franchisor_id: number) {
    this.http.get<{ products: RawStocks[] }>(`http://127.0.0.1:5000/stocks/${franchisor_id}`, {
      headers: this.getHeader(),
    }).subscribe({
      next: (response) => {
        this.products = response.products.map((item: RawStocks) => ({
          id: item.product_id,
          name: item.name,
          price: item.price,
          stock_quantity: item.stock_quantity,
          category: item.category
        }));
        this.filteredProducts = [...this.products];
        this.categories = [...new Set(this.products.map(p => p.category))]
          .sort((a, b) => a.localeCompare(b));
        console.log('Products:', this.products);
      },
      error: err => {
        console.error('Products API Error', err);
      }
    });
  }


  // API call to either approve or reject the Application Status
  sendupdatedStatus(app_id: number, payload: any, header: any) {
    this.http
      .put(`http://127.0.0.1:5000/franchises/${app_id}/status`, payload, { headers: header })
      .subscribe({
        next: (response) => {
          console.log('Stock request submitted successfully:', response)
          this.showMessage("Status Update request submitted successfully", 'success');
          window.scrollTo({ top: 0, behavior: 'smooth' });
          setTimeout(() => {
            window.location.reload();
          }, 3000);
        },
        error: (err) => {
          console.error('Error submitting stock request:', err);
          this.showMessage('Failed to submit Status Update request. Please try again.', 'error');
        }
      });
  }

  // API to create a product
  AddProduct(payload: any, header: any) {
    this.http
      .post('http://127.0.0.1:5000/stocks/add', payload, { headers: header })
      .subscribe({
        next: (response) => {
          console.log('Product Added Sucessfully', response)
          this.showMessage("Product Added Sucessfully", 'success');
          window.scrollTo({ top: 0, behavior: 'smooth' });
          setTimeout(() => {
            window.location.reload();
          }, 3000);
        },
        error: (err) => {
          console.error('Error Adding New Product : ', err);
          this.showMessage('Failed to Add New Product. Please try again.', 'error');
        }
      });
  }

  // API to update the stock of a product
  updateProduct(product_id: any, pay_load: any, header: any) {
    this.http
      .put(`http://127.0.0.1:5000/stocks/update_stock/${product_id}`, pay_load, { headers: header })
      .subscribe({
        next: (response) => {
          console.log('Product updated Sucessfully', response)
          this.showMessage("Product updated Sucessfully", 'success');
          window.scrollTo({ top: 0, behavior: 'smooth' });
          setTimeout(() => {
            window.location.reload();
          }, 3000);
        },
        error: (err) => {
          console.error('Error updated New Product : ', err);
          this.showMessage('Failed to updated Product. Please try again.', 'error');
        }
      });
  }

  // API to update the product Price
  updateProductPrice(product_id: any, pay_load: any, header: any) {
    this.http
      .put(`http://127.0.0.1:5000/stocks/update_price/${product_id}`, pay_load, { headers: header })
      .subscribe({
        next: (response) => {
          console.log('Product Pricce updated Sucessfully', response)
          this.showMessage("Product Price updated Sucessfully", 'success');
          window.scrollTo({ top: 0, behavior: 'smooth' });
          setTimeout(() => {
            window.location.reload();
          }, 3000);
        },
        error: (err) => {
          console.error('Error updated New Product Price : ', err);
          this.showMessage('Failed to updated Product Price. Please try again.', 'error');
        }
      });

  }

  // API to delete Product
  productDelete(product_id: any, header: any) {
    this.http
      .delete(`http://127.0.0.1:5000/stocks/delete/${product_id}`, { headers: header })
      .subscribe({
        next: (response) => {
          console.log('Product Deleted Sucessfully', response)
          this.showMessage("Product Deleted Sucessfully", 'success');
          window.scrollTo({ top: 0, behavior: 'smooth' });
          setTimeout(() => {
            window.location.reload();
          }, 3000);
        },
        error: (err) => {
          console.error('Error Deleting the product : ', err);
          this.showMessage('Failed to delete the product. Please try again.', 'error');
        }
      });
  }

  AcceptStockRequest(requestid: number, header: any) {
    this.http
      .put(`http://127.0.0.1:5000/inventory/stock-requests/${requestid}/approve`, {}, { headers: header })
      .subscribe({
        next: (response) => {
          console.log('Stock Request approved Sucessfully', response)
          this.showMessage("Stock Request approved Sucessfully", 'success');
          window.scrollTo({ top: 0, behavior: 'smooth' });
          setTimeout(() => {
            window.location.reload();
          }, 3000);
        },
        error: (err) => {
          console.error('Error updating the stock request : ', err);
          this.showMessage('Failed to updated stock Request. Please try again.', 'error');
        }
      });

  }

  rejectStockRequest(requestid: number, header: any) {
    this.http
      .put(`http://127.0.0.1:5000/inventory/stock-requests/${requestid}/reject`, {}, { headers: header })
      .subscribe({
        next: (response) => {
          console.log('Stock Request rejected Sucessfully', response)
          this.showMessage("Stock Request rejected Sucessfully", 'success');
          window.scrollTo({ top: 0, behavior: 'smooth' });
          setTimeout(() => {
            window.location.reload();
          }, 3000);
        },
        error: (err) => {
          console.error('Error updating the stock request : ', err);
          this.showMessage('Failed to updated stock Request. Please try again.', 'error');
        }
      });

  }

  loadReports(): void {
   this.http.get<any[]>('http://127.0.0.1:5000/reports/franchisor', {
      headers: this.getHeader(),
    }).subscribe({
      next: (data) => {
        this.reports = data;
      },
      error: (err) => {
        console.error('Error fetching reports:', err);
      }
    });
  }

  //Methods Basic

  // To show what section to load 
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
  

  // to check if an JWT is present
  checkToken() {
    this.token = this.storageService.getItem('token');
    if (!this.token) {
      this.router.navigate(['/login']);
      return;
    }
  }

  // Check role so that the correct dash board is loaded
  checkRole() {
    const newToken: any = this.storageService.getItem('token');
    const decoded: any = jwtDecode(newToken);
    this.role = decoded.role_id;
    if (this.role === '2') {
      this.router.navigate(['/customer']);
    } else if (this.role === '4') {
      this.router.navigate(['/franchisee']);
    }
  }

  // Header information for API calls
  getHeader() {
    const headers = new HttpHeaders({
      Authorization: `Bearer ${this.token}`,
      'Content-Type': 'application/json',
    });
    return headers;
  }

  //filtering status
  extractStatusOptions(): void {
    const allStatuses = this.stockRequests.map(req => req.status_name);
    this.statusOptions = Array.from(new Set(allStatuses));
  }

  applyFilters(): void {
    if (this.selectedStatus) {
      this.filteredStockRequests = this.stockRequests.filter(req => req.status_name === this.selectedStatus);
    } else {
      this.filteredStockRequests = [...this.stockRequests];
    }
  }

  // Method to show Success/Failure Messages
  showMessage(msg: string, type: string) {
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
    }, 3000);
  }

  //to update Commission rate
  updateCommissionRate() {
    this.showMessage(`Commission Rate Update to ${this.commissionRate}%`, 'success');
    console.log(`Commission rate updated to ${this.commissionRate}%`);
  }

  handleViewAction(action: string) {
    alert(`${action} functionality will be implemented here`);
  }

  //filtering functions
  applyApplicationFilters() {
    this.filteredApps = this.applications.filter(app => {
      const matchesSearch = this.applicationSearchTerm === '' ||
        app.applicant.toLowerCase().includes(this.applicationSearchTerm.toLowerCase()) ||
        app.region.toLowerCase().includes(this.applicationSearchTerm.toLowerCase());

      const matchesState = this.selectedState === '' ||
        app.region.toLowerCase().includes(this.selectedState.toLowerCase());

      const matchesStatus = this.selected_Status === '' ||
        app.status === this.selected_Status;

      return matchesSearch && matchesState && matchesStatus;
    });
  }

  get states(): string[] {
    return [...new Set(this.applications.map(app => app.region.split(', ').pop() || ''))]
      .sort((a, b) => a.localeCompare(b));
  }

  applyProductFilters() {
    this.filteredProducts = this.products.filter(product => {
      const matchesSearch =
        this.productSearchTerm === '' ||
        product.name.toLowerCase().includes(this.productSearchTerm.toLowerCase()) ||
        product.category.toLowerCase().includes(this.productSearchTerm.toLowerCase());

      const matchesCategory =
        this.selectedCategory === '' || product.category === this.selectedCategory;

      return matchesSearch && matchesCategory;
    });
  }
  applyStockFilters() {
    this.filteredStockRequests = this.stockRequests.filter(req => {
      const matchesSearch =
        !this.stockSearchTerm ||
        req.franchise.toLowerCase().includes(this.stockSearchTerm.toLowerCase()) ||
        req.product.toLowerCase().includes(this.stockSearchTerm.toLowerCase());

      const matchesStatus =
        !this.selectedStockStatus ||
        req.status_name === this.selectedStockStatus;

      const matchesUrgency =
        !this.selectedStockUrgency ||
        req.urgency === this.selectedStockUrgency;

      return matchesSearch && matchesStatus && matchesUrgency;
    });
  }


  //Application Dialouge Box
  //view Details

  openAppDetails(app: any) {
    this.selectedApplication = app;
    this.showAppDetails = true;
    console.log("Selected Application", this.selectedApplication);
  }


  //Accept Details
  openAcceptDetails(id: any, aid: any) {
    this.selectedApplication = id;
    this.showAcceptDetails = true;
    this.productid = aid;
  }

  acceptApplication() {
    const pay_load = {
      status_id: 2
    };
    this.sendupdatedStatus(this.productid, pay_load, this.getHeader())
    console.log("New Status2 :", pay_load);
    console.log("product ID", this.productid);
    this.closeDialog();
  }


  // Rejected Applications
  openRejectDetails(id: any, aid: any) {
    this.selectedApplication = id;
    this.showAcceptDetails = true;
    this.productid = aid;
  }

  rejectApplication() {
    const pay_load = {
      status_id: 3
    };
    this.sendupdatedStatus(this.productid, pay_load, this.getHeader())
    console.log("New Status2 :", pay_load);
    console.log("product ID : ", this.productid);
    this.closeDialog();

  }

  closeDialog() {
    this.showAppDetails = false;
    this.selectedApplication = null;
    this.showAcceptDetails = false;
    this.showRejectDetails = false;
    this.showAddpProduct = false;
    this.showUpdateStock = false;
    this.showUpdateprice = false;
    this.showDeleteProduct = false;
    this.showAcceptStockRequest = false;
    this.showRejectStockRequest = false;
    this.showStockDetails = false;
    this.productid = 0;
    this.requestid = 0;
    this.productName = '';
    this.productQuantity = 0;
  }

  //add product
  addProductDialouge() {
    this.showAddpProduct = true
  }
  addProduct() {
    this.showMessage('Product Added Sucessfully', 'success')
    //alert('Add new product form would appear here.');
    console.log('Product data:', this.newProduct);
    this.newProduct.user_id = this.franchisor.user_id;
    this.AddProduct(this.newProduct, this.getHeader())
    this.closeDialog();
  }

  //Update Stock
  updateStock() {
    const pay_load = {
      updateStock: this.newStock,
    }
    this.updateProduct(this.product_id, pay_load, this.getHeader())
    console.log("Update Stock : ", pay_load);
    this.closeDialog();

  }

  updateStockDialouge(productid: any) {
    this.showUpdateStock = true;
    this.product_id = productid

  }

  //Update Price
  updatePrice() {
    const pay_load = {
      new_price: this.newPrice,
    }
    this.updateProductPrice(this.product_id, pay_load, this.getHeader())
    console.log("Update Price : ", pay_load);
    this.closeDialog();

  }

  updatePriceDialouge(productid: any) {
    this.showUpdateprice = true;
    this.product_id = productid

  }

  //Delete Product
  deleteProductDialouge(productid: any) {
    this.showDeleteProduct = true;
    this.product_id = productid


  }

  deleteProduct() {
    this.productDelete(this.product_id, this.getHeader())
    this.closeDialog();

  }

  //Acccept Stock request
  acceptStockDialouge(requestID: any, product: any, quantity: any) {
    this.showAcceptStockRequest = true;
    this.requestid = requestID;
    this.productName = product;
    this.productQuantity = quantity;

  }

  acceptRequest() {
    console.log(this.getHeader());
    this.AcceptStockRequest(this.requestid, this.getHeader())
    console.log(this.requestid, this.productName, this.productQuantity);
    this.closeDialog();
  }

  //Acccept Stock request
  rejectStockDialouge(requestID: any, product: any, quantity: any) {
    this.showRejectStockRequest = true;
    this.requestid = requestID;
    this.productName = product;
    this.productQuantity = quantity;

  }

  rejectRequest() {
    console.log(this.getHeader());
    this.rejectStockRequest(this.requestid, this.getHeader())
    console.log(this.requestid, this.productName, this.productQuantity);
    this.closeDialog();
  }

  //View Stock Details
  openStockDetails(stock: any) {
    this.selectedStock = stock;
    this.showStockDetails = true;

  }


  //Method for log out
  logout() {
    localStorage.clear();
    this.router.navigate(['/login']);
  }

}