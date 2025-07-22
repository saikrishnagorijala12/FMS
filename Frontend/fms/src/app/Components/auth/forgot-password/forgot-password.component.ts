import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
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

  onSubmit(form: any) {
    if (form.valid) {
      console.log('Sending reset link to:', this.user.email);
      //const modal = new bootstrap.Modal(document.getElementById('successModal')!);
      // modal.show();
      form.reset();
    }
  }
}
