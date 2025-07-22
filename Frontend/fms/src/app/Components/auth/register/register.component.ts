import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component, inject } from '@angular/core';
import { FormsModule, NgForm } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';

@Component({
  selector: 'app-register',
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {
user = {
    firstName: '',
    email: '',
    phone:'',
    password: '',
    confirmPassword: '',
    role:'',
    role_id:0,
    agreeTerms: false
  };

  passwordVisible = false;
  confirmPasswordVisible = false;
  loading : boolean = true;
  errorMessage : string = '';
  successMessage: string = '';

  private http = inject(HttpClient);
  private router = inject(Router);
  

  togglePasswordVisibility() {
    this.passwordVisible = !this.passwordVisible;
  }

  toggleConfirmPasswordVisibility() {
    this.confirmPasswordVisible = !this.confirmPasswordVisible;
  }

  setRole_id():void {
    if(this.user.role === 'customer'){
      this.user.role_id=2;
    }else if (this.user.role === 'franchisor'){
      this.user.role_id = 3;
    }else if (this.user.role === 'franchisee'){
      this.user.role_id = 4;
    }
  }

  register():void{
    this.setRole_id()
    if (
      !this.user.firstName ||
      !this.user.email ||
      !this.user.password ||
      !this.user.role
    ) {
      this.errorMessage = 'Please fill all required fields.';
      return;
    }
    if (this.user.password !== this.user.confirmPassword) {
      this.errorMessage = 'Passwords do not match!';
      return;
    }
    const pay_load = {
      name: this.user.firstName,
      email: this.user.email,
      password: this.user.password,
      phone_no: this.user.phone,
      role_id: this.user.role_id
    };
    console.log(pay_load);
    this.http.post('http://127.0.0.1:5000/auth/register', pay_load).subscribe({
      next: (response: any) => {
        this.loading = false;
        this.successMessage = 'Registration successful! Redirecting...';
        setTimeout(() => {
          this.router.navigate(['/login']);
        }, 1500);
      },
      error: (error) => {
        this.loading = false;
        this.errorMessage =
          'Register failed: ' + (error.error?.message || error.message);
      },
    });
    

  }

  onSubmit(form: NgForm) {
    if (form.valid && this.user.password === this.user.confirmPassword) {
      console.log('Form Submitted:', this.user);
      // handle backend call here
    } else {
      alert('Form is invalid or passwords do not match.');
    }
    this.loading = false;
    this.register()
  }
}