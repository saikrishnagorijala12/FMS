import { Component, inject, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { StorageServicesService } from '../../../services/storage-services.service';
import { JwtPayload } from '../../../services/interfaces';
import { jwtDecode } from 'jwt-decode';
import { Router, RouterLink } from '@angular/router';

@Component({
  selector: 'app-login',
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent implements OnInit {
  email: string = '';
  password: string = '';
  rememberMe: boolean = false;
  passwordVisible: boolean = false;
  // loading:boolean = true;
  token: string = '';
  roleId: string = '';
  successMessage: string = '';
  errorMessage: string = '';

  private http = inject(HttpClient);
  private storageService = inject(StorageServicesService);
  private router = inject(Router);

  ngOnInit() : void {
    this.checkToken()
  }

  showMessage(msg: string,type:string) {
    if (type === 'error') {
      this.errorMessage = msg;
      this.successMessage = '';
    }
    if(type === 'success') {
      this.successMessage = msg;
      this.errorMessage = ''; 
    }
    setTimeout(() => {
      this.errorMessage = '';
    }, 3000);
  }

  checkToken(): void {
    this.token = this.storageService.getItem('token');
    if (this.token) {

      try {
        const decoded: any = jwtDecode<JwtPayload>(this.token);
        this.roleId=decoded.role_id
        const currentTime = Math.floor(Date.now() / 1000);
        console.log(currentTime)
        if (decoded.exp && decoded.exp > currentTime) {
          this.roleId = decoded.role_id;
          this.callDashboard();
        } else {
          this.storageService.removeItem('token');
        }
      } catch (e) {
        this.storageService.removeItem('token');
      }
    }
  }

  checkRole() {
    // Decode token and route user to correct dashboard
    const decoded = jwtDecode<JwtPayload>(this.token);
    this.roleId = decoded.role_id;
    // console.log("token :", this.token)
    // console.log('roleIid : ', this.roleId)
    this.callDashboard()
  }

  login(): void {
    const pay_load = {
      email: this.email,
      password: this.password,
    };


    this.http.post('http://127.0.0.1:5000/auth/login', pay_load).subscribe({
      next: (response: any) => {

        this.token = response.access_token;
        this.storageService.setItem('token', this.token);
        this.checkRole()
        this.showMessage('Login Sucessfull', 'success')

        //alert('Login successful');
      },
      error: (error) => {
        // this.loading = false;
        this.showMessage('Login Failed. Please Check the Credentials', 'error')
        // alert('Login failed: ' + (error.error?.message || error.message));
      },
    });
  }

  callDashboard() {
    if (this.roleId === "2") {
      this.router.navigate(['/customer']);
      return
    }
    else if (this.roleId === "3") {
      this.router.navigate(['/franchisor']);
      return
    }
    else if (this.roleId === "4") {
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