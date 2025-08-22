export interface JwtPayload {
  identity: string;         // user_id
  role_id: string;  
  role_name : string;
}

// Customer Dashboard API CALLS Data needed
//customer Details
export interface Customer {
  user_id: number;
  name: string;
  email: string;
  phone_no: string;
  role_id: number;
  address? : string
  preferences? : string;
  emailNotifications? : boolean;
  smsNotifications? : boolean;
  preferredLocationId?:number;
}
//Locations Tab
export interface FranchiseLocation {
  id: number;
  name: string;
  address: string;
  phone: string;
  hours: string;
  services: string[];
  state: string;
  franchisee_id: number;
}

export interface RawLocation {
  location_id: number;
  franchisee_id :number;
  franchisee_user_id: number;
  name: string;
  address: string;
  phone: string;
  hours: string;
  services: string[];
  city: string;
  state: string;
  zipcode: string;
}

export type LocationsResponse = RawLocation[];

export interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  rating: number;
  reviews: number;
  category: string;
  franchisee_id:number;
  
}
export interface ProductResponse {
  products: Product[];
}

//Orders Tab
export interface Orders {
  id: string;
  date: string;
  items: string;
  total: number;
  location: number;
  status: string;
}

export interface RawOrders {
  date: string;
  id: string;
  location: number;
  items: string;
  status: string;
  total: number;
}

export type OrderResponse = RawOrders[];

//cart related
export interface CartItem {
  id: number;
  name: string;
  price: number;
  quantity: number;
  franchisee_id:number;
}



// Franchisee Dashboard Related Interfaces

export interface InventoryItem {
  id: number;
  name: string;
  stock: number;
  category:string;
  price :number;
}

export interface OrderItem {
  product_id: number;
  product_name: string;
  quantity: number;
  price: string; 
}

export interface Order_Response {
  id: number;                 
  order_id: string;           
  customer_id: number;
  franchisee_id: number;
  total_amount: string;      
  delivery_address: string;
  status: string;             
  created_time: string;       
  items: OrderItem[];
}

export interface OrderDisplay {
  order_id :number;
  title: string;   
  status: string;  
}

export interface Sales {
    totalSales: number;
    totalRevenue: number;
    commissionPaid: number;
    withdrawnEarnings: number;
}

export interface OrderItemDetails {
  price: string;
  product_id: number;
  product_name: string;
  quantity: number;
  stock_quantity:number;
}

export interface OrderDetails {
  created_time: string;
  customer_name: string;
  items: OrderItemDetails[];
  order_id: number;
  status: string;
  amount:number;
  display_id:string;
}



// Franchisor Dashboard Needed Interfaces

export interface Applications {
  id: string;
  applicant: string;
  region: string;
  investment: number;
  experience: string;
  status: string;
  aid : number;
}

export interface RawStocksRequests {
  id : string;
  product_id : number;
  franchisee_id:number;
  franchise : string;
  product : String;
  quantity : number;
  urgency : string;
  status_name: string,
}

export interface RawStocks{
  category : string,
  description:string,
  name:string,
  price :number,
  stock_quantity:number,
  product_id:number,
}

export interface Products {
  id : number;
  name : string;
  price : number;
  stock_quantity : number;
  category:string;
  // sales : number;
}