import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-forgot-password',
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './forgot-password.component.html',
  styleUrl: './forgot-password.component.css'
})
export class ForgotPasswordComponent {
  user = {
    email: ''
  };
  errorMessage = '';
  successMessage = '';

  private http = inject(HttpClient);

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

  onSubmit(form: any) {
    if (form.valid) {
      console.log('Sending reset link to:', this.user.email);
      this.http.post<any>('http://127.0.0.1:5000/auth/forgot', { email: this.user.email }).subscribe({
        next: (res) => {
          if (res.success) {
            this.showMessage(res.message, 'success')
            // Show success modal
            const modal = document.getElementById('successModal');
            if (modal) {
              // Bootstrap modal trigger
              new (window as any).bootstrap.Modal(modal).show();
            }
          } else {
            this.showMessage(res.message, 'error')
          }
        },
        error: (err) => {
          this.errorMessage = err.error?.message || 'Something went wrong!';
        }
      });
    }
    form.reset();
  }
}