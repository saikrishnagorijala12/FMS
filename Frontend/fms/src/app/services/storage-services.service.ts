import { isPlatformBrowser } from '@angular/common';
import { Inject, Injectable, PLATFORM_ID } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class StorageServicesService {

  constructor(@Inject(PLATFORM_ID) private platformId: Object) {}

  getItem(key: string): string   {
    if (isPlatformBrowser(this.platformId)) {
      return localStorage.getItem(key) ?? '';
    }
    return '' ;
  }

  setItem(key: string, value: string): void {
    if (isPlatformBrowser(this.platformId)) {
      localStorage.setItem(key, value);
    }
  }

  removeItem(key: string): void {
    if (isPlatformBrowser(this.platformId)) {
      localStorage.removeItem(key);
    }
  }
}