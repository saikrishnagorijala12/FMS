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
}

export interface RawLocation {
  location_id: number;
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

//Products Tab
export interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  rating: number;
  reviews: number;
  category: string;
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
}



// Franchisee Dashboard Related Interfaces

export interface InventoryItem {
  name: string;
  stock: number;
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
  title: string;   
  status: string;  
}

export interface Sales {
    totalSales: number;
    totalRevenue: number;
    commissionPaid: number;
    withdrawnEarnings: number;
}


// Franchisor Dashboard Needed Interfaces

export interface Applications {
  id: string;
  applicant: string;
  region: string;
  investment: number;
  experience: string;
  status: string;
}

export interface RawStocksRequests {
  id : string;
  franchise : string;
  product : String;
  quantity : number;
  urgency : string;
  status: string,
}

export interface Stocks {
  name : string;
  price : number;
  stock : number;
  sales : number;
}