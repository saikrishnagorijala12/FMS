import { Routes } from '@angular/router';
import { LoginComponent } from './components/auth/login/login.component';
import { RegisterComponent } from './components/auth/register/register.component';
import { ForgotPasswordComponent } from './components/auth/forgot-password/forgot-password.component';
import { CustomerComponent } from './components/dashboards/customer/customer.component';
import { FranchiseeComponent } from './components/dashboards/franchisee/franchisee.component';
import { FrananchisorComponent } from './components/dashboards/frananchisor/frananchisor.component';


export const routes: Routes = [
    {path: '', redirectTo: '/login', pathMatch: 'full'},
    {path: 'login', component: LoginComponent},
    {path: 'register', component: RegisterComponent},
    {path: 'forgot', component: ForgotPasswordComponent},
    {path: 'customer', component: CustomerComponent},
    {path: 'franchisee', component: FranchiseeComponent},
    {path: 'franchisor', component: FrananchisorComponent}
];
