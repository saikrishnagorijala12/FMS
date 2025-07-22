import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { StorageServicesService } from '../../../services/storage-services.service';
import { JwtPayload } from '../../../services/interfaces';
import { jwtDecode } from 'jwt-decode';
import { Router, RouterLink } from '@angular/router';

@Component({
  selector: 'app-login',
  imports: [CommonModule,FormsModule,RouterLink],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  email: string = '';
  password: string = '';
  rememberMe: boolean = false;
  passwordVisible: boolean = false;
  // loading:boolean = true;
  token : string  = '';
  roleId: string = '';

  private http = inject(HttpClient);
  private storageService = inject(StorageServicesService);
  private router = inject(Router);
  
  onInit(){
    this.checkToken()
  }

  checkToken(){
    this.token = this.storageService.getItem('token');
    if (this.token) {
      this.checkRole()
      return;
    }
  }

  checkRole(){
    // Decode token and route user to correct dashboard
    const decoded = jwtDecode<JwtPayload>(this.token);
        this.roleId = decoded.role_id;
        // console.log("token :", this.token)
        // console.log('roleIid : ', this.roleId)
        this.callDashboard()
  }

  login():void{
    const pay_load ={
      email: this.email,
      password: this.password,
    };

    // this.loading = true;
    
    this.http.post('http://127.0.0.1:5000/auth/login', pay_load).subscribe({
      next: (response: any) => {
        // this.loading = false;
        this.token = response.access_token;
        this.storageService.setItem('token',this.token);
        this.checkRole()
        //alert('Login successful');
      },
      error: (error) => {
        // this.loading = false;
        alert('Login failed: ' + (error.error?.message || error.message));
      },
    });
  }

  callDashboard() {
    if(this.roleId === "2"){
      this.router.navigate(['/customer']);
      return
    }
    else if(this.roleId === "3"){
      this.router.navigate(['/franchisor']);
      return
    }
    else if(this.roleId === "4"){
      this.router.navigate(['/franchisee']);
      return
    }
  }

  togglePassword(): void {
    this.passwordVisible = !this.passwordVisible;
  }



  onSubmit(): void {
    if (this.email && this.password) {
      // console.log('Login Data:', {
      //   email: this.email,
      //   password: this.password,
      //   rememberMe: this.rememberMe,
      // // });
    
  //     setTimeout(() => {
  //   // Redirect or clear the success message
  //   this.router.navigate(['/dashboard']); // or any route
  // }, 1500);
    }
    this.login()
  }
}