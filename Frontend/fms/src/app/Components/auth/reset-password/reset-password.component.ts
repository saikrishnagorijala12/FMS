import { Component } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { AuthService } from '../../../services/auth.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { jwtDecode } from 'jwt-decode';


@Component({
  selector: 'app-reset-password',
  imports: [CommonModule, FormsModule],
  templateUrl: './reset-password.component.html',
})
export class ResetPasswordComponent {
  token: string = '';
  password: string = '';
  confirmPassword: string = '';
  message: string = '';
  isSuccess: boolean | null = null;
  userName: string = '';
  errorMessage: string = '';
  successMessage: string = '';
  passwordVisible: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private authService: AuthService,
    private router: Router
  ) { }

  ngOnInit() {
    this.token = this.route.snapshot.paramMap.get('token') || '';
    try {
      const decoded: any = jwtDecode(this.token);

      // In your generate_access_token, you stored `name` inside additional_claims
      this.userName = decoded.name;
    } catch (err) {
      this.showMessage('Invalid or expired reset link', 'error')
    }
  }

   get passwordCriteria() {
    return {
      length: this.password.length >= 8,
      uppercase: /[A-Z]/.test(this.password),
      lowercase: /[a-z]/.test(this.password),
      number: /[0-9]/.test(this.password),
      special: /[!@#$%^&*(),.?":{}|<>]/.test(this.password),
    };
  }


  showMessage(msg: string, msg_type: string) {
    if (msg_type === 'error') {
      this.errorMessage = msg;
      this.successMessage = '';
    }
    if (msg_type === 'success') {
      this.successMessage = msg;
      this.errorMessage = '';
    }
    setTimeout(() => {
      this.errorMessage = '';
      this.successMessage = '';
    }, 3000);
  }

   togglePassword(): void {
    this.passwordVisible = !this.passwordVisible;
  }

  resetPassword() {
    if (this.password !== this.confirmPassword) {
      this.message = 'Passwords do not match';
      this.isSuccess = false;
      return;
    }
  }

  // 
  onSubmit() {

    this.resetPassword()
  }
}

